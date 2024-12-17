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

from cmdb.manager.rights_manager import RightsManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.group_model.group import UserGroupModel
from cmdb.models.right_model.all_rights import __all__ as rights
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
@pytest.fixture(scope="session", name="rights_manager")
def fixture_rights_manager():
    """TODO: document"""
    return RightsManager(rights)


@pytest.fixture(scope="session", name="full_access_group")
def fixture_full_access_group(rights_manager: RightsManager):
    "TODO: document"
    return UserGroupModel(public_id=1, name='full', label='Full', rights=[rights_manager.get_right('base.*')])


@pytest.fixture(scope="session", name="none_access_group")
def fixture_none_access_group():
    """TODO: document"""
    return UserGroupModel(public_id=2, name='none', label='None')


@pytest.fixture(scope="session", name="full_access_user")
def fixture_full_access_user(full_access_group: UserGroupModel):
    "TODO: document"
    registration_time = datetime.now()
    return UserModel(public_id=1,
                     user_name='full-access-user',
                     active=True,
                     group_id=full_access_group.public_id,
                     registration_time=registration_time)


@pytest.fixture(scope="session", name="none_access_user")
def fixture_none_access_user(none_access_group: UserGroupModel):
    "TODO: document"
    registration_time = datetime.now()
    return UserModel(public_id=2,
                     user_name='none-access-user',
                     active=True,
                     group_id=none_access_group.public_id,
                     registration_time=registration_time)
