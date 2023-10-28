import logging
import os
import sys
import time

if not os.path.exists("./logs"):
    os.makedirs("./logs")

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler that logs messages to a file
log_file_name = f"./logs/log_{time.strftime('%Y-%m-%d')}.txt"
file_handler = logging.FileHandler(log_file_name)
file_handler.setLevel(logging.DEBUG)

# Create a console handler that logs messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Disable external loggers
# external_logger1 = logging.getLogger('urllib3.connectionpool')
# external_logger1.setLevel(logging.ERROR)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# log unhandled exceptions
sys.excepthook = handle_exception

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="'%(name)s %(asctime)s [%(levelname)s] %(message)s'",
    handlers=[file_handler, console_handler]
)
