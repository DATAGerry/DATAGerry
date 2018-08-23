"""
Logging module
"""
import logging.config
import os
import datetime
DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs/')
DEFAULT_FILE_NAME = 'cmdb'
DEFAULT_FILE_EXTENSION = 'log'


def get_logger(module='cmdb', export=False):
    logging_conf = dict(
        version=1,
        disable_existing_loggers=True,
        handlers={
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'generic'
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'generic',
                'filename': DEFAULT_LOG_DIR + DEFAULT_FILE_NAME + '_' + str(
                    datetime.date.today()) + '.' + DEFAULT_FILE_EXTENSION
            },
        },
        formatters={
            'generic': {
                'format': '[%(asctime)s][%(levelname)-8s] --- %(message)s (%(filename)s)',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'class': 'logging.Formatter'
            }
        },
        loggers={
            'cmdb': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    )
    if export:
        return logging_conf
    logging.config.dictConfig(logging_conf)
    return logging.getLogger(module)
