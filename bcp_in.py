import json
import logging
import os
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
        json_string = open(f"./{Config.working_folder}/table_list.json", "r").read()

        sql_out_properties = Config.target
        self.sql_connection = SQLConnectionProperties(**sql_out_properties)
        self.table_list = json.loads(json_string)
        self.conn = SQLServerQueryWrapper(self.sql_connection)

    def import_tables(self):
        bcp_out_wrapper = BCPWrapper(self.sql_connection, Config.bcp_path, Config.working_folder)
        full_table_list = helpers.get_table_list(self.sql_connection)
        self.disable_constraints(full_table_list)

        for table in self.table_list:
            schema_name, table_name = itemgetter("SchemaName", "TableName")(table)
            self.import_table(bcp_out_wrapper, schema_name, table_name)

        self.enable_constraints(full_table_list)

    def import_table(self, bcp_out_wrapper, schema_name, table_name):
        try:
            logging.debug(f"Importing table data for [{schema_name}].[{table_name}]")
            self.batch_delete_table(schema_name, table_name)
            in_statement = bcp_out_wrapper.generate_bcp_in_statement(schema_name, table_name)
            os.system(in_statement)
            error_text = helpers.get_error_text(bcp_out_wrapper, "in", schema_name, table_name)
            if len(error_text) > 0:
                logging.error(f"Error Importing table data for [{schema_name}].[{table_name}] {error_text}")
        except Exception as e:
            logging.error(f"Error Importing table data for [{schema_name}].[{table_name}]", e)

    def disable_constraints(self, full_table_list):
        logging.info("Disabling constraints")
        for table in full_table_list:
            schema_name, table_name = itemgetter("SchemaName", "TableName")(table)
            try:
                self.conn.execute_sql_with_no_results(
                    f"ALTER TABLE [{schema_name}].[{table_name}] NOCHECK CONSTRAINT ALL")
            except Exception as e:
                logging.error(f"Error disabling constraints for table [{schema_name}].[{table_name}] {e}")

    def enable_constraints(self, full_table_list):
        logging.info("Enabling constraints")
        for table in full_table_list:
            schema_name, table_name = itemgetter("SchemaName", "TableName")(table)
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
