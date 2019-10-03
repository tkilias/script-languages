import luigi
from luigi import Config


class job_config(Config):
    job_id = luigi.Parameter()
    remove_return_targets = luigi.BoolParameter(True)
    temporary_base_directory = luigi.OptionalParameter("/tmp")
    output_directory = luigi.Parameter(".build_output")
