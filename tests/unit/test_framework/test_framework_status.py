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

from cmdb.framework.cmdb_dao import RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_status import CmdbStatus


class TestFrameworkStatus:

    @pytest.mark.parametrize('status_instance_class', [
        CmdbStatus
    ])
    def test_init_function(self, status_instance_class):
        right_init_params = {'public_id': 1, 'name': 'test', 'label': 'Test', 'short': 'T', 'events': []}
        init_instance = CmdbStatus(**right_init_params)
        assert isinstance(init_instance, status_instance_class)

        wrong_init_params = {'public_id': 1, 'label': 'Test', 'short': 'T', 'events': []}
        with pytest.raises(RequiredInitKeyNotFoundError):
            CmdbStatus(**wrong_init_params)

    def test_short_truncat(self):
        short_init_params = {'public_id': 1, 'name': 'test'}
        short_instance = CmdbStatus(**short_init_params)
        assert short_instance.get_short() == 'TEST'
        short_init_params['name'] = 'test2test'
        short_instance2 = CmdbStatus(**short_init_params)
        assert short_instance2.get_short() == 'TEST2'
        short_init_params['short'] = 't'
        short_instance3 = CmdbStatus(**short_init_params)
        assert short_instance3.get_short() == 'T'

    def test_getters(self):
        right_init_params = {'public_id': 1, 'name': 'test', 'label': 'Test', 'short': 'T', 'events': []}
        getter_instance = CmdbStatus(**right_init_params)
        assert getter_instance.get_public_id() == 1
        assert getter_instance.get_name() == 'test'
        assert getter_instance.get_label() == 'Test'
        assert getter_instance.get_short() == 'T'
        assert len(getter_instance.get_events()) == 0