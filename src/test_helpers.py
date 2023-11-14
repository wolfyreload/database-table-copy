from unittest import TestCase

import helpers
from config import Config


class TestHelpers(TestCase):
    def test_remove_excluded_tables(self):
        table_list = [
            {
                "schema": "dbo",
                "table": "ErrorLog1"
            },
            {
                "schema": "dbo",
                "table": "ErrorLog2"
            },
            {
                "schema": "dbo",
                "table": "ErrorLog3"
            }
        ]
        Config.exclude_table_list = [
            {
                "schema": "dbo",
                "table": "ErrorLog2"
            },
            {
                "schema": "dbo",
                "table": "ErrorLog3"
            }
        ]
        helpers.remove_excluded_tables(table_list)
        self.assertEqual(1, len(table_list))

    def test_remove_excluded_tables_duplicate_remove(self):
        table_list = [
            {
                "schema": "dbo",
                "table": "ErrorLog1"
            },
            {
                "schema": "dbo",
                "table": "ErrorLog2"
            }
        ]
        Config.exclude_table_list = [
            {
                "schema": "dbo",
                "table": "ErrorLog2"
            },
            {
                "schema": "dbo",
                "table": "ErrorLog2"
            }
        ]
        helpers.remove_excluded_tables(table_list)
        self.assertEqual(1, len(table_list))