import copy
import importlib
from typing import Dict

import luigi

from exaslct_src.lib.base.dependency_logger_base_task import DependencyLoggerBaseTask
from exaslct_src.lib.base.json_pickle_parameter import JsonPickleParameter
from exaslct_src.lib.build_config import build_config
from exaslct_src.lib.data.dependency_collector.dependency_image_info_collector import IMAGE_INFO, \
    DependencyImageInfoCollector
from exaslct_src.lib.data.image_info import ImageState, ImageInfo
from exaslct_src.lib.data.required_task_info import RequiredTaskInfo, RequiredTaskInfoDict
from exaslct_src.lib.docker.docker_build_task import DockerBuildImageTask
from exaslct_src.lib.docker.docker_image_pull_task import DockerPullImageTask
from exaslct_src.lib.docker.docker_load_task import DockerLoadImageTask
from exaslct_src.lib.docker_config import docker_client_config
from exaslct_src.lib.stoppable_task import StoppableTask


class DockerCreateImageTask(DependencyLoggerBaseTask):
    image_name = luigi.Parameter()
    # ParameterVisibility needs to be hidden instead of private, because otherwise a MissingParameter gets thrown
    image_info = JsonPickleParameter(ImageInfo,
                                     visibility=luigi.parameter.ParameterVisibility.HIDDEN,
                                     significant=True)

    def run_task(self):
        yield from self.build(self.image_info)
        self.return_object(self.image_info)

    def build(self, image_info: ImageInfo):
        if image_info.image_state == ImageState.NEEDS_TO_BE_BUILD.name:
            yield DockerBuildImageTask(
                image_name=self.image_name,
                image_info=image_info)
            image_info.image_state = ImageState.WAS_BUILD.name
        elif image_info.image_state == ImageState.CAN_BE_LOADED.name:
            yield DockerLoadImageTask(
                image_name=self.image_name,
                image_info=image_info)
            image_info.image_state = ImageState.WAS_LOADED.name
        elif image_info.image_state == ImageState.REMOTE_AVAILABLE.name:
            yield DockerPullImageTask(
                image_name=self.image_name,
                image_info=image_info)
            image_info.image_state = ImageState.WAS_PULLED.name
        elif image_info.image_state == ImageState.TARGET_LOCALLY_AVAILABLE.name:
            image_info.image_state = ImageState.USED_LOCAL.name
        elif image_info.image_state == ImageState.SOURCE_LOCALLY_AVAILABLE.name:
            image_info.image_state = ImageState.WAS_TAGED.name
            docker_client_config().get_client().images.get(image_info.get_source_complete_name()).tag(
                repository=image_info.target_repository_name,
                tag=image_info.get_target_complete_tag()
            )
        else:
            raise Exception("Task %s: Image state %s not supported for image %s",
                            self.task_id, image_info.image_state, image_info.get_target_complete_name())


class DockerCreateImageTaskWithDeps(DockerCreateImageTask):
    # ParameterVisibility needs to be hidden instead of private, because otherwise a MissingParameter gets thrown
    required_task_infos = JsonPickleParameter(RequiredTaskInfoDict,
                                              visibility=luigi.parameter.ParameterVisibility.HIDDEN,
                                              significant=True)

    def register_required(self):
        self.required_tasks = {key: self.create_required_task(required_task_info)
                               for key, required_task_info
                               in self.required_task_infos.infos.items()}
        self.futures = self.register_dependencies(self.required_tasks)

    def create_required_task(self, required_task_info: RequiredTaskInfo) -> DockerCreateImageTask:
        module = importlib.import_module(required_task_info.module_name)
        class_ = getattr(module, required_task_info.class_name)
        instance = class_(**required_task_info.params)
        return instance

    def run_task(self):
        image_infos = self.get_values_from_futures(self.futures)
        image_info = copy.copy(self.image_info)
        image_info.depends_on_images = image_infos
        yield from self.build(image_info)
        self.return_object(self.image_info)
