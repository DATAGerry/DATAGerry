"""
Logging module
"""
import logging.config
import logging.handlers
import os
import datetime
import multiprocessing

DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs/')


def get_log_level():
    """
    loads logger configuration from config file
    will be overwrite cmdb.__MODE__
    Returns:
        config level
    """
    import cmdb
    if cmdb.__MODE__ == 'DEBUG':
        return 'DEBUG'
    else:
        return cmdb.__MODE__


def get_logging_conf():
    """
    returns the logging configuration

    Returns:
        instance of logging.Logger
    """
    import pathlib

    pathlib.Path(DEFAULT_LOG_DIR).mkdir(parents=True, exist_ok=True)

    # get current process name
    proc_name = multiprocessing.current_process().name

    logging_conf = dict(
        version=1,
        disable_existing_loggers=True,
        handlers={
            'console': {
                'level': str(get_log_level()),
                'class': 'logging.StreamHandler',
                'formatter': 'generic'
            },
            'file_daemon': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'generic',
                'filename': "{}{}.log".format(DEFAULT_LOG_DIR, proc_name),
                'maxBytes': 10 * 1024 * 1024,  # 10 MBytes
                'backupCount': 4
            },
            'file_web_access': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'generic',
                'filename': "{}webserver.access.log".format(DEFAULT_LOG_DIR),
                'maxBytes': 10 * 1024 * 1024,  # 10 MBytes
                'backupCount': 4
            },
            'file_web_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'generic',
                'filename': "{}webserver.error.log".format(DEFAULT_LOG_DIR),
                'maxBytes': 10 * 1024 * 1024,  # 10 MBytes
                'backupCount': 4
            }
        },
        formatters={
            'generic': {
                'format': '[%(asctime)s][%(levelname)-8s] --- %(message)s (%(filename)s)',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'class': 'logging.Formatter'
            }
        },
        loggers={
            "cmdb": {
                'level': str(get_log_level()),
                'handlers': ['console', 'file_daemon'],
                'propagate': False
            },
            "gunicorn.error": {
                "level": "INFO",
                "handlers": ["file_web_error"],
                "propagate": True,
                "qualname": "gunicorn.error"
            },
            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["file_web_access"],
                "propagate": True,
                "qualname": "gunicorn.access"
            }
        }
    )

    return logging_conf
