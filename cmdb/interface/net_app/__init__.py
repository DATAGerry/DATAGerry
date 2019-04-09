"""
Init module for rest routes
"""
import logging
from flask_cors import CORS

from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.user_management.user_manager import UserManagement
from cmdb.utils import SecurityManager, SystemSettingsReader, SystemSettingsWriter
from cmdb.utils.system_reader import SystemConfigReader

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
app = BaseCmdbApp(__name__)
CORS(app)
system_config_reader = SystemConfigReader()


def create_app(event_queue):
    import cmdb

    if cmdb.__MODE__ == 'DEBUG':
        app.config.from_object(app_config['rest_development'])
        LOGGER.info('NetAPP starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('NetAPP starting with config mode {}'.format(app.config.get("ENV")))

    return app



