import os
from unittest import TestCase

import helpers
from bcp_out import BCPOut
from config import Config
from postgres_out import PostgresOut
from util.postgres_server_query_wrapper import PostgresServerQueryWrapper
from util.sql_connection_properties import SQLConnectionProperties


class TestPostgresOut(TestCase):
    def setUp(self):
        Config.source = {
            "driver": "postgres",
            "server": "localhost",
            "database": "postgres",
            "port": "5432",
            "username": "postgres",
            "password": "SuperWeakPassword123!"
        }
        Config.working_folder = "bcp"
        sql_connection = SQLConnectionProperties(**Config.source)
        self.conn = PostgresServerQueryWrapper(sql_connection)
        # Make bcp working folder if it doesn't exist
        helpers.make_dir(Config.working_folder)

    def test_export_table(self):
        self.conn.execute_sql_with_no_results("""
            DO $$ 
            BEGIN
              IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'PGOutTest') THEN
                DROP TABLE "PGOutTest";
              END IF;
            CREATE TABLE "PGOutTest" (ID INT, ID2 INT);
            INSERT INTO "PGOutTest" VALUES (1,2), (3,4);
            END $$;
        """)
        postgres_out = PostgresOut()
        postgres_out.export_table("public", "PGOutTest")
        bcp_file_path = "bcp/public_PGInTest.tar"
        self.assertEqual(True, os.path.exists(bcp_file_path))

        with open('bcp/public_PGInTest.tar', "rb") as file_handle:
            self.assertTrue(len(file_handle.read()) > 0)

        with open('bcp/public_PGOutTest_out_err.txt', "r") as file_handle:
            self.assertTrue(len(file_handle.read()) == 0)
