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

import logging

from cmdb.data_storage import DatabaseManagerMongo, NoDocumentFound
from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.exportd.exportd_job.exportd_job import ExportdJob
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)


class ExportdJobManagement(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.dbm = database_manager
        super().__init__(database_manager)

    def get_job(self, public_id: int) -> ExportdJob:
        try:
            result = self.dbm.find_one(collection=ExportdJob.COLLECTION, public_id=public_id)
        except Exception as err:
            LOGGER.error(err)
            raise err
        return ExportdJob(**result)

    def get_all_jobs(self):
        job_list = []
        for founded_job in self.dbm.find_all(collection=ExportdJob.COLLECTION):
            try:
                job_list.append(ExportdJob(**founded_job))
            except CMDBError:
                continue
        return job_list

    def get_job_by_name(self, name):
        formatted_filter = {'name': name}
        try:
            return self.dbm.find_one_by(collection=ExportdJob.COLLECTION, filter=formatted_filter)
        except NoDocumentFound as err:
            LOGGER.error(err)
            raise err

    def insert_job(self, job: ExportdJob) -> int:
        try:
            return self.dbm.insert(collection=ExportdJob.COLLECTION, data=job.to_database())
        except (CMDBError, Exception):
            raise ExportdJobManagerInsertError(f'Could not insert {job.get_name()}')

    def update_job(self, public_id, update_params: dict):
        try:
            return self.dbm.update(collection=ExportdJob.COLLECTION, public_id=public_id, data=update_params)
        except (CMDBError, Exception):
            raise ExportdJobManagerUpdateError(f'Could not update job with ID: {public_id}')

    def delete_job(self, public_id: int) -> bool:
        try:
            return self._delete(collection=ExportdJob.COLLECTION, public_id=public_id)
        except Exception:
            raise ExportdJobManagerDeleteError(f'Could not delete job with ID: {public_id}')


class ExportdJobManagerGetError(ManagerGetError):

    def __init__(self, err):
        super(ExportdJobManagerGetError, self).__init__(err)


class ExportdJobManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super(ExportdJobManagerInsertError, self).__init__(err)


class ExportdJobManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super(ExportdJobManagerUpdateError, self).__init__(err)


class ExportdJobManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super(ExportdJobManagerDeleteError, self).__init__(err)


def get_exoportd_job_manager():
    from cmdb.data_storage import get_pre_init_database
    db_man = get_pre_init_database()
    return ExportdJobManagement(
        database_manager=db_man
    )


exportd_job_manager = get_exoportd_job_manager()
