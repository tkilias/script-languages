import unittest
from datetime import datetime

import luigi
from luigi import Parameter

from exaslct_src.lib.base.base_task import BaseTask


class TestTask1(BaseTask):
    def init(self):
        self.task2 = self.register_dependency(TestTask2())

    def run_task(self):
        self.logger.info("RUN")
        self.logger.info(f"task2 list_outputs {self.task2.list_outputs()}")
        self.logger.info(f"task2 {self.task2.get_output()}")
        tasks_3 = yield from self.run_dependency({
            "1": TestTask3("e"),
            "2": TestTask3("d"),
        })
        self.logger.info(f"""task3_1 {tasks_3["1"].get_output("output")}""")
        self.logger.info(f"""task3_2 {tasks_3["2"].get_output("output")}""")


class TestTask2(BaseTask):
    def init(self):
        pass

    def run_task(self):
        self.logger.info("RUN")
        self.return_object([1, 2, 3, 4])


class TestTask3(BaseTask):
    input_param = Parameter()

    def init(self):
        pass

    def run_task(self):
        self.logger.info(f"RUN {self.input_param}")
        self.return_object(name="output", object=["a", "b", self.input_param])


class BaseTaskTest(unittest.TestCase):

    def test_something(self):
        job_id = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + str(TestTask1.__name__)
        luigi.configuration.get_config().set('job_config', 'job_id', job_id)

        task = TestTask1()
        luigi.build([task], workers=1, local_scheduler=True, log_level="INFO")


if __name__ == '__main__':
    unittest.main()
