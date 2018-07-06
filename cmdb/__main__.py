#!/usr/bin/env python
"""
Net|CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/NetCMDB/blob/master/LICENSE>.
"""
from gevent import monkey

monkey.patch_all()
from cmdb.application_utils.logger import CMDB_LOGGER


def build_arg_parser():
    from optparse import OptionParser
    from cmdb import __version__, __title__, __DEBUG__
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


def main():
    from multiprocessing import Process, Queue
    from cmdb.communication_interface import HTTPServer, application
    from cmdb.data_storage import init_database
    from cmdb.data_storage.database_connection import ServerTimeoutError
    from cmdb.application_utils import get_system_config_reader

    exit_message = "STOPPING cmdb!"

    database_manager = init_database()
    try:
        database_manager.database_connector.connect()

    except OSError as e:
        CMDB_LOGGER.warning(e.errno)
        exit(CMDB_LOGGER.info(exit_message))
    except ServerTimeoutError as e:
        CMDB_LOGGER.warning(e.message)
        exit(CMDB_LOGGER.info(exit_message))
    finally:
        database_manager.database_connector.disconnect()
    server_queue = Queue()
    web_server_options = get_system_config_reader().get_all_values_from_section('WebServer')
    http_process = Process(
        target=HTTPServer(application, web_server_options).run,
        args=(server_queue,)
    )
    http_process.start()
    if server_queue.get():
        CMDB_LOGGER.info("CMDB successfully started")
    http_process.join()
    CMDB_LOGGER.info("CMDB stopped")


if __name__ == "__main__":
    from time import sleep

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
    CMDB_LOGGER.info("STARTING CMDB...")

    if parameters.debug:
        global __DEBUG__
        __DEBUG__ = True
        # log.setLevel(10)

    if parameters.start:
        main()
