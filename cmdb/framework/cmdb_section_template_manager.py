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

from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.user_management import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework import CmdbSectionTemplate
from cmdb.utils.error import CMDBError
from cmdb.database.errors.database_errors import PublicIDAlreadyExists
from cmdb.framework.cmdb_errors import ObjectInsertError, SectionTemplateManagerDeleteError, SectionTemplateManagerError, \
    SectionTemplateManagerInsertError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class CmdbSectionTemplateManager(CmdbManagerBase):
    """
    class CmdbSectionTemplateManager
    """
    def __init__(self, database_manager=None, event_queue: Queue = None):
        self._event_queue = event_queue
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
            LOGGER.info("insert_section_template()")
            LOGGER.info(f"insert_section_template() => data: {data}")
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

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def get_new_id(self, collection: str) -> int:
        """
        Retrieves next publicID
        Args:
            collection (str): used collection

        Returns:
            int: new publicID
        """
        return self.dbm.get_next_public_id(collection)
