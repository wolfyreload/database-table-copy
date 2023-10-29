from unittest import TestCase

from src.util.sql_connection_properties import SQLConnectionProperties
from src.util.sql_server_query_wrapper import SQLServerQueryWrapper


class TestSQLServerQueryWrapper(TestCase):
    def test_basic_query(self):
        sql_properties = {
            "driver": "ODBC Driver 18 for SQL Server",
            "server": "localhost",
            "database": "master",
            "port": "1433",
            "username": "sa",
            "password": "password123!"
        }
        sql_connection = SQLConnectionProperties(**sql_properties)
        q = SQLServerQueryWrapper(sql_connection)
        query_result = q.execute_sql_with_dict_result("SELECT 1 AS Test")
        self.assertEqual(1, len(query_result))
        self.assertEqual(1, query_result[0]["Test"])
