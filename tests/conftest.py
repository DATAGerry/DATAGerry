
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
"""TODO: document"""
import logging
from datetime import datetime
import pytest

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.users_manager import UsersManager

from cmdb.security.key.generator import KeyGenerator
from cmdb.models.user_management_constants import __FIXED_GROUPS__
from cmdb.models.user_model.user import UserModel

from cmdb.errors.database import DatabaseNotExists
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
def pytest_addoption(parser):
    """Adds command line options"""
    parser.addoption(
        '--mongodb-host',
        action='store',
        default='localhost',
        help='Host of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-port',
        action='store',
        default=27017,
        help='Port of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-database',
        action='store',
        default='cmdb-test',
        help='Database of mongodb test instance'
    )


pytest_plugins = [
    'tests.fixtures.fixture_database',
    'tests.fixtures.fixture_management',
    'tests.fixtures.fixture_rest_api'
]


@pytest.fixture(scope="session", autouse=True)
def preset_database(database_manager: MongoDatabaseManager, database_name: str):
    """TODO: document"""
    try:
        database_manager.drop_database(database_name)
    except DatabaseNotExists:
        pass

    kg = KeyGenerator(database_manager)
    kg.generate_rsa_keypair()
    kg.generate_symmetric_aes_key()

    groups_manager = GroupsManager(database_manager)
    users_manager = UsersManager(database_manager)
    security_manager = SecurityManager(database_manager)

    for group in __FIXED_GROUPS__:
        groups_manager.insert_group(group)

    admin_name = 'admin'
    admin_pass = 'admin'

    admin_user = UserModel(
        public_id=1,
        user_name=admin_name,
        active=True,
        api_level = 2,
        group_id=__FIXED_GROUPS__[0].public_id,
        registration_time=datetime.now(),
        password=security_manager.generate_hmac(admin_pass),
    )

    users_manager.insert_user(admin_user)
