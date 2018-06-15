#!/usr/bin/env python
"""
Net|CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/NetCMDB/blob/master/LICENSE>.
"""
from gevent import monkey

monkey.patch_all()

from cmdb import __version__, __title__, __DEBUG__
from optparse import OptionParser
from time import sleep
from cmdb.application_utils.logger import create_module_logger

logger = create_module_logger(__name__)


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


    from cmdb.communication_interface import HTTPServer, application
    from cmdb.data_storage import init_database
    from cmdb.data_storage.database_connection import ServerTimeoutError
    from cmdb.plugins import plugin_manager

    database_manager = init_database()
    try:
        database_manager.database_connector.connect()

        from cmdb.application_utils import get_system_config_reader
        web_server_options = get_system_config_reader().get_all_values_from_section('WebServer')
        HTTPServer(
            application, web_server_options
        ).run()

        #plugin_manager.load_plugins()

    except OSError as e:
        logger.warning(e.errno)
        exit(logger.info(exit_message))
    except ServerTimeoutError as e:
        logger.warning(e.message)
        exit(logger.info(exit_message))
    finally:
        database_manager.database_connector.disconnect()


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
    logger.info("STARTING CMDB...")
    if parameters.debug:
        global __DEBUG__
        __DEBUG__ = True
        #log.setLevel(10)

    if parameters.start:
        main(arguments)
