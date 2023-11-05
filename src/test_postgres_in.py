from unittest import TestCase

import helpers
from config import Config
from postgres_in import PostgresIn
from util.postgres_server_query_wrapper import PostgresServerQueryWrapper
from util.sql_connection_properties import SQLConnectionProperties


class TestPostgresIn(TestCase):
    def setUp(self):
        Config.bcp_path = "/usr/bin"
        Config.target = {
            "driver": "postgres",
            "server": "localhost",
            "database": "postgres",
            "port": "5432",
            "username": "postgres",
            "password": "SuperWeakPassword123!"
        }
        Config.working_folder = "bcp"
        helpers.write_table_list([{"schema": "public", "table": "PGInTest"}])
        sql_connection = SQLConnectionProperties(**Config.target)
        self.conn = PostgresServerQueryWrapper(sql_connection)
        # Make bcp working folder if it doesn't exist
        helpers.make_dir(Config.working_folder)
        self.pg_in = PostgresIn()

    def test_import_table(self):
        self.conn.execute_sql_with_no_results("""
            DO $$ 
            BEGIN
              IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'PGInTest') THEN
                DROP TABLE "PGInTest";
              END IF;
            CREATE TABLE "PGInTest" (ID INT, ID2 INT);
            END $$;
        """)
        self.pg_in.import_table("public", "PGInTest")

        with open('bcp/public_PGInTest_in_err.txt', "r") as file_handle:
            self.assertTrue(len(file_handle.read()) == 0)

        sql_result = self.conn.execute_sql_with_dict_result('SELECT * FROM public."PGInTest"')
        self.assertEqual(2, len(sql_result))

    def test_batch_delete_table(self):
        self.conn.execute_sql_with_no_results("""
            DO $$ 
            BEGIN
              IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'BatchDeleteTest') THEN
                DROP TABLE "BatchDeleteTest";
              END IF;
            CREATE TABLE "BatchDeleteTest" (ID INT, ID2 INT);
            INSERT INTO "BatchDeleteTest" VALUES (1,2), (3,4);
            END $$;
        """)
        self.pg_in.batch_delete_table("public", "BatchDeleteTest")
        sql_result = self.conn.execute_sql_with_dict_result('SELECT * FROM public."BatchDeleteTest"')
        self.assertEqual(0, len(sql_result))
