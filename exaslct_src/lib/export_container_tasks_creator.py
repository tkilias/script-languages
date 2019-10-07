from typing import Dict

from exaslct_src.lib.export_container_task import ExportContainerTask
from exaslct_src.lib.data.required_task_info import RequiredTaskInfo
from exaslct_src.lib.docker.docker_create_image_task import DockerCreateImageTask


class ExportContainerTasksCreator():

    def __init__(self, flavor_path: str, export_path: str, release_name: str):
        self.flavor_path = flavor_path
        self.release_name = release_name
        self.export_path = export_path

    def create_export_tasks(self, build_tasks: Dict[str, DockerCreateImageTask]) \
            -> Dict[str, ExportContainerTask]:
        return {release_goal: self._create_export_task(release_goal, build_task)
                for release_goal, build_task in build_tasks.items()}

    def _create_export_task(self, release_goal: str,
                            build_task: DockerCreateImageTask) -> ExportContainerTask:
        required_task_info = self._create_required_task_info(build_task)
        return \
            ExportContainerTask(
                required_task_info=required_task_info,
                export_path=self.export_path,
                release_name=self.release_name,
                release_goal=release_goal,
                flavor_path=self.flavor_path)

    def _create_required_task_info(self, build_task) -> RequiredTaskInfo:
        required_task_info = \
            RequiredTaskInfo(module_name=build_task.__module__,
                             class_name=build_task.__class__.__name__,
                             params=build_task.param_kwargs)
        return required_task_info
