from exaslct_src.lib.docker_save_image_task import DockerSaveImageTask
from exaslct_src.lib.task_creator_from_build_tasks import TaskCreatorFromBuildTasks


class SaveTaskCreatorFromBuildTasks(TaskCreatorFromBuildTasks):

    def __init__(self, save_path: str, force_save: bool):
        self.force_save = force_save
        self.save_path = save_path

    def create_task_with_required_tasks(self, build_task, required_task_info):
        push_task = \
            DockerSaveImageTask(
                image_name=build_task.image_name,
                required_task_info=required_task_info,
                save_path=self.save_path,
                force_save=self.force_save
            )
        return push_task