import logging
from pathlib import Path
from typing import Dict, List, Generator, Any

from luigi import Task

from exaslct_src.AbstractMethodException import AbstractMethodException
from exaslct_src.lib.base.abstract_task_future import AbstractTaskFuture
from exaslct_src.lib.base.job_config import job_config
from exaslct_src.lib.base.pickle_target import PickleTarget
from exaslct_src.lib.base.task_logger_wrapper import TaskLoggerWrapper
from exaslct_src.lib.base.task_state import TaskState
from exaslct_src.lib.base.wrong_task_state_exception import WrongTaskStateException
from exaslct_src.lib.build_config import build_config

RETURN_TARGETS = "return_targets"

DEFAULT_RETURN_OBJECT_NAME = "default"

COMPLETION_TARGET = "completion_target"


class RequiresTaskFuture(AbstractTaskFuture):

    def __init__(self, task: "BaseTask", index: int):
        self._index = index
        self._task = task
        self._outputs_dict = None

    def get_output(self, name: str = DEFAULT_RETURN_OBJECT_NAME):
        return self._get_outputs_dict()[name].read()

    def list_outputs(self) -> List[str]:
        return list(self._get_outputs_dict().keys())

    def _get_outputs_dict(self) -> Dict[str, PickleTarget]:
        if self._task._task_state == TaskState.RUN:
            if self._outputs_dict is None:
                completion_target = self._task.input()[self._index]
                self._outputs_dict = completion_target.read()
            return self._outputs_dict
        else:
            raise WrongTaskStateException(self._task._task_state, "RequiresTaskFuture.read_outputs_dict")


class RunTaskFuture(AbstractTaskFuture):

    def __init__(self, completion_target: PickleTarget):
        self._outputs_dict = None
        self.completion_target = completion_target

    def get_output(self, name: str):
        return self._get_outputs_dict()[name].read()

    def list_outputs(self) -> List[str]:
        return list(self._get_outputs_dict().keys())

    def _get_outputs_dict(self) -> Dict[str, PickleTarget]:
        if self._outputs_dict is None:
            self._outputs_dict = self.completion_target.read()
        return self._outputs_dict


class BaseTask(Task):

    def __init__(self, *args, **kwargs):
        self._registered_tasks = []
        self._registered_return_targets = {}
        self._task_state = TaskState.INIT
        super().__init__(*args, **kwargs)
        logger = logging.getLogger(f'luigi-interface.{self.__class__.__name__}')
        self.logger = TaskLoggerWrapper(logger, self.task_id)
        self._complete_target = PickleTarget(path=self._get_tmp_path_for_completion_target(),
                                             is_tmp=job_config().remove_return_targets)
        self.init()
        self._task_state = TaskState.NONE

    def _get_tmp_path_for_returns(self, name: str) -> Path:
        return Path(self._get_tmp_path_for_task(), RETURN_TARGETS, name)

    def _get_tmp_path_for_completion_target(self) -> Path:
        return Path(self._get_tmp_path_for_task(), COMPLETION_TARGET)

    def _get_tmp_path_for_task(self) -> Path:
        return Path(build_config().output_directory,
                    job_config().job_id,
                    "temp",
                    self.task_id)

    def get_output_path(self) -> Path:
        return Path(build_config().output_directory,
                    job_config().job_id,
                    "output",
                    self.task_id)

    def get_cache_path(self) -> Path:
        return Path(build_config().output_directory, "cache")

    def init(self):
        raise AbstractMethodException()

    def register_dependency(self, task: "BaseTask"):
        if self._task_state == TaskState.INIT:
            index = len(self._registered_tasks)
            self._registered_tasks.append(task)
            return RequiresTaskFuture(self, index)
        else:
            raise WrongTaskStateException(self._task_state, "register_dependency")

    def requires(self):
        return self._registered_tasks

    def output(self):
        return self._complete_target

    def run(self):
        self._task_state = TaskState.RUN
        task_generator = self.run_task()
        if task_generator is not None:
            yield from task_generator
        self._task_state = TaskState.NONE
        self._complete_target.write(self._registered_return_targets)

    def run_task(self):
        raise AbstractMethodException()

    def run_dependency(self, tasks) -> Generator["BaseTask", PickleTarget, Any]:
        if self._task_state == TaskState.RUN:
            completion_targets = yield tasks
            task_futures = self.generate_run_task_furtures(completion_targets)
            return task_futures
        else:
            raise WrongTaskStateException(self._task_state, "run_dependency")

    def generate_run_task_furtures(self, completion_targets):
        if isinstance(completion_targets, dict):
            return {key: self.generate_run_task_furtures(task) for key, task in completion_targets.items()}
        elif isinstance(completion_targets, list):
            return [self.generate_run_task_furtures(task) for task in completion_targets]
        elif isinstance(completion_targets, PickleTarget):
            return RunTaskFuture(completion_targets)
        else:
            return completion_targets

    def return_object(self, object: Any, name: str = DEFAULT_RETURN_OBJECT_NAME):
        """Returns the object to the calling task. The object needs to be pickleable"""
        if self._task_state == TaskState.RUN:
            if name not in self._registered_return_targets:
                target = PickleTarget(self._get_tmp_path_for_returns(name), is_tmp=True)
                self._registered_return_targets[name] = target
                target.write(object)
            else:
                raise Exception(f"return target {name} already used")
        else:
            raise WrongTaskStateException(self._task_state, "return_target")