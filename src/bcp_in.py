import json
import logging
import os
import subprocess
from operator import itemgetter

import helpers
from config import Config
from util.bcp_wrapper import BCPWrapper
from util.sql_connection_properties import SQLConnectionProperties
from util.sql_server_query_wrapper import SQLServerQueryWrapper


class BCPIn:
    """
    The BCPIn class is responsible for importing tables into a SQL Server database
    using the BCP utility.
    """
    def __init__(self):
        json_string = helpers.read_table_list()

        sql_out_properties = Config.target
        self.sql_connection = SQLConnectionProperties(**sql_out_properties)
        self.table_list = json.loads(json_string)
        self.conn = SQLServerQueryWrapper(self.sql_connection)
        self.bcp_wrapper = BCPWrapper(self.sql_connection, Config.working_folder)

    def import_tables(self):
        full_table_list = helpers.get_table_list(self.sql_connection)
        self.disable_constraints(full_table_list)

        for table in self.table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            self.import_table(schema_name, table_name)

        self.enable_constraints(full_table_list)

    def import_table(self, schema_name, table_name):
        try:
            logging.debug(f"Importing table data for [{schema_name}].[{table_name}]")
            self.batch_delete_table(schema_name, table_name)
            in_statement = self.bcp_wrapper.generate_bcp_in_statement(schema_name, table_name)
            subprocess.check_call(in_statement, shell=True)
            error_text = helpers.get_error_text(self.bcp_wrapper, "in", schema_name, table_name)
            if len(error_text) > 0:
                logging.error(f"Error Importing table data for [{schema_name}].[{table_name}] {error_text}")
        except Exception as e:
            logging.error(f"Error Importing table data for [{schema_name}].[{table_name}]", e)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error Importing table data for [{schema_name}].[{table_name}]", e)

    def disable_constraints(self, full_table_list):
        logging.info("Disabling constraints")
        for table in full_table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            try:
                self.conn.execute_sql_with_no_results(
                    f"ALTER TABLE [{schema_name}].[{table_name}] NOCHECK CONSTRAINT ALL")
            except Exception as e:
                logging.error(f"Error disabling constraints for table [{schema_name}].[{table_name}] {e}")

    def enable_constraints(self, full_table_list):
        logging.info("Enabling constraints")
        for table in full_table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            try:
                self.conn.execute_sql_with_no_results(
                    f"ALTER TABLE [{schema_name}].[{table_name}] WITH CHECK CHECK CONSTRAINT ALL")
            except Exception as e:
                logging.error(f"Error enabling constraints for table [{schema_name}].[{table_name}] {e}")

    def batch_delete_table(self, schema_name, table_name):
        script = f"""
            DECLARE @BatchSize INT = 1000;
            DECLARE @RowsAffected INT = 1;
            
            WHILE @RowsAffected > 0
            BEGIN
                DELETE TOP (@BatchSize)
                FROM [{schema_name}].[{table_name}];
            
                SET @RowsAffected = @@ROWCOUNT;
            END
        """
        self.conn.execute_sql_with_no_results(script)
        pass
