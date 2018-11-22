"""
Logging module
"""
import logging.config
import os
import datetime
DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs/')
DEFAULT_FILE_NAME = 'cmdb'
DEFAULT_FILE_EXTENSION = 'log'


def get_log_level():
    import cmdb
    from cmdb.utils.system_reader import SystemConfigReader
    scr = SystemConfigReader(
        config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
        config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
    )
    try:
        config_mode = scr.get_value('mode', 'Logger')
    except Exception:
        config_mode = None
    if cmdb.__MODE__ == 'DEBUG':
        return 'DEBUG'
    elif config_mode:
        return config_mode
    else:
        return cmdb.__MODE__


def get_logger(module='cmdb', export=False):
    import pathlib

    pathlib.Path(DEFAULT_LOG_DIR).mkdir(parents=True, exist_ok=True)
    logging_conf = dict(
        version=1,
        disable_existing_loggers=True,
        handlers={
            'console': {
                'level': str(get_log_level()),
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
                'level': str(get_log_level()),
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    )
    if export:
        return logging_conf
    logging.config.dictConfig(logging_conf)
    return logging.getLogger(module)
