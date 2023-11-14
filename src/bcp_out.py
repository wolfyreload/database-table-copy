import json
import logging
import os
import subprocess
from operator import itemgetter

import helpers
from config import Config
from util.bcp_wrapper import BCPWrapper
from util.sql_connection_properties import SQLConnectionProperties


class BCPOut:
    """
    Class for exporting tables from a SQL database using BCP (Bulk Copy Program).
    """

    def __init__(self):
        sql_out_properties = Config.source
        self.sql_connection = SQLConnectionProperties(**sql_out_properties)
        self.bcp_wrapper = BCPWrapper(self.sql_connection, Config.working_folder)

    def export_tables(self):
        table_list = helpers.get_table_list(self.sql_connection)
        helpers.remove_excluded_tables(table_list)

        for table in table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            self.export_table(schema_name, table_name)

        helpers.write_table_list(table_list)

    def export_table(self, schema_name, table_name):
        logging.debug(f"Exporting table data for [{schema_name}].[{table_name}]")
        out_statement = self.bcp_wrapper.generate_bcp_out_statement(schema_name, table_name)
        subprocess.check_call(out_statement, shell=True)
        error_text = helpers.get_error_text(self.bcp_wrapper, "out", schema_name, table_name)
        if len(error_text) > 0:
            logging.error(f"Error Exporting table data for [{schema_name}].[{table_name}] {error_text}")
