#!/usr/bin/env python
"""
CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/CMDB/blob/master/LICENSE>.
"""
from cmdb import __DEBUG__
from cmdb.utils import get_logger
LOGGER = get_logger()


def build_arg_parser():
    from optparse import OptionParser
    from cmdb import __version__, __title__
    _parser = OptionParser(
        usage="usage: {} [options]".format(__title__),
        version=" {}".format(__version__)
    )
    _parser.add_option('-d', '--debug', action='store_true', default=False, dest='debug',
                       help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_option('-s', '--start', action='store_true', default=True, dest='start',
                       help="starting cmdb core system - enables services")
    _parser.add_option('-c', '--command', action='store_true', default=False, dest='command',
                       help="starting interactive command line interface")

    return _parser.parse_args()


def main(args):
    if args.debug:
        global __DEBUG__
        __DEBUG__ = True
        LOGGER.warning("DEBUG mode enabled")
    if args.start:
        LOGGER.info("Starting rest- and web- server")
        pass#start
    if args.command:
        LOGGER.info("Starting CLI menu")
        pass#cli


if __name__ == "__main__":
    from time import sleep
    welcome_string = '''Welcome to Net|CMDB \nStarting core system with following parameters: \n{}'''
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
