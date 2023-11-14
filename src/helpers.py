import glob
import json
import os
import shutil
from operator import itemgetter
from pathlib import Path

from config import Config
from util.bcp_wrapper import BCPWrapper
from util.pg_wrapper import PGWrapper
from util.postgres_server_query_wrapper import PostgresServerQueryWrapper
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


def get_pg_error_text(pg_wrapper: PGWrapper, operation: str, schema: str, table: str):
    error_file = pg_wrapper.get_error_file_name(schema, table, operation)
    with open(error_file, "r") as file_handle:
        errors = file_handle.read()
    if len(errors) == 0:
        return ""
    else:
        return errors


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
    conn = PostgresServerQueryWrapper(sql_connection)
    query = """
        SELECT table_schema AS "schema",
               table_name AS "table"
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY "schema", "table"
    """
    table_list = conn.execute_sql_with_dict_result(query)
    return table_list


def cleanup_error_files():
    directory = f"{Config.working_folder}"
    pattern = "*_err.txt"
    files_to_delete = glob.glob(os.path.join(directory, pattern))
    for file_path in files_to_delete:
        os.remove(file_path)


def make_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def remove_excluded_tables(table_list: list[dict]):
    remove_table_list = []
    for table in table_list:
        for exclude_table in Config.exclude_table_list:
            schema_name, table_name = itemgetter("schema", "table")(table)
            exclude_schema_name, exclude_table_name = itemgetter("schema", "table")(exclude_table)
            if schema_name == exclude_schema_name and table_name == exclude_table_name:
                remove_table_list.append(table)

    for remove_table in remove_table_list:
        if remove_table in table_list:
            table_list.remove(remove_table)


def read_table_list():
    with open(f"./{Config.working_folder}/table_list.json", "r") as file_handle:
        json_string = file_handle.read()
        return json_string


def write_table_list(table_list: list[dict]):
    with open(f"./{Config.working_folder}/table_list.json", "w") as filehandle:
        json_string = json.dumps(table_list, sort_keys=True, indent=4)
        filehandle.write(json_string)


def delete_directory(directory_name: str):
    directory_path = Path(directory_name)
    if directory_path.is_dir():
        shutil.rmtree(directory_name)
