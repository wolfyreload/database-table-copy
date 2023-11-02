import glob
import os

from config import Config
from util.bcp_wrapper import BCPWrapper
from util.sql_connection_properties import SQLConnectionProperties
from util.sql_server_query_wrapper import SQLServerQueryWrapper


def get_error_text(bcp_out_wrapper: BCPWrapper, operation: str, schema: str, table: str):
    error_file = bcp_out_wrapper.get_error_file_name(schema, table, operation)
    with open(error_file, "r") as file_handle:
        error_lines = file_handle.readlines()
    for error_line in error_lines:
        if error_line.startswith("Error = "):
            error_line = error_line.replace("Error = ", "").strip()
            return error_line
    else:
        return ""


def get_table_list(sql_connection: SQLConnectionProperties) -> list[dict]:
    conn = SQLServerQueryWrapper(sql_connection)
    query = """
        SELECT s.name AS [schema], t.name AS [table]
        FROM sys.tables t
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE t.is_ms_shipped = 0
        ORDER BY s.name, t.name
    """
    table_list = conn.execute_sql_with_dict_result(query)
    return table_list


def get_postgres_table_list(sql_connection: SQLConnectionProperties) -> list[dict]:
    conn = SQLServerQueryWrapper(sql_connection)
    query = """
        SELECT table_schema AS "schema",
               table_name AS "table"
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY "schema", "table"
    """
    table_list = conn.execute_sql_with_dict_result()


def cleanup_error_files():
    directory = f"{Config.working_folder}"
    pattern = "*_err.txt"
    files_to_delete = glob.glob(os.path.join(directory, pattern))
    for file_path in files_to_delete:
        os.remove(file_path)


def make_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
