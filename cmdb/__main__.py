#!/usr/bin/env python
"""
CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/NetCMDB/blob/master/LICENSE>.
"""

import signal

from cmdb.utils.logger import get_logger
from cmdb.utils.helpers import timing
from cmdb.utils.error import CMDBError
from argparse import ArgumentParser, Namespace
import time

LOGGER = get_logger()


def _check_database():
    """
    Checks whether the specified connection of the configuration is reachable.
    Returns: True if response otherwise False

    """

    from cmdb.utils.system_reader import SystemConfigReader
    from cmdb.data_storage import get_pre_init_database
    LOGGER.info("Checking database connection with {} data".format(SystemConfigReader.DEFAULT_CONFIG_NAME))
    dbm = get_pre_init_database()
    connection_test = dbm.database_connector.is_connected()
    LOGGER.debug("Database status is {}".format(connection_test))
    if connection_test is True:
        dbm.database_connector.disconnect()
        return connection_test
    retries = 0
    while retries < 3:
        retries += 1
        LOGGER.warning("Retry {}: Checking database connection with {} data".format(retries, SystemConfigReader.DEFAULT_CONFIG_NAME))
        connection_test = dbm.database_connector.is_connected()
        if connection_test:
            dbm.database_connector.disconnect()
            return connection_test
    return connection_test


def _activate_debug():
    """
    Activate the debug mode
    """
    import cmdb
    cmdb.__MODE__ = 'DEBUG'
    LOGGER.warning("DEBUG mode enabled")


def _generate_security_keys():
    """
    Generating security settings keys
    """
    LOGGER.info("Generating security keys")
    from cmdb.utils import get_security_manager
    from cmdb.data_storage import get_pre_init_database
    sec_database = get_pre_init_database()
    sec_security = get_security_manager(sec_database)
    sec_security.generate_symmetric_aes_key()
    LOGGER.info("Security keys generated")


def _setup() -> bool:
    """
    Setup function which generates default settings and admin user
    will be triggered with the --setup parameter
    Returns:
        bool: True if setup was complete without error
    """
    from cmdb.user_management import get_user_manager
    from cmdb.user_management.user import User
    from cmdb.data_storage import get_pre_init_database
    from cmdb.utils import get_security_manager
    from datetime import datetime

    try:
        setup_database = get_pre_init_database()
        setup_security = get_security_manager(setup_database)
        setup_security.generate_sym_key()
        _generate_security_keys()
        setup_management = get_user_manager()
        group_id = setup_management.insert_group('admin', 'Administrator')
        admin_username = input('Enter admin USERNAME: ')
        while True:
            admin_pass_1 = input('Enter admin PASSWORD: ')
            admin_pass_2 = input('Repeat admin PASSWORD: ')
            if admin_pass_1 == admin_pass_2:
                break
            else:
                LOGGER.info("Passwords are not the same - please repeate")
        admin_user = User(
            public_id=setup_database.get_highest_id(collection=User.COLLECTION) + 1,
            user_name=admin_username,
            group_id=group_id,
            registration_time=datetime.utcnow(),
            password=setup_security.generate_hmac(admin_pass_1)
        )
        setup_management.insert_user(admin_user)
    except CMDBError as setup_error:
        LOGGER.critical(setup_error)
        return False
    return True


def _load_plugins():
    """
    Loading plugin system
    TODO: Write plugin system
    """
    LOGGER.info("Loading plugins")
    from cmdb.plugins.plugin_system import PluginManager
    pgm = PluginManager()
    LOGGER.info("Plugins loaded")


def _start_app():
    """
    Starting the services
    """
    import cmdb.process_management.process_manager

    global app_manager

    # install signal handler
    signal.signal(signal.SIGTERM, _stop_app)

    # start app
    app_manager = cmdb.process_management.process_manager.ProcessManager()
    app_status = app_manager.start_app()
    LOGGER.info("Process manager started: {}".format(app_status))
    time.sleep(2)  # prevent logger output


def _stop_app(signum, frame):
    global app_manager
    app_manager.stop_app()


def build_arg_parser() -> Namespace:
    """
    Generate application parameter parser
    Returns: instance of OptionParser

    """

    from cmdb import __title__
    _parser = ArgumentParser(
        prog='NetCMDB',
        usage="usage: {} [options]".format(__title__),
    )
    _parser.add_argument('--setup', action='store_true', default=False, dest='setup',
                         help="init cmdb")

    _parser.add_argument('--keys', action='store_true', default=False, dest='keys',
                         help="init securty keys")

    _parser.add_argument('-d', '--debug', action='store_true', default=False, dest='debug',
                         help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_argument('-s', '--start', action='store_true', default=False, dest='start',
                         help="starting cmdb core system - enables services")

    _parser.add_argument('-c', '--config', default='./etc/cmdb.conf', dest='config_file',
                         help="optional path to config file")

    return _parser.parse_args()


@timing('CMDB start took')
def main(args):
    """
    Default application start function
    Args:
        args: start-options
    """
    import os

    from cmdb.utils.system_reader import SystemConfigReader
    path, filename = os.path.split(args.config_file)
    if filename is not SystemConfigReader.DEFAULT_CONFIG_NAME or path is not SystemConfigReader.DEFAULT_CONFIG_LOCATION:
        SystemConfigReader.DEFAULT_CONFIG_NAME = filename
        SystemConfigReader.DEFAULT_CONFIG_LOCATION = path + '/'
    from cmdb.data_storage.database_connection import DatabaseConnectionError
    try:
        conn = _check_database()
        if not conn:
            raise DatabaseConnectionError()
        LOGGER.info("Database connection established.")
    except CMDBError as conn_error:
        LOGGER.critical(conn_error.message)
        exit(1)
    if args.setup:
        if args.keys:
            _generate_security_keys()
            exit(1)
        setup_finish = _setup()
        if setup_finish is True:
            LOGGER.info("SETUP COMPLETE")
        else:
            LOGGER.critical("During setup something went wrong - {}".format(setup_finish))
        exit(1)
    if args.debug:
        _activate_debug()
    _load_plugins()
    if args.start:
        _start_app()
    LOGGER.info("CMDB successfully started")


if __name__ == "__main__":

    from time import sleep
    from termcolor import colored

    welcome_string = colored('Welcome to Net|CMDB \nStarting system with following parameters: \n{}\n', 'yellow')
    brand_string = colored('''
###########################################
__  __ _____ _____ ____ __  __ ____  ____
| \ | | ____|_   _/ ___|  \/  |  _ \| __ ) 
|  \| |  _|   | || |   | |\/| | | | |  _ \ 
| |\  | |___  | || |___| |  | | |_| | |_) |
|_| \_|_____| |_| \____|_|  |_|____/|____/ 

###########################################\n''', 'green')

    try:
        options = build_arg_parser()
        print(brand_string)
        print(welcome_string.format(options.__dict__))
        sleep(0.1)  # prevent logger output

        LOGGER.info("CMDB starting...")
        main(options)
    except Exception as e:
        LOGGER.critical("There was an unforeseen error {}".format(e))
        LOGGER.info("CMDB stopped!")
        exit(1)
