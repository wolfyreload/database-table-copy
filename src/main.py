import log_configuration
import logging
import sys

import helpers

from arg_handler import config_filename

from config import Config

logging.info("Cleanup error files")
helpers.cleanup_error_files()

from bcp_in import BCPIn
from bcp_out import BCPOut
from postgres_in import PostgresIn
from postgres_out import PostgresOut
from util.bcp_wrapper import BCPWrapper

logging.info("Starting Database Table Copy")
Config.load(config_filename)

# Make bcp working folder if it doesn't exist
helpers.make_dir(Config.working_folder)

if Config.source["driver"] != "postgres":
    import process_bcp
else:
    import process_postgres
