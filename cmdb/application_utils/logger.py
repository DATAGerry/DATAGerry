import logging
import os
import datetime

DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs/')
DEFAULT_FILE_NAME = 'cmdb'
DEFAULT_FILE_EXTENSION = '.log'
LOG_FILE = DEFAULT_LOG_DIR+DEFAULT_FILE_NAME+"_"+str(datetime.date.today())+DEFAULT_FILE_EXTENSION

active_log_level = 'INFO'
active_log_level = logging._nameToLevel[active_log_level]

active_console_level = 'INFO'
active_console_level = logging._nameToLevel[active_console_level]

active_file_level = 'ERROR'
active_file_level = logging._nameToLevel[active_file_level]

formatter = logging.Formatter("[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s)", "%Y-%m-%d %H:%M:%S")

log = logging.getLogger()
log.setLevel(active_log_level)

console_logger = logging.StreamHandler()
console_logger.setLevel(active_console_level)
console_logger.setFormatter(formatter)

try:
    file_logger = logging.FileHandler(LOG_FILE, mode='a')
except FileNotFoundError:
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)
        file_logger = logging.FileHandler(LOG_FILE)

file_logger.setLevel(active_file_level)
file_logger.setFormatter(formatter)

log.addHandler(console_logger)
log.addHandler(file_logger)
