# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest
from _pytest.config import Config

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.utils.system_config import SystemConfigReader

pytest_plugins = 'tests/pytest_plugins/pytest_config'


@pytest.fixture(scope="session")
def config_reader(pytestconfig: Config) -> SystemConfigReader:
    config_path = pytestconfig.getoption('config-path', '../../etc/cmdb_test.conf')
    return SystemConfigReader.from_full_path(config_path)


@pytest.fixture(scope="session")
def database_manager(config_reader) -> DatabaseManagerMongo:
    database_options = config_reader.get_all_values_from_section('Database')
    return DatabaseManagerMongo(**database_options)


@pytest.fixture(scope="session")
def object_manager(database_manager) -> CmdbObjectManager:
    return CmdbObjectManager(database_manager=database_manager)


@pytest.fixture(scope="class")
def object_manager_class(request, object_manager):
    request.cls.object_manager = object_manager


@pytest.fixture(scope="class")
def database_manager_class(request, database_manager):
    request.cls.database_manager = database_manager


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    import cmdb
    cmdb.__MODE__ = 'TESTING'
