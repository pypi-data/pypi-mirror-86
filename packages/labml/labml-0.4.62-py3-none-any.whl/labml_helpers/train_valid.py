from typing import Optional, Callable, Dict, Tuple

import numpy as np
import torch.optim
import torch.utils.data
from torch import nn

import labml.utils.pytorch as pytorch_utils
from labml import tracker, monit
from labml.configs import option, meta_config
from .training_loop import TrainingLoopConfigs
from labml.utils.pytorch import get_device


class BatchStepProtocol:
    def prepare_for_iteration(self) -> None:
        raise NotImplementedError()

    def init_stats(self) -> Dict[str, any]:
        return {}

    def update_stats(self, stats: Dict[str, any], update: Dict[str, any]):
        for k, v in update.items():
            if k not in stats:
                stats[k] = []
            stats[k].append(v)

    def log_stats(self, stats: Dict[str, any]):
        pass

    def process(self, batch: any, state: any) -> Tuple[Dict[str, any], any]:
        """
        Returns a tuple of stats and state
        """
        raise NotImplementedError()

    def update(self):
        pass


class BatchStep(BatchStepProtocol):
    def __init__(self, *,
                 model: nn.Module,
                 optimizer: torch.optim.Adam,
                 loss_func: Callable,
                 accuracy_func: Callable):
        self.accuracy_func = accuracy_func
        self.loss_func = loss_func
        self.optimizer = optimizer
        self.model = model
        hook_model_outputs(self.model)

        tracker.set_queue("loss.*", 20, True)
        tracker.set_scalar("accuracy.*", True)

    def log_stats(self, stats: any):
        if 'correct' in stats:
            tracker.add("accuracy.", np.sum(stats['correct']) / np.sum(stats['samples']))

    def prepare_for_iteration(self):
        if MODE_STATE.is_train:
            self.model.train()
        else:
            self.model.eval()

    def calculate_loss(self, batch: any, state: any):
        device = get_device(self.model)
        data, target = batch[0].to(device), batch[1].to(device)
        stats = {
            'samples': len(data)
        }

        with monit.section("model"):
            output = self.model(data)

        if isinstance(output, tuple):
            output = output[0]

        loss = self.loss_func(output, target)
        if self.accuracy_func is not None:
            stats['correct'] = self.accuracy_func(output, target)

        tracker.add("loss.", loss)

        return loss, stats, None

    def process(self, batch: any, state: any):
        loss, stats, new_state = self.calculate_loss(batch, state)

        if MODE_STATE.is_train:
            with monit.section('backward'):
                loss.backward()

        return stats, new_state

    def update(self):
        if not MODE_STATE.is_train:
            return
        with monit.section('optimize'):
            self.optimizer.step()
        if MODE_STATE.is_log_parameters:
            pytorch_utils.store_model_indicators(self.model)
        self.optimizer.zero_grad()


class ModeState:
    def __init__(self):
        self._rollback_stack = []

        self.is_log_activations = False
        self.is_train = False
        self.is_log_parameters = False

    def enter(self, mode: Dict[str, any]):
        rollback = {}
        for k, v in mode.items():
            if v is None:
                continue
            rollback[k] = getattr(self, k)
            setattr(self, k, v)

        self._rollback_stack.append(rollback)

        return len(self._rollback_stack)

    def exit(self, n: int):
        assert n == len(self._rollback_stack)

        rollback = self._rollback_stack[-1]
        self._rollback_stack.pop(-1)

        for k, v in rollback.items():
            setattr(self, k, v)


MODE_STATE = ModeState()


