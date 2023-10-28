import os

from util.sql_connection_properties import SQLConnectionProperties

class BCPWrapper:
    """
    Wrapper to simplify interacting with the bcp command line tool.

    :param sql_connection_properties: The SQL connection properties.
    :type sql_connection_properties: SQLConnectionProperties
    :param folder: The folder to store BCP files. Default is "bcp".
    :type folder: str
    """
    def __init__(self, sql_connection_properties: SQLConnectionProperties, folder="bcp"):
        self.sql_connection_properties = sql_connection_properties
        self.folder = folder

    def generate_bcp_out_statement(self, schema: str, table: str):
        """
        Generate BCP OUT Statement

        This method is used to generate a BCP OUT statement for a given schema and table.

        :return: The BCP OUT statement as a string.
        """
        script = self.generate_bcp_statement(schema, table, "out")
        return script

    def generate_bcp_in_statement(self, schema: str, table: str):
        """
        Generate BCP IN statement for importing data into a SQL Server table.

        :return: The BCP IN statement as a string.
        """
        script = self.generate_bcp_statement(schema, table, "in")
        return script

    def generate_bcp_statement(self, schema: str, table: str, operation: str):
        database = self.sql_connection_properties.database
        username = self.sql_connection_properties.username
        password = self.sql_connection_properties.password
        port = self.sql_connection_properties.port
        server = self.sql_connection_properties.server

        if os.name == 'nt':
            arguments = '-n -k -q -E'
        else:
            arguments = '-u -n -k -q -E'

        script = (f'bcp '
                  f'"{database}.{schema}.{table}" '
                  f'{operation} ./{self.folder}/{schema}_{table}.bcp '
                  f'-S"{server},{port}" '
                  f'-U {username} '
                  f'-P {password} '
                  f'{arguments}'
                  f' >{self.get_error_file_name(schema, table, operation)} 2>&1')
        # -n native type
        # -k keep null values
        # -E keep identity values
        # -q quoted identifier
        # -u trust server certificate (not working on windows)
        return script

    def get_error_file_name(self, schema: str, table: str, operation: str):
        return f"./{self.folder}/{schema}_{table}_{operation}_err.txt"
