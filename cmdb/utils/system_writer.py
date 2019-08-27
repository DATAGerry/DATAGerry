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

"""
Configuration module for settings in file format and in the database
"""
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.data_storage.database_manager import NoDocumentFound
from cmdb.utils.error import CMDBError

import logging
LOGGER = logging.getLogger(__name__)


class SystemWriter:
    """
    Superclass for general write permissions
    Watch out with the collection constants. In Mongo the Settings Collection is pre-defined
    """

    COLLECTION = 'settings.*'

    def __init__(self, writer: DatabaseManagerMongo):
        """
        Default constructor
        Args:
            writer: Database manager instance
        """
        self.writer = writer

    def write(self, _id: str, data: dict) -> str:
        """
        write data into database
        it' the only module where no public_id is used
        Args:
            _id: database entry identifier
            data: data to write

        Returns:
            acknowledgment: based on database manager
        """
        raise NotImplementedError

    def update(self, _id: str or int, data: dict) -> str:
        """
        update entry in database
        Args:
            _id: database entry identifier
            data: data to update

        Returns:
            acknowledgment: based on database manager
        """
        raise NotImplementedError

    def verify(self, _id: int, data: dict) -> bool:
        """
        Checks if configuration entry exists
        Returns: True if exists - else False

        """
        raise NotImplementedError


class SystemSettingsWriter(SystemWriter):
    """

    """
    COLLECTION = 'settings.conf'

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Init database writer with DatabaseManagerMongo
        Args:
            database_manager: Database connection
        """
        super(SystemSettingsWriter, self).__init__(database_manager)

    def write(self, _id: str, data: dict) -> str:
        """
        Write new settings in database
        Args:
            _id: new settings_id
            data: data to write
        Returns:
            acknowledgment: based on database manager
        TODO: auto find _id

        """
        try:
            writing_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except NoDocumentFound:
            self.writer.insert_with_internal(collection=self.COLLECTION, _id=_id, data=data)
            writing_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})

        writing_document.update(data)
        ack = self.writer.update_with_internal(
            collection=self.COLLECTION,
            _id=writing_document['_id'],
            data=writing_document
        )
        return ack

    def update(self, _id: str or int, data: dict) -> str:
        """
        Update existing setting in database
        Args:
            _id: settings entry id
            data: data to update

        Returns:
            acknowledgment: based on database manager

        TODO: Error handling
        """
        from cmdb.data_storage.database_utils import convert_form_data
        new_data = convert_form_data(data)
        current_setting = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        current_setting.update(new_data)
        ack = self.writer.update_with_internal(collection=self.COLLECTION, _id=_id, data=current_setting)
        return ack

    def verify(self, _id: str, data: dict = None) -> bool:
        """
        Checks if setting exists and has data
        Args:
            _id: settings entry id
            data: verify if has same data

        Returns:
            bool if entry exists and has data (compare), otherwise false
        """
        try:
            verify_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except (NoEntryFoundError, CMDBError):
            return False

        if verify_document != data and data is not None:
            return False
        return True


class NoEntryFoundError(CMDBError):
    """
    Error if no entry exists
    """

    def __init__(self, _id):
        super().__init__()
        self.message = "Entry with the id {} was not found".format(_id)
