"""
Logging module
"""
import logging.config
import os
import datetime


def get_logger(module='cmdb'):
    default_log_dir = os.path.join(os.path.dirname(__file__), '../../logs/')
    default_file_name = 'cmdb'
    default_file_extension = '.log'
    logging_conf = dict(
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
                "filename": default_log_dir + default_file_name + "_" + str(
                    datetime.date.today()) + default_file_extension
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

    logging.config.dictConfig(logging_conf)
    return logging.getLogger(module)