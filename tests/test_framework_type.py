import pytest

from datetime import datetime
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFoundError
from cmdb.object_framework.cmdb_object_type import CmdbType
from cmdb.object_framework.cmdb_object_manager import TypeNotFoundError, TypeAlreadyExists


@pytest.mark.usefixtures("mongodb")
@pytest.fixture
def object_manager(mongodb):
    from cmdb.data_storage.database_manager import DatabaseManagerMongo

    from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
    return CmdbObjectManager(
        database_manager=DatabaseManagerMongo(connector=mongodb)
    )


@pytest.mark.parametrize('type_instance_class', [
    CmdbType
])
def test_cmdb_object_type_init(type_instance_class):
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


@pytest.fixture
def type_rest_client():
    from cmdb.interface.rest_api.type_routes import type_routes
    return type_routes.test_client()


@pytest.mark.usefixtures("type_rest_client")
class TestTypeRestCalls:

    def test_get_routes(self, type_rest_client):
        rv = type_rest_client
        print(rv)