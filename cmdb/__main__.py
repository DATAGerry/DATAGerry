#!/usr/bin/env python
"""
CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/CMDB/blob/master/LICENSE>.
"""

from gevent import monkey

monkey.patch_all()
from cmdb.utils import get_logger

LOGGER = get_logger()


def activate_debug():
    import cmdb
    cmdb.__MODE__ = 'DEBUG'
    LOGGER.warning("DEBUG mode enabled")


def _setup():
    from cmdb.data_storage import get_pre_init_database
    from cmdb.user_management import get_user_manager
    from cmdb.utils import get_security_manager

    try:
        setup_database = get_pre_init_database()
        setup_security = get_security_manager(setup_database)
        setup_security.generate_sym_key()
        setup_management = get_user_manager()
        group_id = setup_management.insert_group('admin', 'Administrator')
        admin_pass = input('Enter admin password: ')
        admin_user_id = setup_management.insert_user(
            user_name='admin',
            group_id=group_id,
            password=admin_pass
        )
    except Exception as e:
        return e

    if admin_user_id == 1:
        return True

    return False


def build_arg_parser():
    from optparse import OptionParser
    from cmdb import __version__, __title__
    _parser = OptionParser(
        usage="usage: {} [options]".format(__title__),
        version=" {}".format(__version__)
    )
    _parser.add_option('--setup', action='store_true', default=False, dest='setup',
                       help="init cmdb")
    _parser.add_option('-d', '--debug', action='store_true', default=False, dest='debug',
                       help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_option('-s', '--start', action='store_true', default=False, dest='start',
                       help="starting cmdb core system - enables services")

    _parser.add_option('-c', '--command', action='store_true', default=True, dest='command',
                       help="starting interactive command line interface")

    return _parser.parse_args()


def main(args):
    from multiprocessing import Process, Queue
    if args.setup:
        setup_finish = _setup()
        if setup_finish is True:
            LOGGER.info("SETUP COMPLETE")
        else:
            LOGGER.critical("During setup something went wrong - {}".format(setup_finish))
        exit(0)
    if args.debug:
        activate_debug()
    '''
    if args.command:
        LOGGER.info("Starting CLI menu")
        pass#cli'''
    if args.start:
        from cmdb.interface import HTTPServer, main_application
        LOGGER.info("Starting rest- and web- server")
        server_queue = Queue()
        from cmdb.utils import get_system_config_reader
        web_server_options = get_system_config_reader().get_all_values_from_section('WebServer')
        http_process = Process(
            target=HTTPServer(main_application, web_server_options).run,
            args=(server_queue,)
        )
        http_process.start()
        if server_queue.get():
            LOGGER.info("CMDB successfully started")
        http_process.join()


if __name__ == "__main__":

    from time import sleep
    from termcolor import colored

    welcome_string = colored('Welcome to Net|CMDB \nStarting system with following parameters: \n{}', 'green')
    brand_string = '''
    ###########################################
    __  __ _____ _____ ____ __  __ ____  ____
    | \ | | ____|_   _/ ___|  \/  |  _ \| __ ) 
    |  \| |  _|   | || |   | |\/| | | | |  _ \ 
    | |\  | |___  | || |___| |  | | |_| | |_) |
    |_| \_|_____| |_| \____|_|  |_|____/|____/ 

    ###########################################                                        
    '''

    try:
        (options, args) = build_arg_parser()
        print(brand_string)
        print(welcome_string.format(options))
        sleep(0.1)  # prevent logger output

        LOGGER.info("CMDB starting...")
        main(options)
    except Exception as e:
        LOGGER.critical("There was an unforseen error {}".format(e))
        LOGGER.info("CMDB stopped!")
        exit(1)
