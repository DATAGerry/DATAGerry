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
This module is the base class for the profiles of DATAGERRY assistant
"""
import logging
from datetime import datetime, timezone

from flask import current_app
from cmdb.framework import TypeModel
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

class ProfileBase:
    """
    This class cointains all functions required by the different profiles
    """

    def __init__(self, created_type_ids: dict):
        self.type_dict: dict = {}
        self.created_type_ids: dict = created_type_ids

        self.type_collection = TypeModel.COLLECTION

        with current_app.app_context():
            self.type_manager: TypeManager = TypeManager(current_app.database_manager)
            self.object_manager: CmdbObjectManager = CmdbObjectManager(current_app.database_manager)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   HELPER FUNCTIONS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
    def set_type_section_field(self, type_key: str, section_id: str, field_name: str):
        """
        Sets the section for the type

        Args:
            type_key (str): Used to identify the correct type of the profile
            section_id (str): Used to identify the correct section in the list
            field_name (str): The unique field name like 'ref-33320'
        """
        current_type = self.type_dict[type_key]

        type_sections: list = current_type['render_meta']['sections']

        for section in type_sections:
            if section['name'] == section_id:
                section_fields: list = section['fields']
                section_fields.append(field_name)

        self.type_dict[type_key] = current_type


    def set_type_summary_field(self, type_key: str, field_name: str):
        """
        Sets the summary for the type

        Args:
            type_key (str): _description_
            field_name (str): _description_
        """
        current_type = self.type_dict[type_key]

        type_summary_fields: list = current_type['render_meta']['summary']['fields']
        type_summary_fields.append(field_name)

        self.type_dict[type_key] = current_type


    def create_basic_type(self, type_name_key: str, type_dict: dict):
        """
        Creates a new type in the db
        Args:
            type_name_id (str): Key which should be used for the id of this type, like 'user_type_id'
            type_dict (dict): all the required data to create the type except the public_id
        """
        type_dict['public_id'] = self.object_manager.get_new_id(self.type_collection)
        new_type_id: int = self.type_manager.insert(type_dict)

        self.created_type_ids[type_name_key] = new_type_id


    def get_created_type_ids(self) -> dict:
        """
        Returns all created type ids which can be used for other profile creations

        Returns:
            dict: All created type ids
        """
        return self.created_type_ids


    def get_current_datetime(self) -> datetime:
        """
        Calculates the current datetime and returns it
        
        Returns:
            datetime: Current datetime
        """
        return datetime.now(timezone.utc)
