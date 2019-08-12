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

from datetime import datetime

from cmdb.framework.cmdb_object_type import CmdbType
from cmdb.framework.cmdb_errors import TypeAlreadyExists, TypeNotFoundError


@pytest.mark.usefixtures("mongodb")
@pytest.fixture
def object_manager(mongodb):
    from cmdb.data_storage.database_manager import DatabaseManagerMongo

    from cmdb.framework.cmdb_object_manager import CmdbObjectManager
    return CmdbObjectManager(
        database_manager=DatabaseManagerMongo(connector=mongodb)
    )


@pytest.mark.parametrize('type_instance_class', [
    CmdbType
])
def test_cmdb_object_type_init(type_instance_class):
    from cmdb.framework.cmdb_dao import RequiredInitKeyNotFoundError
    with pytest.raises(RequiredInitKeyNotFoundError):
        CmdbType(name='example', active=True, author_id=1, creation_time=datetime.utcnow(),
                 render_meta={}, fields=[])
    type_instance = CmdbType(name='example', active=True, author_id=1, creation_time=datetime.utcnow(),
                             render_meta={}, fields=[], public_id=1)
    assert isinstance(type_instance, type_instance_class)


def test_cmdb_object_type_calls():
    _render_data = {
        'summary': [],
        'external': [],
        'sections': []
    }
    type_instance = CmdbType(name='example', active=True, author_id=1, creation_time=datetime.utcnow(),
                             render_meta=_render_data, fields=[], public_id=1)

    assert type_instance.has_externals() is False
    assert type_instance.has_summaries() is False
    assert type_instance.has_sections() is False


@pytest.mark.usefixtures("object_manager")
class TestFrameworkType:
    """Test the type functions at runtime"""

    def test_get_all(self, object_manager):
        assert len(object_manager.get_all_types()) == 1

    def test_get_type(self, object_manager):
        type_instance_1 = object_manager.get_type(public_id=1)
        assert type_instance_1.get_name() == 'example'
        with pytest.raises(TypeNotFoundError):
            object_manager.get_type(public_id=2)

    def test_add_type(self, object_manager):
        _render_data = {
            'summary': [],
            'external': [],
            'sections': []
        }
        type_instance_new_1 = CmdbType(name='example2', active=True, author_id=1, creation_time=datetime.utcnow(),
                                       render_meta=_render_data, fields=[], public_id=2)
        # CmdbObjectType insert
        ack = object_manager.insert_type(type_instance_new_1)
        assert ack == 2
        type_instance_new_2 = object_manager.get_type(public_id=2)
        assert type_instance_new_2.get_name() == 'example2'

        # dict insert
        type_instance_new_3 = CmdbType(name='example3', active=True, author_id=1, creation_time=datetime.utcnow(),
                                       render_meta=_render_data, fields=[], public_id=3)
        object_manager.insert_type(type_instance_new_3.__dict__)
        type_instance_new_3 = object_manager.get_type(public_id=3)
        assert type_instance_new_3.get_name() == 'example3'

        # insert error test
        type_instance_new_4 = CmdbType(name='example3', active=True, author_id=1, creation_time=datetime.utcnow(),
                                       render_meta=_render_data, fields=[],
                                       public_id=type_instance_new_3.get_public_id())
        with pytest.raises(TypeAlreadyExists):
            object_manager.insert_type(type_instance_new_4)

    def test_update_type(self, object_manager):
        _render_data = {
            'summary': [],
            'external': [],
            'sections': []
        }
        type_instance_update_1 = CmdbType(name='exampleX', active=True, author_id=1, creation_time=datetime.utcnow(),
                                          render_meta=_render_data, fields=[], public_id=1)
        object_manager.update_type(type_instance_update_1)
        type_get_instance = object_manager.get_type(public_id=1)
        assert type_get_instance.get_name() == type_instance_update_1.get_name()

    def test_delete_type(self, object_manager):
        object_manager.delete_type(public_id=1)
        assert len(object_manager.get_all_types()) == 0
