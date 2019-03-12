from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObjectLink(CmdbDAO):
    COLLECTION = "objects.links"
    REQUIRED_INIT_KEYS = [
        'partner_1',
        'partner_2',
    ]

    def __init__(self, partner_1: int, partner_2: int, **kwargs):
        self.partner_1 = partner_1
        self.partner_2 = partner_2
        super(CmdbObjectLink, self).__init__(**kwargs)

    def get_partner_1(self):
        return self.partner_1

    def get_partner_2(self):
        return self.partner_2

    def get_partners(self):
        return self.get_partner_1(), self.get_partner_2()
