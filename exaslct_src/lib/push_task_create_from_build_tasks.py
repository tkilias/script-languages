from exaslct_src.lib.docker_push_image_task import DockerPushImageTask
from exaslct_src.lib.task_creator_from_build_tasks import TaskCreatorFromBuildTasks


class PushTaskCreatorFromBuildTasks(TaskCreatorFromBuildTasks):

    def __init__(self, force_push: bool):
        self.force_push = force_push

    def create_task_with_required_tasks(self, build_task, required_task_info):
        push_task = \
            DockerPushImageTask(
                image_name=build_task.image_name,
                required_task_info=required_task_info,
                force_push=self.force_push)
        return push_task