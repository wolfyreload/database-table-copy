import pyodbc

from util.sql_connection_properties import SQLConnectionProperties


class SQLServerQueryWrapper:
    """
    This class provides methods to execute SQL queries on a SQL Server
     database and retrieve results.
    """
    def __init__(self, connection_properties: SQLConnectionProperties):
        self.connection_string = connection_properties.connection_string

    def execute_sql_with_dict_result(self, query: str, parameters=None) -> list[dict]:
        """
        Execute query and return list of dictionary results

        :param query: the query string
        :param parameters: query parameters
        :return: list[dict]
        """
        with pyodbc.connect(self.connection_string) as connection:
            cursor = self.get_query_cursor(connection, query, parameters)

            # Fetch all the rows and store them in a list of dictionaries
            result_set = []
            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                zipped = zip(columns, row)
                dictionary = dict(zipped)
                result_set.append(dictionary)

            return result_set

    def execute_sql_with_no_results(self, query: str, parameters=None) -> None:
        """
        Execute query and expect no results

        :param query: the query string
        :param parameters: query parameters
        :return: None
        """
        with pyodbc.connect(self.connection_string) as connection:
            cursor = self.get_query_cursor(connection, query, parameters)

    @staticmethod
    def get_query_cursor(
            connection: pyodbc.Connection, query: str, parameters=None
    ) -> pyodbc.Cursor:
        cursor = connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        return cursor
