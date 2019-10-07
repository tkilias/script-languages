from typing import Dict

import jsonpickle
import luigi

from exaslct_src.lib.flavor_task import FlavorBaseTask, FlavorsBaseTask
from exaslct_src.lib.test_runner.run_db_tests_parameter import GeneralRunDBTestParameter, \
    RunDBTestsInTestConfigParameter
from exaslct_src.lib.test_runner.spawn_test_environment_parameter import SpawnTestEnvironmentParameter
from exaslct_src.lib.test_runner.test_runner_db_test_task import TestRunnerDBTestTask


class TestContainerParameter(RunDBTestsInTestConfigParameter,
                             GeneralRunDBTestParameter):
    release_goals = luigi.ListParameter(["release"])
    languages = luigi.ListParameter([None])
    reuse_uploaded_container = luigi.BoolParameter(False, significant=False)


class TestContainer(FlavorsBaseTask,
                    TestContainerParameter,
                    SpawnTestEnvironmentParameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        command_line_output_path = self.get_output_path().joinpath("command_line_output")
        self.command_line_output_target = luigi.LocalTarget(str(command_line_output_path))

    def register_required(self):
        tasks = self.create_tasks_for_flavors_with_common_params(
            TestFlavorContainer)  # type: Dict[str,TestFlavorContainer]
        self.test_results_futures = self.register_dependencies(tasks)

    def run_task(self):
        test_results = self.get_values_from_futures(
            self.test_results_futures)
        print("Test Results")
        jsonpickle.set_preferred_backend('simplejson')
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=2)
        print(jsonpickle.encode(test_results))


class TestFlavorContainer(FlavorBaseTask,
                          TestContainerParameter,
                          SpawnTestEnvironmentParameter):

    def register_required(self):
        tasks = [self.generate_tasks_for_flavor(release_goal)
                 for release_goal in self.release_goals]
        self.test_result_futures = self.register_dependencies(tasks)

    def generate_tasks_for_flavor(self, release_goal: str):
        task = self.create_child_task_with_common_params(TestRunnerDBTestTask,
                                                         release_goal=release_goal)
        return task

    def run_task(self):
        test_results = self.get_values_from_futures(self.test_result_futures)
        self.return_object(test_results)
