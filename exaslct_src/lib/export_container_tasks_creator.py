from typing import Dict

from exaslct_src.lib.export_container_task import ExportContainerTask
from exaslct_src.lib.data.required_task_info import RequiredTaskInfo
from exaslct_src.lib.docker.docker_create_image_task import DockerCreateImageTask


class ExportContainerTasksCreator():

    def __init__(self, export_path: str, release_name: str):
        self.release_name = release_name
        self.export_path = export_path

    def create_export_tasks(self, flavor_path: str,
                            build_tasks: Dict[str, DockerCreateImageTask]) \
            -> Dict[str, ExportContainerTask]:
        return {release_type: self._create_export_task(release_type, flavor_path, build_task)
                for release_type, build_task in build_tasks.items()}

    def _create_export_task(self, release_type: str, flavor_path: str,
                            build_task: DockerCreateImageTask) -> ExportContainerTask:
        required_task_info = self._create_required_task_info(build_task)
        return \
            ExportContainerTask(
                required_task_info=required_task_info,
                export_path=self.export_path,
                release_name=self.release_name,
                release_type=release_type,
                flavor_path=flavor_path)

    def _create_required_task_info(self, build_task) -> RequiredTaskInfo:
        required_task_info = \
            RequiredTaskInfo(module_name=build_task.__module__,
                             class_name=build_task.__class__.__name__,
                             params=build_task.param_kwargs)
        return required_task_info
