from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObjectLink(CmdbDAO):

    COLLECTION = "objects.links"

    def __init__(self, partner_ids=[], **kwargs):
        self.partner_ids = partner_ids
        super(CmdbObjectLink, self).__init__(**kwargs)

    def get_partners(self):
        return self.partner_ids
