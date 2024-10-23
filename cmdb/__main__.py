#!/usr/bin/env python
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
import traceback
from argparse import ArgumentParser, Namespace
import os
import sys

from cmdb.database.mongo_database_manager import MongoDatabaseManager

import cmdb
from cmdb import __title__
from cmdb.__check__ import CheckRoutine
from cmdb.__update__ import UpdateRoutine
from cmdb.__setup__ import SetupRoutine
from cmdb.utils.logger import get_logging_conf
from cmdb.utils.system_config import SystemConfigReader
import cmdb.process_management.process_manager

from cmdb.errors.database import ServerTimeoutError, DatabaseConnectionError
# -------------------------------------------------------------------------------------------------------------------- #

# setup logging for startup
logging.config.dictConfig(get_logging_conf())
LOGGER = logging.getLogger(__name__)

app_manager = cmdb.process_management.process_manager.ProcessManager()


def main(args: Namespace):
    """
    Default application start function
    Args:
        args: start-options
    """
    try:
        dbm = None
        LOGGER.info("DATAGERRY starting...")

        _activate_debug(args)
        __activate_cloud_mode(args)
        _init_config_reader(args.config_file)

        if args.start and not args.cloud:
            try:
                dbm: MongoDatabaseManager = _check_database()

                if not dbm:
                    raise DatabaseConnectionError('Could not establish connection to db')

                LOGGER.info("Database connection established.")

            except DatabaseConnectionError as err:
                LOGGER.critical("%s: %s",type(err), err)
                sys.exit(1)

        # check db-settings and run update if needed
        if args.start and not args.cloud:
            _start_check_routines(dbm)

        if args.keys and not args.cloud:
            _start_key_routine(dbm)

        if args.start:
            _start_app()
            LOGGER.info("DATAGERRY successfully started")
    except Exception as err:
        raise RuntimeError(err) from err

# ----------------------------------------------- ROUTINES AND CHECKERS ---------------------------------------------- #

def _start_key_routine(dbm: MongoDatabaseManager):
    """
    Starts key generation routine
    Args:
        dbm (MongoDatabaseManager): Database Connector
    """
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


def _start_check_routines(dbm: MongoDatabaseManager):
    """
    Starts validation of database structure
    Args:
        dbm (MongoDatabaseManager): Database Connector
    """
    check_routine = CheckRoutine(dbm)
        # check db-settings
    try:
        check_status = check_routine.checker()
    except RuntimeError as error:
        LOGGER.debug("[_start_check_routines] Error: %s", error)
        LOGGER.error('The check did not go through as expected. Please run an update. \n Error: %s', error)
        check_status = check_routine.get_check_status()

    if check_status == CheckRoutine.CheckStatus.HAS_UPDATES:
        # run update
        update_routine = UpdateRoutine(dbm)

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


def _check_database():
    """
    Checks whether the specified connection of the configuration is reachable.
    Returns: Datebase if response
    """
    ssc = SystemConfigReader()
    LOGGER.info('Checking database connection with %s data',ssc.config_name)
    database_options = ssc.get_all_values_from_section('Database')
    dbm = MongoDatabaseManager(**database_options)

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

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

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

    _parser.add_argument('--cloud',
                         action='store_true',
                         default=False,
                         dest='cloud',
                         help="init cloud mode")

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


def _activate_debug(args: Namespace):
    """
    Activate the debug mode if set
    """
    if args.debug:
        cmdb.__MODE__ = 'DEBUG'
        LOGGER.warning("DEBUG mode enabled")


def __activate_cloud_mode(args: Namespace):
    """ Activates cloud mode if set"""
    if args.cloud:
        cmdb.__CLOUD_MODE__ = True
        LOGGER.info("CLOUD MODE enabled")


def _init_config_reader(config_file: str):
    """
    Initialises the config file reader
    Args:
        config_file (str): Path to config file as a string
    """
    path, filename = os.path.split(config_file)

    if filename is not SystemConfigReader.DEFAULT_CONFIG_NAME:
        SystemConfigReader.RUNNING_CONFIG_NAME = filename

    if path is not SystemConfigReader.DEFAULT_CONFIG_LOCATION:
        SystemConfigReader.RUNNING_CONFIG_LOCATION = path + '/'

    SystemConfigReader(SystemConfigReader.RUNNING_CONFIG_NAME, SystemConfigReader.RUNNING_CONFIG_LOCATION)


def _start_app():
    """Starting application services"""
    # install signal handler
    signal.signal(signal.SIGTERM, _stop_app)

    # start app
    app_status = app_manager.start_app()
    LOGGER.info('Process manager started: %s',app_status)


def _stop_app():
    """Stop application services"""
    app_manager.stop_app()

# --------------------------------------------------- INTIALISATION -------------------------------------------------- #

if __name__ == "__main__":
    BRAND_STRING = """
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
                            
        ########################################################################\n
    """

    WELCOME_STRING = """
        Welcome to DATAGERRY
        Starting system with following parameters:
        {}\n
    """

    LICENSE_STRING = """
        Copyright (C) 2024 becon GmbH
        licensed under the terms of the GNU Affero General Public License version 3\n
    """

    try:
        options: Namespace = build_arg_parser()
        print(BRAND_STRING)
        print(WELCOME_STRING.format(options.__dict__))
        print(LICENSE_STRING)
        main(options)
    except RuntimeError as err:
        if cmdb.__MODE__ == 'DEBUG':
            traceback.print_exc()

        LOGGER.critical("%s: %s",type(err).__name__, err)
        LOGGER.info("DATAGERRY stopped!")
        sys.exit(1)
