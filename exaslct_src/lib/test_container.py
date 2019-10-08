from typing import Dict

import luigi

from exaslct_src.lib.base.json_pickle_target import JsonPickleTarget
from exaslct_src.lib.flavor_task import FlavorBaseTask, FlavorsBaseTask
from exaslct_src.lib.test_runner.run_db_test_result import RunDBTestsInTestConfigResult
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
            self.test_results_futures)  # type: Dict[str,RunDBTestsInTestConfigResult]
        JsonPickleTarget(self.get_output_path().joinpath("test_results.json")).write(test_results, 4)
        with self.command_line_output_target.open("w") as file:
            for flavor, test_result_of_flavor in test_results.items():
                print(f"Tests for flavor {flavor}: {self.get_status_string(test_result_of_flavor.tests_are_ok)}",
                      file=file)
                self.print_status_for_generic_language_tests(test_result_of_flavor, file)
                self.print_status_for_test_folders(test_result_of_flavor, file)
                self.print_status_for_test_files(test_result_of_flavor, file)

    def print_status_for_test_files(self, test_result_of_flavor, file):
        for test_results_for_test_files in test_result_of_flavor.test_files_output.test_results:
            print(f"- Tests in test files"
                  f"with language {test_results_for_test_files.language}: "
                  f"{self.get_status_string(test_results_for_test_files.tests_are_ok)}",
                  file=file)

    def print_status_for_test_folders(self, test_result_of_flavor, file):
        for test_results_for_test_folder in test_result_of_flavor.test_folders_output.test_results:
            print(f"- Tests in test folder {test_results_for_test_folder.test_folder}"
                  f"with language {test_results_for_test_folder.test_folder}: "
                  f"{self.get_status_string(test_results_for_test_folder.tests_are_ok)}",
                  file=file)

    def print_status_for_generic_language_tests(self, test_result_of_flavor, file):
        for test_results_for_test_folder in test_result_of_flavor.generic_language_tests_output.test_results:
            print(f"- Tests in test folder {test_results_for_test_folder.test_folder}"
                  f"with language {test_results_for_test_folder.language}: "
                  f"{self.get_status_string(test_results_for_test_folder.tests_are_ok)}",
                  file=file)

    def get_status_string(self, status: bool):
        return 'OK' if status else 'FAILED'


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
        test_results = self.get_values_from_futures(self.test_result_futures)  # type: RunDBTestsInTestConfigResult
        JsonPickleTarget(self.get_output_path().joinpath("test_results.json")).write(test_results, 4)
        self.return_object(test_results)
