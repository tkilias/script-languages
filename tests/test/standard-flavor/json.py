#!/usr/bin/env python2.7

import os
import sys

sys.path.append(os.path.realpath(__file__ + '/../../../lib'))

import udf
import time


class JsonTests(udf.TestCase):

    def setUp(self):
        self.schema = self.__class__.__name__
        self.query('drop schema %s cascade'%self.schema,ingnore_errors=True)
        self.query('create schema %'%self.schema)
        self.query('open schema %'%self.schema)
        self.query('create table json_table (json VARCHAR(10000))')
        self.query("""insert into json_table values ('{"destination_addresses":["Washington, DC, USA","Philadelphia, PA, USA","Santa Barbara, CA, USA","Miami, FL, USA","Austin, TX, USA","Napa County, CA, USA"],"origin_addresses":["New York, NY, USA"],"rows":[{"elements":[{"distance":{"text":"227 mi","value":365468},"duration":{"text":"3 hours 54 mins","value":14064},"status":"OK"},{"distance":{"text":"94.6 mi","value":152193},"duration":{"text":"1 hour 44 mins","value":6227},"status":"OK"},{"distance":{"text":"2,878 mi","value":4632197},"duration":{"text":"1 day 18 hours","value":151772},"status":"OK"},{"distance":{"text":"1,286 mi","value":2069031},"duration":{"text":"18 hours 43 mins","value":67405},"status":"OK"},{"distance":{"text":"1,742 mi","value":2802972},"duration":{"text":"1 day 2 hours","value":93070},"status":"OK"},{"distance":{"text":"2,871 mi","value":4620514},"duration":{"text":"1 day 18 hours","value":152913},"status":"OK"}]}],"status":"OK"}')""")
        self.query("preload json_table")
        for i in range(20):
            self.query("insert into json_table select * from json_table")

    def measure(self, func):
        start = time.time()
        func()
        end = time.time()
        elapsed = end -start
        return elapsed

    def test_json(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) RETURNS int AS
            import json
            def run(ctx):
                obj=json.loads(ctx.json)
                return len(obj.keys)
            /
            ''' % (self.connection, self.user, self.pwd)))
        elapsed = self.measure(lambda: self.query('''SELECT parse_json() FROM json_table'''))
        print("json: "+elapsed)

    def tearDown(self):
        self.query("drop schema % cascade"%self.schema)


if __name__ == '__main__':
    udf.main()

