import json
import logging
import os
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

    def export_tables(self):
        bcp_in_wrapper = BCPWrapper(self.sql_connection, Config.bcp_path, Config.working_folder)
        table_list = helpers.get_table_list(self.sql_connection)
        self.remove_excluded_tables(table_list)
        helpers.make_dir(Config.working_folder)
        
        for table in table_list:
            schema_name, table_name = itemgetter("SchemaName", "TableName")(table)
            self.export_table(bcp_in_wrapper, schema_name, table_name)

        with open(f"./{Config.working_folder}/table_list.json", "w") as filehandle:
            json_string = json.dumps(table_list, sort_keys=True, indent=4)
            filehandle.write(json_string)

    @staticmethod
    def export_table(bcp_out_wrapper, schema_name, table_name):
        logging.debug(f"Exporting table data for [{schema_name}].[{table_name}]")
        out_statement = bcp_out_wrapper.generate_bcp_out_statement(schema_name, table_name)
        os.system(out_statement)
        error_text = helpers.get_error_text(bcp_out_wrapper, "out", schema_name, table_name)
        if len(error_text) > 0:
            logging.error(f"Error Exporting table data for [{schema_name}].[{table_name}] {error_text}")

    @staticmethod
    def remove_excluded_tables(table_list: list[dict]):
        remove_table_list = []
        for table in table_list:
            for exclude_table in Config.exclude_table_list:
                schema_name, table_name = itemgetter("SchemaName", "TableName")(table)
                exclude_schema_name, exclude_table_name = itemgetter("schema", "table")(exclude_table)
                if schema_name == exclude_schema_name and table_name == exclude_table_name:
                    remove_table_list.append(table)

        for remove_table in remove_table_list:
            table_list.remove(remove_table)
