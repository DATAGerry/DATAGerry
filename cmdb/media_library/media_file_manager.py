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

    def get_media_file(self, file_name: str):
        try:
            result = self.fs_bucket.get_last_version(filename=file_name, metadata={'ref_to': 3170})
        except (MediaFileManagerGetError, Exception) as err:
            LOGGER.error(err)
            raise err
        return result.read()

    def get_all_media_files(self):
        media_file_list = []
        for file_name in self.fs_bucket.list():
            try:
                # media_file_list.append(self.fs_bucket.get_last_version(filename=file_name))
                new_file = {}
                grid_out = self.fs_bucket.get_last_version(filename=file_name)
                new_file['public_id'] = self.get_new_id(MediaFile.COLLECTION)
                new_file['name'] = grid_out.filename
                new_file['chunk_size'] = grid_out.chunk_size
                new_file['upload_date'] = grid_out.upload_date
                new_file['metadata'] = grid_out.metadata
                new_file['size'] = grid_out.length
                media_file_list.append(MediaFile(**new_file))
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
                media_file.metadata = FileMetadata(**metadata)
        except CMDBError as e:
            raise MediaFileManagerInsertError(e)
        return media_file

    def delete_media_file(self, file_name: str) -> bool:
        try:
            file_list = self.fs_bucket.find({"filename": file_name}, no_cursor_timeout=True)
            for grid_out in file_list:
                self.fs_bucket.delete(grid_out['_id'])
            return True
        except Exception:
            raise MediaFileManagerDeleteError(f'Could not delete job with ID: {file_name}')


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