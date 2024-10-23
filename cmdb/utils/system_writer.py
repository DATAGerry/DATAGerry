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
"""
Configuration module for settings in file format and in the database
"""
import logging

from cmdb.database.mongo_database_manager import MongoDatabaseManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 SystemWriter - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class SystemWriter:
    """
    Superclass for general write permissions
    Watch out with the collection constants. In Mongo the Settings Collection is pre-defined
    """
    COLLECTION = 'settings.*'

    def __init__(self, dbm: MongoDatabaseManager):
        """
        Default constructor
        Args:
            writer: Database managers instance
        """
        self.dbm = dbm


    def write(self, _id: str, data: dict):
        """
        write data into database
        it' the only module where no public_id is used
        Args:
            _id: database entry identifier
            data: data to write

        Returns:
            acknowledgment: based on database managers
        """
        raise NotImplementedError


    def verify(self, _id: int, data: dict) -> bool:
        """
        Checks if configuration entry exists
        Returns: True if exists - else False

        """
        raise NotImplementedError


#CLASS-FIX
class SystemSettingsWriter(SystemWriter):
    """TODO: document"""
    COLLECTION = 'settings.conf'

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Init database writer with MongoDatabaseManager
        Args:
            database_manager: Database connection
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(dbm)


    def write(self, _id: str, data: dict):
        """
        Write new settings in database
        """
        return self.dbm.update(collection=self.COLLECTION, criteria={'_id': _id}, data=data, upsert=True)


    def verify(self, _id: str, data: dict = None) -> bool:
        """
        Checks if setting exists and has data
        Args:
            _id: settings entry id
            data: verify if has same data

        Returns:
            bool if entry exists and has data (compare), otherwise false
        TODO: REFACTOR
        """
        try:
            verify_document = self.dbm.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except Exception:
            #ERROR-FIX
            return False

        if verify_document != data and data is not None:
            return False

        return True
