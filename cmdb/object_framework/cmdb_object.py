from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObject(CmdbDAO):
    """
    The CMDB object is the basic data wrapper for storing
    and holding the pure objects within the CMDB.
    """
    COLLECTION = 'objects.data'
    REQUIRED_INIT_KEYS = [
        'type_id',
        'status',
        'version',
        'creation_time',
        'creator_id',
        'last_editor_id',
        'last_edit_time',
        'active',
        'views',
        'fields',
        'logs'
    ]

    def __init__(self, type_id, status, version, creation_time, creator_id,
                 last_editor_id, last_edit_time, active, views, fields, logs, **kwargs):
        """
        init of object
        :param type_id: public type id which implements the object
        :param status: current status of object
        :param version: current version of object
        :param creation_time: date of object creation
        :param creator_id: public id of creation user
        :param last_editor_id: public id of last author which edits the object
        :param last_edit_time: last date of editing
        :param active: object activation status
        :param views: numbers of views
        :param fields: data inside fields
        :param logs: object log
        :param kwargs: additional data
        """
        self.type_id = type_id
        self.status = status
        self.version = version
        self.creation_time = creation_time
        self.creator_id = creator_id
        self.last_editor_id = last_editor_id
        self.last_edit_time = last_edit_time
        self.active = active
        self.views = int(views)
        self.fields = fields
        self.logs = logs
        super(CmdbObject, self).__init__(**kwargs)

    def get_type_id(self):
        return self.type_id

    def get_links(self):
        if self.links:
            return self.links
        else:
            None

    def update_view_counter(self):
        self.views += 1
        return self.views

    def get_all_fields(self):
        """
        get all fields with key value pair
        :return: all fields
        """
        return self.fields

    def get_value(self, field):
        """
        get value of an fields
        :param field: field_name
        :return: value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            else:
                continue
        return ""

