import jsonpickle
from luigi.parameter import Parameter


class JsonPickleParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, s):
        return jsonpickle.decode(s)

    def serialize(self, x):
        jsonpickle.set_preferred_backend('simplejson')
        return jsonpickle.encode(x)
