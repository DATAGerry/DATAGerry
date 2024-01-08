# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
This managers represents the core functionalities for the use of CMDB section templates.
All communication with the section templates is controlled by this manager.
The implementation of the manager used is always realized using the respective superclass.
"""
import logging
from queue import Queue

from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.object_manager import ObjectManager

from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.user_management import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework import CmdbSectionTemplate
from cmdb.utils.error import CMDBError
from cmdb.database.errors.database_errors import PublicIDAlreadyExists
from cmdb.framework.cmdb_errors import ObjectInsertError, \
                                       SectionTemplateManagerDeleteError, \
                                       SectionTemplateManagerError, \
                                       SectionTemplateManagerInsertError
from cmdb.framework.results.list import ListResult
from cmdb.framework import TypeModel
from cmdb.framework.models.type_model import TypeFieldSection
from cmdb.framework.cmdb_object import CmdbObject

# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class CmdbSectionTemplateManager(CmdbManagerBase):
    """
    class CmdbSectionTemplateManager
    """
    def __init__(self, database_manager=None, event_queue: Queue = None):
        self._event_queue = event_queue
        self.type_manager = TypeManager(database_manager)
        self.cmdb_object_manager = CmdbObjectManager(database_manager)
        self.object_manager = ObjectManager(database_manager, event_queue)
        super().__init__(database_manager)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    CRUD - SECTION                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_section_template(
            self,
            data: dict,
            user: UserModel = None,
            permission: AccessControlPermission = None) -> int:
        """
        Insert new CMDB Section Template
        Args:
            data: init data
            user: current user, to detect who triggered event
            permission: extended user acl rights
        Returns:
            Public ID of the new section template in database
        """
        new_section_template = None
        try:
            new_section_template = CmdbSectionTemplate(**data)
        except CMDBError as error:
            LOGGER.debug('Error while inserting section template - error: %s', error)
            raise SectionTemplateManagerInsertError(error) from error

        try:
            ack = self.dbm.insert(
                collection = CmdbSectionTemplate.COLLECTION,
                data = new_section_template.__dict__
            )

        except (CMDBError, PublicIDAlreadyExists) as error:
            raise ObjectInsertError(error) from error

        return ack


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_section_template(self,
                             public_id: int,
                             user: UserModel = None,
                             permission: AccessControlPermission = None) -> CmdbSectionTemplate:
        """TODO: document"""
        try:
            resource = []
            section_template = self._get(collection=CmdbSectionTemplate.COLLECTION, public_id=public_id)
            if section_template:
                resource = CmdbSectionTemplate(**section_template)
        except Exception as error:
            raise SectionTemplateManagerError(str(error)) from error

        return resource

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_section_template(self, public_id: int, user: UserModel, permission: AccessControlPermission = None):
        """TODO: document"""
        try:
            # then delete the location itself
            ack = self._delete(CmdbSectionTemplate.COLLECTION, public_id)
            return ack
        except (CMDBError, Exception) as error:
            raise SectionTemplateManagerDeleteError(error) from error


# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def cleanup_global_section_templates(self, template_name: str) -> None:
        """
        Removes the global section template from types, summaries and objects

        Args:
            template_name (str): The name of the global section template
        """
        type_filter: dict = {
            "global_template_ids":template_name
        }

        found_types: ListResult = self.type_manager.find(type_filter)

        a_type: TypeModel
        for a_type in found_types.results:
            #remove the template_name from the type
            a_type.global_template_ids.remove(template_name)

            #remove the section from render_meta.sections
            type_template_section: TypeFieldSection = a_type.get_section(template_name)

            a_type.render_meta.sections = [section for section in a_type.render_meta.sections
                                           if section.name != type_template_section.name]

            #remove the fields in render_meta.sections.fields from type.fields
            template_section_field_names: list[str] = type_template_section.get_fields()

            a_type.fields = [field for field in a_type.fields if field['name'] not in template_section_field_names]

            #remove all fields from summary
            a_type.render_meta.summary.fields = [field_name for field_name in a_type.render_meta.summary.fields
                                                  if field_name not in template_section_field_names]

            #remove the fields from all objects which used this global section template
            self.cleanup_global_section_objects(a_type.public_id, template_section_field_names)

            #Update the type changes for the type
            self.type_manager.update(a_type.public_id, a_type)


    def cleanup_global_section_objects(self, type_id: int, section_field_names: list[str]) -> None:
        """
        Retrives all objects with the given type_id and deletes all fields provided

        Args:
            type_id (int): ID of the type for which the objects should be cleaned
            section_field_names (list[str]): List of all fields which should be deleted 
        """
        section_objects: list = self.cmdb_object_manager.get_objects_by_type(type_id)

        # remove section fields and update the objects
        an_object: CmdbObject
        for an_object in section_objects:
            an_object.fields = [field for field in an_object.fields if field['name'] not in section_field_names]

            self.object_manager.update(an_object.public_id, an_object)


    def get_new_id(self, collection: str) -> int:
        """
        Retrieves next publicID
        Args:
            collection (str): used collection

        Returns:
            int: new publicID
        """
        return self.dbm.get_next_public_id(collection)
