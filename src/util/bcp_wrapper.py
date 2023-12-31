import subprocess

from util.sql_connection_properties import SQLConnectionProperties

class BCPWrapper:
    """
    Wrapper to simplify interacting with the bcp command line tool.

    :param sql_connection_properties: The SQL connection properties.
    :type sql_connection_properties: SQLConnectionProperties
    :param folder: The folder to store BCP files. Default is "bcp".
    :type folder: str
    """
    def __init__(self, sql_connection_properties: SQLConnectionProperties, folder):
        self.sql_connection_properties = sql_connection_properties
        self.folder = folder

    @staticmethod
    def is_valid_bcp_version(bcp_path) -> bool:
        version_information = str(subprocess.check_output([bcp_path, "-v"]))
        return "18." in version_information

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

        # -n native type
        # -k keep null values
        # -E keep identity values
        # -q quoted identifier
        # -u trust server certificate
        arguments = '-u -n -k -q -E'

        script = (f'/opt/mssql-tools18/bin/bcp '
                  f'"{database}.{schema}.{table}" '
                  f'{operation} ./{self.folder}/{schema}_{table}.bcp '
                  f'-S"{server},{port}" '
                  f'-U {username} '
                  f'-P {password} '
                  f'-e {self.get_error_file_name(schema, table, operation)} '
                  f'{arguments}')

        return script

    def get_error_file_name(self, schema: str, table: str, operation: str):
        return f"./{self.folder}/{schema}_{table}_{operation}_err.txt"
