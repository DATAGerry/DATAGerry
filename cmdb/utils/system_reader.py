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
Collection of system readers which loads configuration files and settings
"""
from typing import Any, Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb.errors.database import NoDocumentFound
from cmdb.errors.system_config import SectionError
# -------------------------------------------------------------------------------------------------------------------- #

class SystemReader:
    """
    Reader super class
    """

    def get_value(self, name: str, section: str) -> Any:
        """
        get specific value from a section
        Args:
            name: key name of value
            section: section identifier
        Returns:
            value
        """
        raise NotImplementedError


    def get_sections(self) -> list[str]:
        """
        get all sections from config
        Returns:
            list of config names
        """
        raise NotImplementedError


    def get_all_values_from_section(self, section: str) -> dict:
        """
        get list of all values in section
        Args:
            section: section key
        Returns:
            key/value list of all values inside a section
        """
        raise NotImplementedError



class SystemSettingsReader(SystemReader):
    """
    Settings reader loads settings from database
    """
    COLLECTION = 'settings.conf'

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        init system settings reader
        Args:
            database_manager: database managers
        """
        if database:
            dbm.connector.set_database(database)

        self.dbm = dbm

        super().__init__()


    def get_value(self, name, section) -> Union[dict, list]:
        """
        get a value from a given section
        Args:
            name: key of value
            section: section of the value

        Returns:
            value
        """
        return self.dbm.find_one_by(collection=SystemSettingsReader.COLLECTION, filter={'_id': section})[name]


    def get_section(self, section_name: str) -> dict:
        """TODO: document"""
        query_filter = {'_id': section_name}
        return self.dbm.find_one_by(collection=SystemSettingsReader.COLLECTION, filter=query_filter)


    def get_sections(self):
        """
        get all sections from config
        Returns:
            list of sections inside a config
        """
        return self.dbm.find_all(collection=SystemSettingsReader.COLLECTION, projection={'_id': 1})


    def get_all_values_from_section(self, section, default=None) -> dict:
        """
        get all values from a section
        Args:
            section: section name
            default: if no document was found

        Returns:
            key value dict of all elements inside section
        """
        try:
            section_values = self.dbm.find_one_by(collection=SystemSettingsReader.COLLECTION, filter={'_id': section})
        except NoDocumentFound as err:
            if default:
                return default
            raise SectionError(section) from err

        return section_values


    def get_all(self) -> list:
        """TODO: document"""
        return self.dbm.find_all(collection=SystemSettingsReader.COLLECTION)
