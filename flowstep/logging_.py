from sys import stderr, stdout
from loguru import logger
from os import getlogin

# Define the format for the logs
log_format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

# Configure the logger
config = {
    "handlers": [
        {"sink": stdout, "format": log_format, "level": "INFO"},
        {"sink": stderr, "format": log_format, "level": "ERROR"},
        {"sink": "logs.log", "format": log_format, "level": "DEBUG"},
        {"sink": "logs.log", "format": log_format, "level": "TRACE", 
         "enqueue": True, "diagnose": True}
    ],
    "extra": {"user": getlogin()}
}
logger.configure(**config)