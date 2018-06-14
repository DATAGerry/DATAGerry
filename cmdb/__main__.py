#!/usr/bin/env python
"""
Net|CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/NetCMDB/blob/master/LICENSE>.
"""

from cmdb import __version__, __title__, __DEBUG__
from optparse import OptionParser
from cmdb.application_utils import log
from time import sleep


def build_arg_parser():
    _parser = OptionParser(
        usage="usage: {} [options]".format(__title__),
        version=" {}".format(__version__)
    )
    _parser.add_option('-d', '--debug', action='store_true', default=False, dest='debug',
                       help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")

    _parser.add_option('-s', '--start', action='store_true', default=False, dest='start',
                       help="starting cmdb core system - enables services")

    (options, args) = _parser.parse_args()

    return options, args


def main(args):
    exit_message = "STOPPING cmdb!"
    from cmdb.communication_interface.web_app import create_web_app
    from cmdb.data_storage.database_connection import ServerTimeoutError
    try:
        create_web_app().run()
    except OSError as e:
        log.warning(e.errno)
        exit(log.info(exit_message))
    except ServerTimeoutError as e:
        log.warning(e.message)
        exit(log.info(exit_message))


if __name__ == "__main__":
    welcome_string = '''Welcome to Net|CMDB
Starting core system with following parameters: \n{}
    '''
    brand_string = '''
###########################################
__  __ _____ _____ ____ __  __ ____  ____
| \ | | ____|_   _/ ___|  \/  |  _ \| __ ) 
|  \| |  _|   | || |   | |\/| | | | |  _ \ 
| |\  | |___  | || |___| |  | | |_| | |_) |
|_| \_|_____| |_| \____|_|  |_|____/|____/ 
   
###########################################                                        
    '''
    parameters, arguments = build_arg_parser()
    print(brand_string)
    print(welcome_string.format(parameters))
    sleep(0.1)  # prevent logger output

    if parameters.debug:
        global __DEBUG__
        __DEBUG__ = True
        log.setLevel(10)

    if parameters.start:
        main(arguments)
