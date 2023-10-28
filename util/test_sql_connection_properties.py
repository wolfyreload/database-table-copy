from unittest import TestCase

from util.sql_connection_properties import SQLConnectionProperties


class TestSQLConnectionProperties(TestCase):
    def test_get_connection_string(self):
        sql_properties = {
            "driver": "ODBC Driver 18 for SQL Server",
            "server": "localhost",
            "database": "master",
            "port": "1433",
            "username": "sa",
            "password": "password123!"
        }
        connection_properties = SQLConnectionProperties(**sql_properties)
        actual = connection_properties.connection_string
        expected = ("DRIVER=ODBC Driver 18 for SQL Server;"
                    "Server=localhost,1433;"
                    "Database=master;"
                    "UID=sa;"
                    "PWD=password123!;"
                    "TrustServerCertificate=yes")
        self.assertEqual(expected, actual)
