import json
import logging
import sys


class Config:
    """
    Class to handle configuration settings from the config.json
    """
    source = ""
    target = ""
    working_folder = ""
    exclude_table_list = []

    @classmethod
    def load(cls, config_filename):
        try:
            with open(config_filename) as file_handle:
                json_string = file_handle.read()
                json_data = json.loads(json_string)
            cls.source = json_data["source"]
            cls.target = json_data["target"]
            cls.working_folder = json_data["working_folder"]
            cls.exclude_table_list = json_data["exclude_table_list"]
        except Exception as e:
            logging.error(f"Could not load config file '{config_filename}' {e}")
            sys.exit(1)
