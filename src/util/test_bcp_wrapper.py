from unittest import TestCase

from util.bcp_wrapper import BCPWrapper
from util.sql_connection_properties import SQLConnectionProperties


class TestBcpWrapper(TestCase):
    def setUp(self):
        sql_properties = {
            "driver": "ODBC Driver 18 for SQL Server",
            "server": "localhost",
            "database": "master",
            "port": "1433",
            "username": "sa",
            "password": "password123!"
        }
        self.sql_connection = SQLConnectionProperties(**sql_properties)

    def test_generate_bcp_out_statement(self):
        bcp_wrapper = BCPWrapper(self.sql_connection, "/opt/mssql-tools18/bin/bcp", "bcp")
        actual = bcp_wrapper.generate_bcp_out_statement("dbo", "Test1")
        self.assertTrue(len(actual) > 0)

    def test_generate_bcp_in_statement(self):
        bcp_wrapper = BCPWrapper(self.sql_connection, "/opt/mssql-tools18/bin/bcp", "bcp")
        actual = bcp_wrapper.generate_bcp_in_statement("dbo", "Test1")
        self.assertTrue(len(actual) > 0)
