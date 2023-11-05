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
            self.conn.execute_sql_with_no_results("""
                CREATE TABLE temp_constraints AS
                SELECT pc.conname AS constraint_name, pc.conrelid::regclass AS table_name, pg_get_constraintdef(pc.oid) AS definition, pc.contype AS constraint_type
                FROM pg_catalog.pg_constraint AS pc
                INNER JOIN information_schema.table_constraints AS itc
                ON pc.conname = itc.constraint_name
                    AND pc.conrelid::regclass = CAST(itc.table_name AS regclass)
                    AND pc.connamespace::regnamespace = CAST(itc.table_schema AS regnamespace)
                WHERE itc.table_schema NOT IN ('pg_catalog');
                
                DO $$
                DECLARE constraint_name_var TEXT;
                DECLARE constraint_table_var TEXT;
                BEGIN
                    FOR constraint_name_var, constraint_table_var IN
                    SELECT constraint_name ,  table_name FROM temp_constraints ORDER BY constraint_type DESC
                        LOOP
                            EXECUTE 'ALTER TABLE ' || constraint_table_var || ' DROP CONSTRAINT IF EXISTS ' || constraint_name_var || ' CASCADE;';
                        END LOOP;
                END $$;
            """)
        except Exception as e:
            logging.error(f"Error disabling constraints {e}")

    def enable_constraints(self):
        logging.info("Enabling constraints")
        try:
            self.conn.execute_sql_with_no_results("""
                DO $$
                DECLARE constraint_table_var TEXT;
                DECLARE constraint_definition_var TEXT;
                BEGIN
                    FOR constraint_table_var, constraint_definition_var IN
                    SELECT table_name, definition FROM temp_constraints ORDER BY constraint_type DESC
                        LOOP
                            EXECUTE 'ALTER TABLE ' || constraint_table_var || ' ADD ' || constraint_definition_var || ';';
                        END LOOP;
                    DROP TABLE IF EXISTS temp_constraints;
                END $$;
            """)
        except Exception as e:
            logging.error(f"Error enabling constraints {e}")

    def batch_delete_table(self, schema_name, table_name):
        script = f'''
            DELETE FROM "{schema_name}"."{table_name}";        
        '''
        self.conn.execute_sql_with_no_results(script)
        pass
