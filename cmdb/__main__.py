#!/usr/bin/env python
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
DATAGERRY is a flexible asset management tool and
open-source configurable management database
"""
import logging
import signal
from time import sleep
from argparse import ArgumentParser, Namespace
from cmdb.utils.logger import get_logging_conf
from cmdb.utils.wraps import timing
from sys import exit

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from cmdb.utils.system_reader import SystemConfigReader
from cmdb.data_storage.database_manager import DatabaseManagerMongo

# setup logging for startup
logging.config.dictConfig(get_logging_conf())
LOGGER = logging.getLogger(__name__)


def _activate_debug():
    """
    Activate the debug mode
    """
    import cmdb
    cmdb.__MODE__ = 'DEBUG'
    LOGGER.warning("DEBUG mode enabled")


def _check_database():
    """
    Checks whether the specified connection of the configuration is reachable.
    Returns: Datebase if response

    """
    from cmdb.data_storage.database_connection import ServerTimeoutError
    ssc = SystemConfigReader()
    LOGGER.info(f'Checking database connection with {ssc.config_name} data')
    database_options = ssc.get_all_values_from_section('Database')
    dbm = DatabaseManagerMongo(
        **database_options
    )
    try:
        connection_test = dbm.connector.is_connected()
    except ServerTimeoutError:
        connection_test = False
    LOGGER.debug(f'Database status is {connection_test}')
    if connection_test is True:
        return dbm
    retries = 0
    while retries < 3:
        retries += 1
        LOGGER.warning(
            f'Retry {retries}: Checking database connection with {SystemConfigReader.DEFAULT_CONFIG_NAME} data')

        connection_test = dbm.connector.is_connected()
        if connection_test:
            return dbm
    return None


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
    LOGGER.info(f'Process manager started: {app_status}')


def _stop_app(signum, frame):
    global app_manager
    app_manager.stop_app()


def _init_config_reader(config_file):
    import os

    path, filename = os.path.split(config_file)
    if filename is not SystemConfigReader.DEFAULT_CONFIG_NAME or path is not SystemConfigReader.DEFAULT_CONFIG_LOCATION:
        SystemConfigReader.RUNNING_CONFIG_NAME = filename
        SystemConfigReader.RUNNING_CONFIG_LOCATION = path + '/'
    SystemConfigReader(SystemConfigReader.RUNNING_CONFIG_NAME,
                       SystemConfigReader.RUNNING_CONFIG_LOCATION)


def build_arg_parser() -> Namespace:
    """
    Generate application parameter parser
    Returns: instance of OptionParser

    """

    from cmdb import __title__
    _parser = ArgumentParser(
        prog='DATAGERRY',
        usage="usage: {} [options]".format(__title__),
    )

    _parser.add_argument('--keys', action='store_true', default=False, dest='keys',
                         help="init keys")

    _parser.add_argument('--test', action='store_true', default=False, dest='test_data',
                         help="generate and insert test data")

    _parser.add_argument('-d', '--debug', action='store_true', default=False, dest='debug',
                         help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_argument('-s', '--start', action='store_true', default=False, dest='start',
                         help="starting cmdb core system - enables services")

    _parser.add_argument('-c', '--config', default='./etc/cmdb.conf', dest='config_file',
                         help="optional path to config file")

    return _parser.parse_args()


@timing('CMDB start')
def main(args):
    """
    Default application start function
    Args:
        args: start-options
    """
    LOGGER.info("DATAGERRY starting...")
    if args.debug:
        _activate_debug()
    _init_config_reader(args.config_file)
    from cmdb.data_storage.database_connection import DatabaseConnectionError

    # create / check connection database manager
    dbm = None
    try:
        dbm = _check_database()
        if not dbm:
            raise DatabaseConnectionError('')
        LOGGER.info("Database connection established.")
    except CMDBError as conn_error:
        LOGGER.critical(conn_error.message)
        exit(1)

    # check db-settings and run update if needed
    if args.start:
        from cmdb.__check__ import CheckRoutine
        check_routine = CheckRoutine(dbm)
        # check db-settings
        try:
            check_status = check_routine.checker()
        except Exception as err:
            LOGGER.error(err)
            check_status = check_routine.get_check_status()
            LOGGER.error(f'The check did not go through as expected. Please run an update. \n Error: {err}')
        if check_status == CheckRoutine.CheckStatus.HAS_UPDATES:
            # run update
            from cmdb.__update__ import UpdateRoutine
            update_routine = UpdateRoutine()
            try:
                update_status = update_routine.start_update()
            except RuntimeError as err:
                LOGGER.error(err)
                update_status = update_routine.get_updater_status()
                LOGGER.warning(f'The update did not go through as expected - Status {update_status}')
            if update_status == UpdateRoutine.UpateStatus.FINISHED:
                pass
            else:
                exit(1)
        if check_status == CheckRoutine.CheckStatus.FINISHED:
            # run setup if needed
            from cmdb.__setup__ import SetupRoutine
            setup_routine = SetupRoutine(dbm)
            try:
                setup_status = setup_routine.setup()
            except RuntimeError as err:
                LOGGER.error(err)
                setup_status = setup_routine.get_setup_status()
                LOGGER.warning(f'The setup did not go through as expected - Status {setup_status}')
            if setup_status == SetupRoutine.SetupStatus.FINISHED:
                pass
            else:
                exit(1)
        else:
            pass

    if args.keys:
        from cmdb.__setup__ import SetupRoutine
        setup_routine = SetupRoutine(dbm)
        setup_status = None
        try:
            setup_routine.init_keys()
        except RuntimeError as err:
            LOGGER.error(err)
            setup_status = setup_routine.get_setup_status()
            LOGGER.warning(f'The key generation did not go through as expected - Status {setup_status}')
        if setup_status == SetupRoutine.SetupStatus.FINISHED:
            exit(0)
        else:
            exit(1)

    if args.test_data:
        _activate_debug()
        from cmdb.utils.data_factory import DataFactory

        ssc = SystemConfigReader()
        database_options = ssc.get_all_values_from_section('Database')
        dbm = DatabaseManagerMongo(
                **database_options
        )
        db_name = dbm.get_database_name()
        LOGGER.warning(f'Inserting test-data into: {db_name}')
        try:
            factory = DataFactory(database_manager=dbm)
            ack = factory.insert_data()
            LOGGER.warning("Test-data was successfully added".format(dbm.get_database_name()))
            if len(ack) > 0:
                LOGGER.critical("Error while inserting test-data: {} - dropping database".format(ack))
                dbm.drop(db_name)  # cleanup database
        except (Exception, CMDBError) as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            dbm.drop(db_name)  # cleanup database
            exit(1)

    if args.start:
        _start_app()
    sleep(0.2)  # prevent logger output
    LOGGER.info("DATAGERRY successfully started")


if __name__ == "__main__":
    from termcolor import colored

    welcome_string = colored('Welcome to DATAGERRY \nStarting system with following parameters: \n{}\n', 'yellow')
    brand_string = colored('''
    ########################################################################                                  
    
    @@@@@     @   @@@@@@@ @           @@@@@  @@@@@@@ @@@@@   @@@@@  @@    @@
    @    @    @@     @    @@         @@@@@@@ @@@@@@@ @@@@@@  @@@@@@ @@@  @@@
    @     @  @  @    @   @  @       @@@   @@ @@@     @@   @@ @@   @@ @@  @@ 
    @     @  @  @    @   @  @       @@       @@@@@@  @@   @@ @@   @@  @@@@  
    @     @ @    @   @  @    @      @@   @@@ @@@@@@  @@@@@@  @@@@@@   @@@@  
    @     @ @@@@@@   @  @@@@@@      @@   @@@ @@@     @@@@@   @@@@@     @@   
    @     @ @    @   @  @    @      @@@   @@ @@@     @@ @@@  @@ @@@    @@   
    @    @ @      @  @ @      @      @@@@@@@ @@@@@@@ @@  @@@ @@  @@@   @@   
    @@@@@  @      @  @ @      @       @@@@@@ @@@@@@@ @@  @@@ @@  @@@   @@   
                        
    ########################################################################\n''', 'green')
    license_string = colored('''Copyright (C) 2019 NETHINKS GmbH
licensed under the terms of the GNU Affero General Public License version 3\n''', 'yellow')

    try:
        options = build_arg_parser()
        print(brand_string)
        print(welcome_string.format(options.__dict__))
        print(license_string)
        sleep(0.2)  # prevent logger output
        main(options)
    except Exception as e:
        import cmdb

        if cmdb.__MODE__ == 'DEBUG':
            import traceback

            traceback.print_exc()
        LOGGER.critical("There was an unforeseen error {}".format(e))
        LOGGER.info("DATAGERRY stopped!")
        exit(1)
