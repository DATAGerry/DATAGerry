"""
Experimental module for the automated import of test data
"""
import logging
from .system_reader import SystemConfigReader
import os

LOGGER = logging.getLogger(__name__)


def list_example_files(extension: str = 'json', path: str = None) -> list:
    """
    get list of examples files
    Args:
        extension: file extension
        path: default path

    Returns:
        list of example file names without path
    """
    if path:
        working_path = path
    else:
        working_path = SystemConfigReader.DEFAULT_CONFIG_LOCATION + 'example/'
    json_files = [pos_json for pos_json in os.listdir(working_path) if pos_json.endswith('.' + extension)]
    LOGGER.debug(json_files)
    return json_files


def import_example_data(file_list: list, path: str = None) -> []:
    """
    Import a list of files into the database
    The name of the file will be the collection name
    Args:
        file_list: list of files without path
        path: directory path

    Returns:
        import results
    """
    from cmdb.data_storage import get_pre_init_database
    dbm = get_pre_init_database()
    import json
    success_imports = []
    failed_imports = []
    if path:
        working_path = path
    else:
        working_path = SystemConfigReader.DEFAULT_CONFIG_LOCATION + 'example/'
    for import_file in file_list:
        f = open(working_path + import_file, 'r')
        r = json.loads(f.read())
        LOGGER.debug("IMPORT FILE {}".format(import_file[:-5]))
        LOGGER.debug("DATA TYPE {}".format(type(r)))
        LOGGER.debug("DATABASE CONNECTED: {}".format(dbm.database_connector.is_connected()))
        ack = dbm._import(import_file[:-5], r)
        if ack:
            success_imports.append(import_file)
        else:
            failed_imports.append(import_file)
    return success_imports, failed_imports
