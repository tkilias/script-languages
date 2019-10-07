import luigi

from exaslct_src.lib.data.container_info import ContainerInfo
from exaslct_src.lib.data.database_info import DatabaseInfo
from exaslct_src.lib.data.docker_network_info import DockerNetworkInfo
from exaslct_src.lib.test_runner.determine_external_database_host import DetermineExternalDatabaseHost
from exaslct_src.lib.test_runner.external_test_environment_parameter import ExternalTestEnvironmentParameter, \
    ExternalDatabaseHostParameter
from exaslct_src.lib.test_runner.prepare_network_for_test_environment import PrepareDockerNetworkForTestEnvironment
from exaslct_src.lib.test_runner.abstract_spawn_test_environment import AbstractSpawnTestEnvironment
from exaslct_src.lib.test_runner.wait_for_external_database import WaitForTestExternalDatabase


class SpawnTestEnvironmentWithExternalDB(AbstractSpawnTestEnvironment,
                                         ExternalDatabaseHostParameter):

    def create_network_task(self, attempt:int):
        return \
            PrepareDockerNetworkForTestEnvironment(
                environment_name=self.environment_name,
                test_container_name=self.test_container_name,
                network_name=self.network_name,
                reuse=self.reuse_test_container,
                attempt=attempt
            )

    def create_spawn_database_task(self, network_info:DockerNetworkInfo, attempt:int):
        return \
            DetermineExternalDatabaseHost(
                environment_name=self.environment_name,
                external_exasol_db_host=self.external_exasol_db_host,
                external_exasol_db_port=self.external_exasol_db_port,
                external_exasol_bucketfs_port=self.external_exasol_bucketfs_port,
                network_info=network_info,
                attempt=attempt
            )

    def create_wait_for_database_task(self,
                                      attempt:int,
                                      database_info:DatabaseInfo,
                                      test_container_info:ContainerInfo):
        return WaitForTestExternalDatabase(
            environment_name=self.environment_name,
            test_container_info=test_container_info,
            database_info=database_info,
            attempt=attempt,
            db_user=self.db_user,
            db_password=self.db_password,
            bucketfs_write_password=self.bucketfs_write_password)
