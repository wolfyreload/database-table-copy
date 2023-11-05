from unittest import TestCase

from util.sql_connection_properties import SQLConnectionProperties
from util.pg_wrapper import PGWrapper


class TestPGWrapper(TestCase):
    def setUp(self):
        sql_properties = {
            "driver": "postgres",
            "server": "localhost",
            "database": "postgres",
            "port": "5432",
            "username": "postgres",
            "password": "SuperWeakPassword123!"
        }
        self.sql_connection = SQLConnectionProperties(**sql_properties)

    def test_generate_pg_dump_statement(self):
        pg_wrapper = PGWrapper(self.sql_connection, "bcp")
        actual = pg_wrapper.generate_pg_dump_statement("public", "TestTable1")
        self.assertTrue(len(actual) > 0)

    def test_generate_pg_restore_statement(self):
        pg_wrapper = PGWrapper(self.sql_connection, "bcp")
        actual = pg_wrapper.generate_pg_restore_statement("public", "TestTable1")
        self.assertTrue(len(actual) > 0)
