from exaslct_src.AbstractMethodException import AbstractMethodException


class AbstractTaskFuture:
    def get_output(self, name: str):
        raise AbstractMethodException()

    def list_outputs(self):
        raise AbstractMethodException()