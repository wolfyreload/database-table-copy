from unittest import TestCase

from util.postgres_server_query_wrapper import PostgresServerQueryWrapper
from util.sql_connection_properties import SQLConnectionProperties


class TestSQLServerQueryWrapper(TestCase):
    def setUp(self):
        sql_properties = {
            "driver": "postgresql",
            "server": "localhost",
            "database": "postgres",
            "port": "5432",
            "username": "postgres",
            "password": "SuperWeakPassword123!"
        }
        sql_connection = SQLConnectionProperties(**sql_properties)
        self.query_wrapper = PostgresServerQueryWrapper(sql_connection)

    def test_basic_query(self):
        query_result = self.query_wrapper.execute_sql_with_dict_result('SELECT 1 AS "Test"')
        self.assertEqual(1, len(query_result))
        self.assertEqual(1, query_result[0]["Test"])

    def test_query_no_results(self):
        self.query_wrapper.execute_sql_with_no_results('SELECT 1 AS "Test"')
