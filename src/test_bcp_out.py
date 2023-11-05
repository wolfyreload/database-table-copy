import os
from unittest import TestCase

import helpers
from bcp_out import BCPOut
from config import Config
from util.sql_connection_properties import SQLConnectionProperties
from util.sql_server_query_wrapper import SQLServerQueryWrapper


class TestBCPOut(TestCase):
    def setUp(self):
        Config.bcp_path = "/opt/mssql-tools18/bin/bcp"
        Config.source = {
            "driver": "ODBC Driver 18 for SQL Server",
            "server": "localhost",
            "database": "master",
            "port": "1433",
            "username": "sa",
            "password": "password123!"
        }
        Config.working_folder = "bcp"
        sql_connection = SQLConnectionProperties(**Config.source)
        self.conn = SQLServerQueryWrapper(sql_connection)
        # Make bcp working folder if it doesn't exist
        helpers.make_dir(Config.working_folder)

    def test_export_table(self):
        self.conn.execute_sql_with_no_results("""
            IF EXISTS (SELECT 1 FROM sys.tables WHERE name = 'BcpOutTest')
                DROP TABLE BcpOutTest;
            
            CREATE TABLE BcpOutTest (ID INT, ID2 INT);
            INSERT INTO BcpOutTest VALUES (1,2), (3,4);
        """)
        bcp_out = BCPOut()
        bcp_out.export_table("dbo", "BcpOutTest")
        bcp_file_path = "bcp/dbo_BcpOutTest.bcp"
        self.assertEqual(True, os.path.exists(bcp_file_path))

        with open('bcp/dbo_BcpOutTest.bcp', "r") as file_handle:
            self.assertTrue(len(file_handle.read()) > 0)



