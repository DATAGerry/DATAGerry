from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObject(CmdbDAO):
    """

    """
    # pylint: disable=too-many-instance-attributes

    COLLECTION = 'objects.data'
    REQUIRED_INIT_KEYS = ['_id', 'public_id', 'type_id', 'status',
                          'version', 'creation_time', 'creator_id',
                          'last_editor_id', 'last_edit_time', 'active',
                          'views', 'fields', 'logs']

    def __init__(self, *args, **kwargs):
        self.public_id = None
        self.type_id = None
        self.status = None
        self.version = None
        self.creation_time = None
        self.creator_id = None
        self.last_editor_id = None
        self.last_edit_time = None
        self.views = None
        self.fields = None
        self.logs = None
        super(CmdbObject, self).__init__(*args, **kwargs)

    def get_all_values(self):
        return self.fields

    def get_value(self, field):
        el = [x for x in self.fields if x['name'] == field][0]
        if el:
            return el['value']

