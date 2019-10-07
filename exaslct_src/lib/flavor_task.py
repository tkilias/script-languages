from pathlib import Path
from typing import Dict, Any

import luigi

from exaslct_src.lib.base.dependency_logger_base_task import DependencyLoggerBaseTask
from exaslct_src.lib.stoppable_task import StoppableTask


class FlavorsBaseTask(DependencyLoggerBaseTask):
    flavor_paths = luigi.ListParameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for flavor_path in self.flavor_paths:
            if not Path(flavor_path).is_dir():
                raise OSError("Flavor path %s not a directory." % flavor_path)

    def create_tasks_for_flavors_with_common_params(self, cls, **kwargs) -> Dict[str, Any]:
        return {flavor_path: self._create_task_for_with_common_params(cls, flavor_path, kwargs)
                for flavor_path in self.flavor_paths}

    def _create_task_for_with_common_params(self, cls, flavor_path, kwargs):
        params = {**kwargs, "flavor_path": flavor_path}
        task = self.create_child_task_with_common_params(cls, **params)
        return task


class FlavorBaseTask(DependencyLoggerBaseTask):
    flavor_path = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not Path(self.flavor_path).is_dir():
            raise OSError("Flavor path %s not a directory." % self.flavor_path)

    def get_flavor_name(self):
        path = Path(self.flavor_path)
        flavor_name = path.name
        return flavor_name


class FlavorTask(StoppableTask):
    flavor_paths = luigi.ListParameter(None)
    flavor_path = luigi.OptionalParameter(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.flavor_paths is not None:
            self.actual_flavor_paths = set(self.flavor_paths)
        elif self.flavor_path is not None:
            self.actual_flavor_paths = [self.flavor_path]
        else:
            raise luigi.parameter.MissingParameterException(
                "either flavor_paths or flavor_path argument is missing")
        for flavor_path in self.actual_flavor_paths:
            if not pathlib.Path(flavor_path).is_dir():
                raise OSError("Flavor path %s not a directory." % flavor_path)


class FlavorWrapperTask(FlavorTask):

    def complete(self):
        return all(r.complete() for r in luigi.task.flatten(self.requires()))
