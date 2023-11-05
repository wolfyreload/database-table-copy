from util.sql_connection_properties import SQLConnectionProperties


class PGWrapper:
    def __init__(self, sql_connection_properties: SQLConnectionProperties, pg_tool_path: str, folder: str):
        self.sql_connection_properties = sql_connection_properties
        self.pg_tool_path = pg_tool_path
        self.folder = folder

    def generate_pg_dump_statement(self, schema: str, table: str):
        """
        Generate a pg_dump statement for this table
        """
        database = self.sql_connection_properties.database
        username = self.sql_connection_properties.username
        password = self.sql_connection_properties.password
        port = self.sql_connection_properties.port
        server = self.sql_connection_properties.server

        script = (f'export PGPASSWORD="{password}" && '
                  f'{self.pg_tool_path}/pg_dump '
                  f'--jobs=4 '
                  f'--host="{server}" '
                  f'--port="{port}" '
                  f'--username="{username}" '
                  f'--format="d" '
                  f'--file="./{self.folder}/{schema}_{table}.dir" '
                  f'--table \'"{schema}"."{table}"\' '
                  f'--no-owner --no-privileges --data-only --column-inserts '
                  f'"{database}"'
                  f'>./{self.folder}/{schema}_{table}_out_err.txt 2>&1'
                  )
        return script

    def generate_pg_restore_statement(self, schema: str, table: str):
        """
        Generate a pg_restore statement for this table
        """
        database = self.sql_connection_properties.database
        username = self.sql_connection_properties.username
        password = self.sql_connection_properties.password
        port = self.sql_connection_properties.port
        server = self.sql_connection_properties.server

        script = (f'export PGPASSWORD="{password}" && '
                  f'{self.pg_tool_path}/pg_restore '
                  f'--jobs=4 '
                  f'--host="{server}" '
                  f'--port="{port}" '
                  f'--dbname="{database}" '
                  f'--username="{username}" '
                  f'--format="d" '
                  f'--no-owner --no-privileges '
                  f'"./{self.folder}/{schema}_{table}.dir" '
                  f'>./{self.folder}/{schema}_{table}_in_err.txt 2>&1'
                  )
        return script

    def get_error_file_name(self, schema: str, table: str, operation: str):
        return f"./{self.folder}/{schema}_{table}_{operation}_err.txt"