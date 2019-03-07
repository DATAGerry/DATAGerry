import pytest
from datetime import datetime
from cmdb.object_framework.cmdb_render import CmdbRender


@pytest.fixture
def object_instance():
    from cmdb.object_framework.cmdb_object import CmdbObject
    return CmdbObject(
        public_id=1,
        type_id=1,
        creation_time=datetime.utcnow(),
        author_id=0,
        active=True,
        fields=[
            {
                'name': 'text-1',
                'value': 'test_1'
            },
            {
                'name': 'text-2',
                'value': 'test_2'
            }
        ]
    )


@pytest.fixture
def type_instance():
    from cmdb.object_framework.cmdb_object_type import CmdbType
    return CmdbType(
        public_id=1,
        name='Test',
        active=True,
        author_id=0,
        creation_time=datetime.utcnow(),
        render_meta={
            'sections': [
                {
                    "tag": "h1",
                    "name": "text_fields",
                    "label": "Text Fields",
                    "fields": [
                        "text-1",
                        "text-2"
                    ],
                    "position": 1
                }
            ],
            'external': [
                {
                    "href": "http://example.org/{}/{}/",
                    "fields": [
                        "text-1",
                        "text-2",
                    ],
                    "label": "Internal link",
                    "icon": None,
                    "name": "internal_link"
                }
            ],
            "summary": [
                {
                    "label": "Summary",
                    "fields": [
                        "text-1",
                        "text-2"
                    ],
                    "name": "example_summary"
                }
            ]
        },
        fields=[
            {
                "input_type": "text",
                "label": "Basic Text Field",
                "className": "form-control",
                "name": "text-1",
                "subtype": "text"
            }, {
                "input_type": "text",
                "required": True,
                "label": "Full Text Field",
                "description": "example text field with all possible options",
                "placeholder": "example",
                "className": "form-control",
                "name": "text-2",
                "access": True,
                "subtype": "text",
                "maxlength": 120,
                "role": 1
            }
        ]
    )


def test_render_init(type_instance, object_instance):
    from cmdb.object_framework.cmdb_render import TypeInstanceError, ObjectInstanceError, WrongOutputFormat
    # test class type error handling
    with pytest.raises(TypeError):
        CmdbRender()
    with pytest.raises(TypeInstanceError):
        CmdbRender(type_instance=None, object_instance=object_instance)
    with pytest.raises(ObjectInstanceError):
        CmdbRender(type_instance=type_instance, object_instance=None)
    with pytest.raises(WrongOutputFormat):
        CmdbRender(type_instance=type_instance, object_instance=object_instance, format_=None)
    # test property sets
    render_instance = CmdbRender(type_instance=type_instance, object_instance=object_instance)
    assert render_instance.object_instance == object_instance
    assert render_instance.type_instance == type_instance


def test_meta_functions(type_instance, object_instance):
    from cmdb.object_framework.cmdb_object_type import _ExternalLink, _Summary
    render_instance = CmdbRender(type_instance=type_instance, object_instance=object_instance)
    for ext in render_instance.get_externals():
        assert type(ext) == _ExternalLink
    for sum in render_instance.get_summaries():
        assert type(sum) == _Summary


def test_output(type_instance, object_instance):
    render_instance = CmdbRender(type_instance=type_instance, object_instance=object_instance)
    print(render_instance.output())