class Mode:
    def __init__(self, *,
                 is_train: bool = None,
                 is_log_parameters: bool = None,
                 is_log_activations: bool = None):
        self.mode = {}
        if is_log_activations is not None:
            self.mode['is_log_activations'] = is_log_activations
        if is_train is not None:
            self.mode['is_train'] = is_train
        if is_log_parameters is not None:
            self.mode['is_log_parameters'] = is_log_parameters
        # for k, v in kwargs.items():
        #     if k[0] == '_' or not hasattr(_MODE_STATE, k):
        #         raise RuntimeError(f"Unknown mode {k}={v}")
        #
        #     self.mode[k] = v

        self.idx = -1

    def __enter__(self):
        self.idx = MODE_STATE.enter(self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        MODE_STATE.exit(self.idx)


class ForwardHook:
    def __init__(self, model_name, name: str, module: torch.nn.Module):
        self.model_name = model_name
        self.name = name
        self.module = module
        module.register_forward_hook(self)

    def save(self, name: str, output):
        if isinstance(output, torch.Tensor):
            pytorch_utils.store_l1_l2(name, output)
        elif isinstance(output, tuple):
            for i, o in enumerate(output):
                self.save(f"{name}.{i}", o)

    def __call__(self, module, i, o):
        if not MODE_STATE.is_log_activations:
            return

        self.save(f"module.{self.model_name}.{self.name}", o)


def hook_model_outputs(model: torch.nn.Module, model_name: str = "model"):
    for name, module in model.named_modules():
        if name == '':
            name = 'full'
        ForwardHook(model_name, name, module)


class Trainer:
    def __init__(self, *,
                 name: str,
                 batch_step: BatchStepProtocol,
                 data_loader: torch.utils.data.DataLoader,
                 is_increment_global_step: bool,
                 log_interval: Optional[int],
                 update_interval: Optional[int],
                 inner_iterations: int):
        self.batch_step = batch_step
        self.log_interval = log_interval
        self.update_interval = update_interval
        self.is_increment_global_step = is_increment_global_step
        self.data_loader = data_loader
        self.name = name
        self.__total_steps = len(data_loader)
        self.__iteration_idx = -1
        self.__iterable = None
        self.__n_iteration = -1
        self.inner_iterations = inner_iterations
        self.__state = None
        self.__stats = {}

    def __call__(self):
        if self.__iterable is None or self.__n_iteration >= self.inner_iterations:
            self.__iterable = iter(self.data_loader)
            self.__iteration_idx = 0
            self.__n_iteration = 0
            self.stats = self.batch_step.init_stats()
        self.batch_step.prepare_for_iteration()
        self.__state = None
        with torch.set_grad_enabled(MODE_STATE.is_train):
            self.__iterate()

    def __iterate(self):
        self.__n_iteration += 1
        if self.__iteration_idx >= self.__n_iteration * self.__total_steps / self.inner_iterations:
            return

        is_updated = True
        is_activations_logged = False
        is_parameters_logged = False

        with monit.section(self.name, is_partial=True):
            if self.__iteration_idx == 0:
                monit.progress(0)
            while True:
                i = self.__iteration_idx
                batch = next(self.__iterable)

                with Mode(is_log_activations=(MODE_STATE.is_log_activations and not is_activations_logged)):
                    is_activations_logged = is_activations_logged or MODE_STATE.is_log_activations
                    update, self.__state = self.batch_step.process(batch, self.__state)

                is_updated = False
                self.batch_step.update_stats(self.stats, update)

                if self.is_increment_global_step:
                    tracker.add_global_step(update['samples'])

                if self.update_interval is not None and (i + 1) % self.update_interval == 0:
                    with Mode(is_log_parameters=(MODE_STATE.is_log_parameters and not is_parameters_logged)):
                        is_parameters_logged = is_parameters_logged or MODE_STATE.is_log_parameters
                        self.batch_step.update()
                    is_updated = True

                if self.log_interval is not None and (i + 1) % self.log_interval == 0:
                    tracker.save()

                self.__iteration_idx += 1
                monit.progress(self.__iteration_idx / self.__total_steps)

                if self.__iteration_idx >= self.__n_iteration * self.__total_steps / self.inner_iterations:
                    break

        if not is_updated:
            with Mode(is_log_parameters=(MODE_STATE.is_log_parameters and not is_parameters_logged)):
                self.batch_step.update()

        self.batch_step.log_stats(self.stats)


class TrainValidConfigs(TrainingLoopConfigs):
    epochs: int = 10

    loss_func: Callable
    accuracy_func: Callable
    optimizer: torch.optim.Adam
    model: nn.Module
    batch_step: BatchStepProtocol = 'simple_batch_step'

    trainer: Trainer
    validator: Trainer

    train_log_interval: int = 10
    train_update_interval: int = 1

    loop_count = 'data_loop_count'
    loop_step = None

    train_loader: torch.utils.data.DataLoader
    valid_loader: torch.utils.data.DataLoader

    inner_iterations: int = 1

    is_log_parameters: bool = True
    is_log_activations: bool = True

    def run_step(self):
        for i in range(self.inner_iterations):
            with tracker.namespace('sample'):
                self.sample()
            with Mode(is_train=True,
                      is_log_parameters=self.is_log_parameters,
                      is_log_activations=self.is_log_activations):
                with tracker.namespace('train'):
                    self.trainer()
            if self.validator:
                with tracker.namespace('valid'):
                    self.validator()

    def run(self):
        for _ in self.training_loop:
            self.run_step()

    def sample(self):
        pass


@option(TrainValidConfigs.batch_step)
def simple_batch_step(c: TrainValidConfigs):
    return BatchStep(model=c.model,
                     optimizer=c.optimizer,
                     loss_func=c.loss_func,
                     accuracy_func=c.accuracy_func)


@option(TrainValidConfigs.trainer)
def trainer(c: TrainValidConfigs):
    return Trainer(name='Train',
                   batch_step=c.batch_step,
                   data_loader=c.train_loader,
                   is_increment_global_step=True,
                   log_interval=c.train_log_interval,
                   update_interval=c.train_update_interval,
                   inner_iterations=c.inner_iterations)


@option(TrainValidConfigs.validator)
def validator(c: TrainValidConfigs):
    return Trainer(name='Valid',
                   batch_step=c.batch_step,
                   data_loader=c.valid_loader,
                   is_increment_global_step=False,
                   log_interval=None,
                   update_interval=None,
                   inner_iterations=c.inner_iterations)


@option(TrainValidConfigs.optimizer)
def optimizer(c: TrainValidConfigs):
    from labml_helpers.optimizer import OptimizerConfigs
    opt_conf = OptimizerConfigs()
    opt_conf.parameters = c.model.parameters()
    return opt_conf


@option(TrainValidConfigs.loop_count)
def data_loop_count(c: TrainValidConfigs):
    return c.epochs


meta_config(TrainValidConfigs.train_log_interval,
            TrainValidConfigs.train_update_interval,
            TrainValidConfigs.is_log_parameters,
            TrainValidConfigs.is_log_activations)
