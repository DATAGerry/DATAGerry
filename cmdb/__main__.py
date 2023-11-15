#!/usr/bin/env python
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
DATAGERRY is a flexible asset management tool and
open-source configurable management database
"""
import logging.config
import signal
from time import sleep
from argparse import ArgumentParser, Namespace
import os
import sys

import cmdb
from cmdb import __title__
from cmdb.__check__ import CheckRoutine
from cmdb.__update__ import UpdateRoutine

from cmdb.utils.logger import get_logging_conf
from cmdb.utils.wraps import timing
from cmdb.utils.termcolor import colored
from cmdb.utils.error import CMDBError
from cmdb.utils.system_config import SystemConfigReader

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.database.errors.connection_errors import ServerTimeoutError, DatabaseConnectionError

import cmdb.process_management.process_manager
# -------------------------------------------------------------------------------------------------------------------- #

# setup logging for startup
logging.config.dictConfig(get_logging_conf())
LOGGER = logging.getLogger(__name__)



def _activate_debug():
    """
    Activate the debug mode
    """
    cmdb.__MODE__ = 'DEBUG'
    LOGGER.warning("DEBUG mode enabled")



def _check_database():
    """
    Checks whether the specified connection of the configuration is reachable.
    Returns: Datebase if response
    """
    ssc = SystemConfigReader()
    LOGGER.info('Checking database connection with %s data',ssc.config_name)
    database_options = ssc.get_all_values_from_section('Database')
    dbm = DatabaseManagerMongo(**database_options)

    try:
        connection_test = dbm.connector.is_connected()
    except ServerTimeoutError:
        connection_test = False
    LOGGER.debug('Database status is %s',connection_test)

    if connection_test is True:
        return dbm

    retries = 0

    while retries < 3:
        retries += 1
        LOGGER.warning(
            'Retry %i: Checking database connection with %s data', retries, SystemConfigReader.DEFAULT_CONFIG_NAME
        )

        connection_test = dbm.connector.is_connected()

        if connection_test:
            return dbm

    return None



def _start_app():
    """
    Starting the services
    """
    global app_manager

    # install signal handler
    signal.signal(signal.SIGTERM, _stop_app)

    # start app
    app_manager = cmdb.process_management.process_manager.ProcessManager()
    app_status = app_manager.start_app()
    LOGGER.info('Process manager started: %s',app_status)



def _stop_app(signum, frame):
    """TODO: document"""
    global app_manager

    app_manager.stop_app()



def _init_config_reader(config_file):
    """TODO: document"""
    path, filename = os.path.split(config_file)
    if filename is not SystemConfigReader.DEFAULT_CONFIG_NAME or path is not SystemConfigReader.DEFAULT_CONFIG_LOCATION:
        SystemConfigReader.RUNNING_CONFIG_NAME = filename
        SystemConfigReader.RUNNING_CONFIG_LOCATION = path + '/'

    SystemConfigReader(SystemConfigReader.RUNNING_CONFIG_NAME, SystemConfigReader.RUNNING_CONFIG_LOCATION)



def build_arg_parser() -> Namespace:
    """
    Generate application parameter parser
    Returns: instance of OptionParser
    """
    _parser = ArgumentParser(prog='DATAGERRY', usage=f"usage: {__title__} [options]")

    _parser.add_argument('--keys',
                         action='store_true',
                         default=False,
                         dest='keys',
                         help="init keys")

    _parser.add_argument('-d',
                         '--debug',
                         action='store_true',
                         default=False,
                         dest='debug',
                         help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_argument('-s',
                         '--start',
                         action='store_true',
                         default=False,
                         dest='start',
                         help="starting cmdb core system - enables services")

    _parser.add_argument('-c',
                         '--config',
                         default='./etc/cmdb.conf',
                         dest='config_file',
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

# --------------------------------------------------- DEBUG - PART --------------------------------------------------- #
    if args.debug:
        _activate_debug()

    _init_config_reader(args.config_file)

    dbm = None

# --------------------------------------------------- START - PART --------------------------------------------------- #
    # check db-settings and run update if needed
    if args.start:
        try:
            dbm = _check_database()
            if not dbm:
                raise DatabaseConnectionError('Could not establish connection to db')

            LOGGER.info("Database connection established.")

        except CMDBError as error:
            LOGGER.critical(error)
            sys.exit(1)

        check_routine = CheckRoutine(dbm)
        # check db-settings
        try:
            check_status = check_routine.checker()
        except Exception as error:
            LOGGER.error(error)
            check_status = check_routine.get_check_status()
            LOGGER.error('The check did not go through as expected. Please run an update. \n Error: %s', error)

        if check_status == CheckRoutine.CheckStatus.HAS_UPDATES:
            # run update
            update_routine = UpdateRoutine()

            try:
                update_status = update_routine.start_update()
            except RuntimeError as error:
                LOGGER.error(error)
                update_status = update_routine.get_updater_status()
                LOGGER.warning('The update did not go through as expected - Status %s', update_status)

            if update_status == UpdateRoutine.UpateStatus.FINISHED:
                check_status = CheckRoutine.CheckStatus.FINISHED
            else:
                sys.exit(1)

        if check_status == CheckRoutine.CheckStatus.FINISHED:
            # run setup if needed
            from cmdb.__setup__ import SetupRoutine
            setup_routine = SetupRoutine(dbm)

            try:
                setup_status = setup_routine.setup()
            except RuntimeError as error:
                LOGGER.error(error)
                setup_status = setup_routine.get_setup_status()
                LOGGER.warning('The setup did not go through as expected - Status %s', setup_status)

            if setup_status == SetupRoutine.SetupStatus.FINISHED:
                pass
            else:
                sys.exit(1)

        else:
            pass

# ---------------------------------------------------- KEYS - PART --------------------------------------------------- #
    if args.keys:
        from cmdb.__setup__ import SetupRoutine
        setup_routine = SetupRoutine(dbm)
        setup_status = None

        try:
            setup_routine.init_keys()
        except RuntimeError as error:
            LOGGER.error(error)
            setup_status = setup_routine.get_setup_status()
            LOGGER.warning('The key generation did not go through as expected - Status %s', setup_status)

        if setup_status == SetupRoutine.SetupStatus.FINISHED:
            sys.exit(0)
        else:
            sys.exit(1)

    if args.start:
        _start_app()
    sleep(0.2)  # prevent logger output
    LOGGER.info("DATAGERRY successfully started")



if __name__ == "__main__":
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
    license_string = colored('''Copyright (C) 2023 becon GmbH
licensed under the terms of the GNU Affero General Public License version 3\n''', 'yellow')

    try:
        options = build_arg_parser()
        print(brand_string)
        print(welcome_string.format(options.__dict__))
        print(license_string)
        sleep(0.2)  # prevent logger output
        main(options)
    except Exception as err:
        if cmdb.__MODE__ == 'DEBUG':
            import traceback
            traceback.print_exc()

        LOGGER.critical("There was an unforeseen error %s",err)
        LOGGER.info("DATAGERRY stopped!")
        sys.exit(1)
