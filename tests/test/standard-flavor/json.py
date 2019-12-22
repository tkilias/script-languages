#!/usr/bin/env python2.7

import os
import sys

sys.path.append(os.path.realpath(__file__ + '/../../../lib'))

import udf
import time


class JsonTests(udf.TestCase):

    def setUp(self):
        self.schema = self.__class__.__name__
        self.query('drop schema %s cascade'%self.schema,ignore_errors=True)
        self.query('create schema %s'%self.schema)
        self.query('open schema %s'%self.schema)
        self.query('create table json_table (json VARCHAR(10000))')
        self.query("""
                insert into json_table values ('{"destination_addresses":["Washington, DC, USA","Philadelphia, PA, USA","Santa Barbara, CA, USA","Miami, FL, USA","Austin, TX, USA","Napa County, CA, USA"],"origin_addresses":["New York, NY, USA"],"rows":[{"elements":[{"distance":{"text":"227 mi","value":365468},"duration":{"text":"3 hours 54 mins","value":14064},"status":"OK"},{"distance":{"text":"94.6 mi","value":152193},"duration":{"text":"1 hour 44 mins","value":6227},"status":"OK"},{"distance":{"text":"2,878 mi","value":4632197},"duration":{"text":"1 day 18 hours","value":151772},"status":"OK"},{"distance":{"text":"1,286 mi","value":2069031},"duration":{"text":"18 hours 43 mins","value":67405},"status":"OK"},{"distance":{"text":"1,742 mi","value":2802972},"duration":{"text":"1 day 2 hours","value":93070},"status":"OK"},{"distance":{"text":"2,871 mi","value":4620514},"duration":{"text":"1 day 18 hours","value":152913},"status":"OK"}]}],"status":"OK"}')
                """)
        self.query("preload table json_table")
        for i in range(22):
            self.query("insert into json_table select * from json_table")

    def measure_query(self, query, wrap_count=True):
        elapsed = []
        if wrap_count:
            query = "SELECT count(*) FROM (%s) q"%query
        for i in range(3):
            start = time.time()
            result=self.query(query)
            print("result",result)
            end = time.time()
            elapsed.append(end -start)
        return sum(elapsed)/len(elapsed)

    def test_json_loads(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import json
            def run(ctx):
                obj=json.loads(ctx.json)
                ctx.emit(str(obj["rows"][0]["elements"][0]["distance"]["text"]))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("json_loads: %s"%elapsed)
        self.fail()
    
    def test_simplejson_loads(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import simplejson
            def run(ctx):
                obj=simplejson.loads(ctx.json)
                ctx.emit(str(obj["rows"][0]["elements"][0]["distance"]["text"]))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("simplejson_loads: %s"%elapsed)
        self.fail()
    
    def test_ujson_loads(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import ujson
            def run(ctx):
                obj=ujson.loads(ctx.json)
                ctx.emit(str(obj["rows"][0]["elements"][0]["distance"]["text"]))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("ujson_loads: %s"%elapsed)
        self.fail()
    
    def test_simdjson_loads(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import simdjson
            def run(ctx):
                obj=simdjson.loads(ctx.json.encode("utf8"))
                ctx.emit(str(obj["rows"][0]["elements"][0]["distance"]["text"]))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("simdjson_loads: %s"%elapsed)
        self.fail()

    def test_simdjson_new_pj_new_path(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import simdjson
            def run(ctx):
                json_bytes=ctx.json.encode("utf8")
                pj = simdjson.ParsedJson(json_bytes)
                ctx.emit(str(pj.items('.rows[0].elements[0].distance.text')))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("simdjson_new_pj_new_path: %s"%elapsed)
        self.fail()

    def test_simdjson_reuse_pj_new_path(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            import simdjson
            pj = simdjson.ParsedJson()
            def run(ctx):
                global pj
                json_bytes=ctx.json.encode("utf8")
                length=int(len(json_bytes))
                pj.allocate_capacity(size=length)
                pj.parse(json_bytes)
                ctx.emit(str(pj.items('.rows[0].elements[0].distance.text')))
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("simdjson_reuse_pj_new_path: %s"%elapsed)
        self.fail()


    def test_input_output_baseline(self):
        self.query(udf.fixindent('''
            CREATE OR REPLACE PYTHON3 SCALAR SCRIPT parse_json(json VARCHAR(100000)) EMITS (a VARCHAR(10000)) AS
            def run(ctx):
                json=ctx.json
                ctx.emit("200 mi")
            /
            '''))
        elapsed = self.measure_query('''SELECT parse_json(json) FROM json_table''')
        print("input_output_baseline: %s"%elapsed)
        self.fail()

    def tearDown(self):
        self.query("drop schema %s cascade"%self.schema)


if __name__ == '__main__':
    udf.main()

