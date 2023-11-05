import logging
import sys

from bcp_in import BCPIn
from bcp_out import BCPOut
from config import Config
from util.bcp_wrapper import BCPWrapper

logging.info("Checking for valid bcp version")
if not BCPWrapper.is_valid_bcp_version("/opt/mssql-tools18/bin/bcp"):
    logging.error("Invalid bcp version detected, only version 18 is currently supported")
    sys.exit(1)

logging.info("Exporting tables from source with bcp started")
bcp_out = BCPOut()
bcp_out.export_tables()
logging.info("Exporting tables from source with bcp  completed")

logging.info("Importing tables to target with bcp  started")
bcp_in = BCPIn()
bcp_in.import_tables()
logging.info("Importing tables to target with bcp  completed")