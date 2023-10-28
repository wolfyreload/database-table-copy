import logging
import helpers
import log_configuration

from arg_handler import config_filename
from bcp_in import BCPIn
from bcp_out import BCPOut
from config import Config

logging.info("Starting Database Table Copy")
Config.load(config_filename)

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
