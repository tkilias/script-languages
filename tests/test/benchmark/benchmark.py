#!/usr/bin/env python2.7

import os
import sys

sys.path.append(os.path.realpath(__file__ + '/../../../lib'))

import udf
from udf import useData, expectedFailure

class BenchmarkTest(udf.TestCase):
    def setUp(self):
        self.query('CREATE SCHEMA benchmark', ignore_errors=True)
        self.query('OPEN SCHEMA benchmark', ignore_errors=True)
        self.query('CREATE TABLE benchmark_input ( id int );')
        self.query('INSERT INTO benchmark_input values %s;'%",".join(["(1)" for i in range(100)]))
        for i in range(20):
            self.query('INSERT INTO benchmark_input select * from benchmark_input;')
        self.query(udf.fixindent('''
                CREATE OR REPLACE benchmark SET SCRIPT benchmark(%s)
                EMITS (test1 VARCHAR(1000)) AS

                /
                '''%",".join(["c%s double"%i for i in range(100)])))

    def test_benchmark(self):
        print(self.query("select benchmark(%s) from benchmark_input;"%",".join(["1.0" for i in range(100)])))

    def tearDown(self):
        self.query('DROP TABLE benchmark_input;')
        self.query('DROP SCRIPT benchmark;')
        self.query('DROP SCHEMA benchmark', ignore_errors=True)

if __name__ == '__main__':
    udf.main()

# vim: ts=4:sts=4:sw=4:et:fdm=indent

