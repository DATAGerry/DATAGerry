"""
Logging module
"""
import logging.config
import os

DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs/')
DEFAULT_FILE_NAME = 'cmdb'
DEFAULT_FILE_EXTENSION = '.log'
LOGGING_CONF = dict(
    version=1,
    disable_existing_loggers=True,
    handlers={
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'generic'
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": DEFAULT_LOG_DIR + "cmdb" + DEFAULT_FILE_EXTENSION
        },
    },
    formatters={
        "generic": {
            "format": "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter"
        }
    },
    loggers={
        "cmdb": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
)

logging.config.dictConfig(LOGGING_CONF)
CMDB_LOGGER = logging.getLogger('cmdb')
