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

from gridfs import GridFS

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError

from cmdb.media_library.media_file import MediaFile
from cmdb.media_library.media_file import FileMetadata

LOGGER = logging.getLogger(__name__)


class MediaFileManagement(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.dbm = database_manager
        self.fs_bucket = GridFS(self.dbm.get_connector().get_database(), MediaFile.COLLECTION)
        super().__init__(database_manager)

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def get_media_file(self, file_name: str, filter_metadata):
        try:
            result = self.fs_bucket.get_last_version(filename=file_name, **filter_metadata)
        except (MediaFileManagerGetError, Exception) as err:
            LOGGER.error(err)
            raise err
        return result

    def get_all_media_files(self, filter_metadata):
        media_file_list = []
        for grid_out in self.fs_bucket.find(filter=filter_metadata):
            try:
                media_file_list.append(MediaFile(**grid_out._file))
            except CMDBError:
                continue
        return media_file_list

    def insert_media_file(self, data, metadata) -> str:
        """
        Insert new MediaFile Object
        Args:
            data: init media_file
            metadata: a set of data that describes and gives information about other data.
        Returns:
            Filename of the new MediaFile in database
        """
        try:
            with self.fs_bucket.new_file(filename=data.filename) as media_file:
                media_file.write(data)
                media_file.public_id = self.get_new_id(MediaFile.COLLECTION)
                media_file.metadata = FileMetadata(**metadata).__dict__
        except CMDBError as e:
            raise MediaFileManagerInsertError(e)
        return media_file._id

    def delete_media_file(self, public_id) -> bool:
        """
        Delete MediaFile Object
        Args:
            public_id(int): init media_file
        Returns:
            bool: If deleted return true else false
        """
        try:
            file_id = self.fs_bucket.get_last_version(**{'public_id': public_id})._id
            self.fs_bucket.delete(file_id)
            return True
        except Exception:
            raise MediaFileManagerDeleteError(f'Could not delete file with ID: {file_id}')

    def exist_media_file(self, file_name: str, filter_metadata) -> bool:
        """
        Check is MediaFile Object exist
        Args:
            file_name(str): init media_file
            filter_metadata: Metadata as filter
        Returns:
            bool: If exist return true else false
        """
        return self.fs_bucket.exists(filename=file_name, **filter_metadata)


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