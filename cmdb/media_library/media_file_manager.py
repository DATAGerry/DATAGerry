# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
import logging

from datetime import datetime, timezone
from gridfs.grid_file import GridOutCursor, GridOut

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.database.database_gridfs import DatabaseGridFS
from cmdb.media_library.media_file import MediaFile
from cmdb.media_library.media_file import FileMetadata
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.cmdb_errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class MediaFileManager(CmdbManagerBase):
    """TODO: document"""
    def __init__(self, database_manager: DatabaseManagerMongo, database: str = None):
        if database:
            database_manager.connector.set_database(database)

        self.dbm = database_manager
        self.fs = DatabaseGridFS(self.dbm.connector.database, MediaFile.COLLECTION)

        super().__init__(database_manager)


    def get_new_id(self, collection: str) -> int:
        """TODO: document"""
        return self.dbm.get_next_public_id(collection)


    def get_file(self, metadata: dict, blob: bool = False) -> GridOut:
        """TODO: document"""
        try:
            result = self.fs.get_last_version(**metadata)
        except (MediaFileManagerGetError, Exception) as err:
            LOGGER.error(err)
            raise MediaFileManagerGetError(err=err) from err

        return result.read() if blob else result._file


    def get_many(self, metadata, **params: dict):
        """TODO: document"""
        try:
            results = []
            records_total = self.fs.find(filter=metadata).retrieved

            #pymongo4.6 records_total = self.fs.find(filter=metadata).count()
            iterator: GridOutCursor = self.fs.find(filter=metadata, **params)
            for grid in iterator:
                results.append(MediaFile.to_json(MediaFile(**grid._file)))
        except (CMDBError, MediaFileManagerGetError) as err:
            raise MediaFileManagerGetError(err) from err

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
        except CMDBError as err:
            raise MediaFileManagerInsertError(err) from err

        return media_file._file


    def updata_file(self, data):
        """TODO: document"""
        try:
            data['uploadDate'] = datetime.now(timezone.utc)
            self._update(collection='media.libary.files', public_id=data['public_id'], data=data)
        except Exception as err:
            raise MediaFileManagerUpdateError(err) from err
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
        except Exception as exc:
            raise MediaFileManagerDeleteError(f'Could not delete file with ID: {file_id}') from exc

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
    """TODO: document"""
    def __init__(self, result, total: int = None):
        self.result = result
        self.count = len(result)
        self.total = total or 0


class MediaFileManagerGetError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err)


class MediaFileManagerInsertError(ManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err)


class MediaFileManagerUpdateError(ManagerUpdateError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err)


class MediaFileManagerDeleteError(ManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err)
