from typing import Dict

from exaslct_src.lib.docker.docker_flavor_image_task import DockerFlavorAnalyzeImageTask


class AnalyzeUDFClientDeps(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "udfclient_deps"

    def get_additional_build_directories_mapping(self) -> Dict[str, str]:
        return {"01_nodoc": "ext/01_nodoc"}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeLanguageDeps(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "language_deps"

    def get_additional_build_directories_mapping(self) -> Dict[str, str]:
        return {"scripts": "ext/scripts"}

    def requires_tasks(self):
        return {"udfclient_deps": self.create_child_task_with_common_params(AnalyzeUDFClientDeps)}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeBuildDeps(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "build_deps"

    def get_additional_build_directories_mapping(self) -> Dict[str, str]:
        return {"01_nodoc": "ext/01_nodoc", "scripts": "ext/scripts"}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeBuildRun(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "build_run"

    def requires_tasks(self):
        return {"build_deps": self.create_child_task_with_common_params(AnalyzeBuildDeps),
                "language_deps": self.create_child_task_with_common_params(AnalyzeLanguageDeps)}

    def get_additional_build_directories_mapping(self) -> Dict[str, str]:
        return {"exaudfclient/base": "exaudfclient/base"}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeBaseTestDeps(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "base_test_deps"

    def requires_tasks(self):
        return {"build_deps": self.create_child_task_with_common_params(AnalyzeBuildDeps)}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeBaseTestBuildRun(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "base_test_build_run"

    def requires_tasks(self):
        return {"base_test_deps": self.create_child_task_with_common_params(AnalyzeBaseTestDeps),
                "language_deps": self.create_child_task_with_common_params(AnalyzeLanguageDeps)}

    def get_additional_build_directories_mapping(self) -> Dict[str, str]:
        return {"exaudfclient/base": "exaudfclient/base", "emulator": "emulator"}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeFlavorBaseDeps(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "flavor_base_deps"

    def requires_tasks(self):
        return {"language_deps": self.create_child_task_with_common_params(AnalyzeLanguageDeps)}

    def get_additional_build_directories_mapping(self):
        return {"01_nodoc": "ext/01_nodoc", "scripts": "ext/scripts"}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeFlavorCustomization(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "flavor_customization"

    def requires_tasks(self):
        return {"flavor_base_deps": self.create_child_task_with_common_params(AnalyzeFlavorBaseDeps)}


class AnalyzeFlavorTestBuildRun(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "flavor_test_build_run"

    def requires_tasks(self):
        return {"flavor_customization": self.create_child_task_with_common_params(AnalyzeFlavorCustomization),
                "base_test_build_run": self.create_child_task_with_common_params(AnalyzeBaseTestBuildRun)}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeRelease(DockerFlavorAnalyzeImageTask):
    def get_build_step(self) -> str:
        return "release"

    def requires_tasks(self):
        return {
            "flavor_customization": self.create_child_task_with_common_params(AnalyzeFlavorCustomization),
            "build_run": self.create_child_task_with_common_params(AnalyzeBuildRun),
            "language_deps": self.create_child_task_with_common_params(AnalyzeLanguageDeps)}

    def get_path_in_flavor(self):
        return "flavor_base"
