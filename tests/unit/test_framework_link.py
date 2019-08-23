# dataGerry - OpenSource Enterprise CMDB
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
from cmdb.framework.cmdb_link import CmdbLink


class TestFrameworkLink:

    @pytest.mark.parametrize('link_instance_class', [
        CmdbLink
    ])
    def test_init_function(self, link_instance_class):
        right_init_params = {'public_id': 1, 'primary': 1, 'secondary': 2}
        init_instance = CmdbLink(**right_init_params)
        assert isinstance(init_instance, link_instance_class)

        wrong_init_params = {}
        with pytest.raises(RequiredInitKeyNotFoundError):
            CmdbLink(**wrong_init_params)

        double_id_params = {'public_id': 1, 'primary': 1, 'secondary': 1}
        with pytest.raises(ValueError):
            CmdbLink(**double_id_params)

    def test_getters(self):
        right_init_params = {'public_id': 1, 'primary': 1, 'secondary': 2}
        getter_instance = CmdbLink(**right_init_params)
        assert 1 == getter_instance.get_public_id()
        assert 1 == getter_instance.get_primary()
        assert 2 == getter_instance.get_secondary()
        assert 1, 2 == getter_instance.get_partners()
