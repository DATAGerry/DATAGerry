#!/usr/bin/env python
"""
CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/CMDB/blob/master/LICENSE>.
"""

from gevent import monkey
monkey.patch_all()
from cmdb.utils import get_logger, get_system_config_reader
LOGGER = get_logger()


def activate_debug():
    import cmdb
    cmdb.__DEBUG__ = True
    LOGGER.warning("DEBUG mode enabled")


def build_arg_parser():
    from optparse import OptionParser
    from cmdb import __version__, __title__
    _parser = OptionParser(
        usage="usage: {} [options]".format(__title__),
        version=" {}".format(__version__)
    )
    _parser.add_option('-d', '--debug', action='store_true', default=False, dest='debug',
                       help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_option('-s', '--start', action='store_true', default=False, dest='start',
                       help="starting cmdb core system - enables services")

    _parser.add_option('-c', '--command', action='store_true', default=True, dest='command',
                       help="starting interactive command line interface")

    return _parser.parse_args()


def main(args):
    from multiprocessing import Process, Queue
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
    welcome_string = '''Welcome to Net|CMDB \nStarting system with following parameters: \n{}'''
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
