from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObject(CmdbDAO):
    """The CMDB object is the basic data wrapper for storing and holding the pure objects within the CMDB.
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
        """init of object

        Args:
            type_id: public type id which implements the object
            status: current status of object
            version: current version of object
            creation_time: date of object creation
            creator_id: public id of creation user
            last_editor_id: public id of last author which edits the object
            last_edit_time: last date of editing
            active: object activation status
            views: numbers of views
            fields: data inside fields
            logs: object log
            **kwargs: additional data
        """
        self.type_id = type_id
        self.status = status
        self.version = version
        self.creation_time = creation_time
        self.creator_id = creator_id
        self.last_editor_id = last_editor_id
        self.last_edit_time = last_edit_time
        self.active = active
        self.views = views
        self.fields = fields
        self.logs = logs
        super(CmdbObject, self).__init__(**kwargs)

    def get_type_id(self) -> int:
        """get type if of this object

        Returns:
            int: public id of type

        """
        return self.type_id

    def get_links(self) -> list:
        """get list of all linked objects

        Returns:
            list: list of objects public ids
            None: if none exists

        """
        if self.links:
            return self.links
        else:
            None

    def update_view_counter(self) -> int:
        """update the number of times this object was viewd

        Returns:
            int: number of views

        """
        self.views += 1
        return self.views

    def get_all_fields(self):
        """ get all fields with key value pair

        Returns:
            all fields

        """

        return self.fields

    def get_value(self, field):
        """get value of an field

        Args:
            field: field_name

        Returns:
            value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            else:
                continue
        return None
