import json
import logging
import os
from operator import itemgetter

import helpers
from config import Config
from util.pg_wrapper import PGWrapper
from util.postgres_server_query_wrapper import PostgresServerQueryWrapper
from util.sql_connection_properties import SQLConnectionProperties


class PostgresIn:
    """
    The BCPIn class is responsible for importing tables into a SQL Server database
    using the BCP utility.
    """

    def __init__(self):
        json_string = helpers.read_table_list()

        sql_out_properties = Config.target
        self.sql_connection = SQLConnectionProperties(**sql_out_properties)
        self.table_list = json.loads(json_string)
        self.conn = PostgresServerQueryWrapper(self.sql_connection)
        self.pg_wrapper = PGWrapper(self.sql_connection, Config.bcp_path, Config.working_folder)

    def import_tables(self):
        self.disable_constraints()

        for table in self.table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            self.import_table(schema_name, table_name)

        self.enable_constraints()

    def import_table(self, schema_name, table_name):
        try:
            logging.debug(f"Importing table data for [{schema_name}].[{table_name}]")
            self.batch_delete_table(schema_name, table_name)
            in_statement = self.pg_wrapper.generate_pg_restore_statement(schema_name, table_name)
            os.system(in_statement)
            error_text = helpers.get_pg_error_text(self.pg_wrapper, "in", schema_name, table_name)
            if len(error_text) > 0:
                logging.error(f"Error Importing table data for [{schema_name}].[{table_name}] {error_text}")
        except Exception as e:
            logging.error(f"Error Importing table data for [{schema_name}].[{table_name}]", e)

    def disable_constraints(self):
        logging.info("Disabling constraints")
        try:
            self.conn.execute_sql_with_no_results(
                f"SET session_replication_role = 'replica';")
        except Exception as e:
            logging.error(f"Error disabling constraints {e}")

    def enable_constraints(self):
        logging.info("Enabling constraints")
        try:
            self.conn.execute_sql_with_no_results(
                f"SET session_replication_role = 'origin';")
        except Exception as e:
            logging.error(f"Error enabling constraints {e}")

    def batch_delete_table(self, schema_name, table_name):
        script = f'''
            TRUNCATE TABLE "{schema_name}"."{table_name}";        
        '''
        self.conn.execute_sql_with_no_results(script)
        pass
