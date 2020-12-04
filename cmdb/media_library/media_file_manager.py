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

from datetime import datetime

from cmdb.database.database_manager import DatabaseManagerMongo, DatabaseGridFS
from gridfs.grid_file import GridOutCursor, GridOut

from cmdb.media_library.media_file import MediaFile
from cmdb.media_library.media_file import FileMetadata

from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)


class MediaFileManagement(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.dbm = database_manager
        self.fs = DatabaseGridFS(self.dbm.get_connector().database, MediaFile.COLLECTION)
        super().__init__(database_manager)

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def get_file(self, metadata: dict, blob: bool = False) -> GridOut:
        try:
            result = self.fs.get_last_version(**metadata)
        except (MediaFileManagerGetError, Exception) as err:
            LOGGER.error(err)
            raise MediaFileManagerGetError(err=err)
        return result.read() if blob else result._file

    def get_many(self, metadata, **params: dict):
        try:
            results = []
            records_total = self.fs.find(filter=metadata).count()
            iterator: GridOutCursor = self.fs.find(filter=metadata, **params)
            for grid in iterator:
                results.append(MediaFile.to_json(MediaFile(**grid._file)))
        except (CMDBError, MediaFileManagerGetError) as err:
            raise MediaFileManagerGetError(err)
        return GridFsResponse(results, records_total)

    def insert_file(self, data, metadata):
        """
        Insert new MediaFile Object
        Args:
            data: init media_file
            metadata: a set of data that describes and gives information about other data.
        Returns:
            New MediaFile in database
        """
        try:
            with self.fs.new_file(filename=data.filename) as media_file:
                media_file.write(data)
                media_file.public_id = self.get_new_id(MediaFile.COLLECTION)
                media_file.metadata = FileMetadata(**metadata).__dict__
        except CMDBError as e:
            raise MediaFileManagerInsertError(e)

        return media_file._file

    def updata_file(self, data):
        try:
            data['uploadDate'] = datetime.utcnow()
            self._update(collection='media.libary.files', public_id=data['public_id'], data=data)
        except Exception as err:
            raise MediaFileManagerUpdateError(err)
        return data

    def delete_file(self, public_id) -> bool:
        """
        Delete MediaFile Object
        Args:
            public_id(int): init media_file
        Returns:
            bool: If deleted return true else false
        """
        try:
            file_id = self.fs.get_last_version(**{'public_id': public_id})._id
            self.fs.delete(file_id)
        except Exception:
            raise MediaFileManagerDeleteError(f'Could not delete file with ID: {file_id}')

        return True

    def exist_file(self, filter_metadata) -> bool:
        """
        Check is MediaFile Object exist
        Args:
            filter_metadata: Metadata as filter
        Returns:
            bool: If exist return true else false
        """
        return self.fs.exists(**filter_metadata)


class GridFsResponse:

    def __init__(self, result, total: int = None):
        self.result = result
        self.count = len(result)
        self.total = total or 0


class MediaFileManagerGetError(ManagerGetError):

    def __init__(self, err):
        super(MediaFileManagerGetError, self).__init__(err)


class MediaFileManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super(MediaFileManagerInsertError, self).__init__(err)


class MediaFileManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super(MediaFileManagerUpdateError, self).__init__(err)


class MediaFileManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super(MediaFileManagerDeleteError, self).__init__(err)