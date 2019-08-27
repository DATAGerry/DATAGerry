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

from cmdb.framework.cmdb_collection import CmdbCollection, CmdbCollectionTemplate


class TestFrameworkCollection:

    @pytest.mark.parametrize('collection_instance_class', [
        CmdbCollection
    ])
    def test_init(self):
        pass


class TestFrameworkCollectionTemplate:

    @pytest.mark.parametrize('collection_template_instance_class', [
        CmdbCollectionTemplate
    ])
    def test_init(self, collection_template_instance_class):
        type_tuple_list = [CmdbCollectionTemplate.generate_type_tuple(1, 10)]
        right_init_params = {'public_id': 1, 'name': 'test', 'type_tuple_list': type_tuple_list}
        init_instance = CmdbCollectionTemplate(**right_init_params)
        assert isinstance(init_instance, collection_template_instance_class)

    def test_tuple_generation(self):
        assert (1, 10) == CmdbCollectionTemplate.generate_type_tuple(1, 10)
