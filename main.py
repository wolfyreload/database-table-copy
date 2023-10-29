import logging
import sys

import helpers
import log_configuration

from arg_handler import config_filename
from bcp_in import BCPIn
from bcp_out import BCPOut
from config import Config
from util.bcp_wrapper import BCPWrapper

logging.info("Starting Database Table Copy")
Config.load(config_filename)

logging.info("Checking for valid bcp version")
if not BCPWrapper.is_valid_bcp_version(Config.bcp_path):
    logging.error("Invalid bcp version detected, only version 18 is currently supported")
    sys.exit(1)

logging.info("Exporting tables from source started")
bcp_out = BCPOut()
bcp_out.export_tables()
logging.info("Exporting tables from source completed")

logging.info("Importing tables to target started")
bcp_in = BCPIn()
bcp_in.import_tables()
logging.info("Importing tables to target completed")

logging.info("Cleanup error files")
helpers.cleanup_error_files()
