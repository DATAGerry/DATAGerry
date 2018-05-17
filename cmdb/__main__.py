"""
Net|CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/markheumueller/NetCMDB/blob/master/LICENSE>.
"""
from cmdb.object_framework import CmdbStatus
from cmdb.data_storage import DATABASE_MANAGER


if __name__ == "__main__":

    status = DATABASE_MANAGER.find_one(collection=CmdbStatus.COLLECTION, public_id=2)
    print(CmdbStatus(**status))
