import os
from unittest import TestCase

import helpers
from bcp_in import BCPIn
from config import Config
from util.sql_connection_properties import SQLConnectionProperties
from util.sql_server_query_wrapper import SQLServerQueryWrapper


class TestBCPIn(TestCase):
    def setUp(self):
        Config.bcp_path = "/opt/mssql-tools18/bin/bcp"
        Config.target = {
            "driver": "ODBC Driver 18 for SQL Server",
            "server": "localhost",
            "database": "master",
            "port": "1433",
            "username": "sa",
            "password": "password123!"
        }
        Config.working_folder = "bcp"
        helpers.write_table_list([{"schema": "dbo", "table": "BcpInTest"}])
        sql_connection = SQLConnectionProperties(**Config.target)
        self.conn = SQLServerQueryWrapper(sql_connection)
        # Make bcp working folder if it doesn't exist
        helpers.make_dir(Config.working_folder)
        self.bcp_in = BCPIn()

    def test_import_table(self):
        self.conn.execute_sql_with_no_results("""
            IF EXISTS (SELECT 1 FROM sys.tables WHERE name = 'BcpInTest')
                DROP TABLE BcpInTest;
            
            CREATE TABLE BcpInTest (ID INT, ID2 INT);
        """)
        self.bcp_in.import_table("dbo", "BcpInTest")

        sql_result = self.conn.execute_sql_with_dict_result("SELECT * FROM dbo.BcpInTest")
        self.assertEqual(2, len(sql_result))

    def test_batch_delete_table(self):
        self.conn.execute_sql_with_no_results("""
            IF EXISTS (SELECT 1 FROM sys.tables WHERE name = 'BatchDeleteTest')
                DROP TABLE dbo.BatchDeleteTest;

            CREATE TABLE dbo.BatchDeleteTest (ID INT, ID2 INT);
            INSERT INTO dbo.BatchDeleteTest VALUES (1,2), (3,4)
        """)
        self.bcp_in.batch_delete_table("dbo", "BatchDeleteTest")
        sql_result = self.conn.execute_sql_with_dict_result("SELECT * FROM dbo.BatchDeleteTest")
        self.assertEqual(0, len(sql_result))
