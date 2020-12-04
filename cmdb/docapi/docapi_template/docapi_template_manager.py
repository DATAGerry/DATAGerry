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

from cmdb.event_management.event import Event
from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError
from cmdb.user_management import UserModel
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate

LOGGER = logging.getLogger(__name__)


class DocapiTemplateManager(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo, event_queue=None):
        self.dbm = database_manager
        self._event_queue = event_queue
        super().__init__(database_manager)

    def get_new_id(self) -> int:
        return self.dbm.get_next_public_id(DocapiTemplate.COLLECTION)

    def get_template(self, public_id: int) -> DocapiTemplate:
        try:
            result = self.dbm.find_one(collection=DocapiTemplate.COLLECTION, public_id=public_id)
        except (DocapiTemplateManagerGetError, Exception) as err:
            LOGGER.error(err)
            raise err
        return DocapiTemplate(**result)

    def get_all_templates(self):
        template_list = []
        for template in self.dbm.find_all(collection=DocapiTemplate.COLLECTION):
            try:
                template_list.append(DocapiTemplate(**template))
            except CMDBError:
                continue
        return template_list

    def get_templates_by(self, **requirements):
        try:
            ack = []
            templates = self._get_many(collection=DocapiTemplate.COLLECTION, limit=0, **requirements)
            for template in templates:
                ack.append(DocapiTemplate(**template))
            return ack
        except (CMDBError, Exception) as e:
            raise DocapiTemplateManagerGetError(err=e)

    def get_template_by_name(self, **requirements) -> DocapiTemplate:
        try:
            templates = self._get_many(collection=DocapiTemplate.COLLECTION, limit=1, **requirements)
            if len(templates) > 0:
                return DocapiTemplate(**templates[0])
            else:
                raise DocapiTemplateManagerGetError(err='More than 1 type matches this requirement')
        except (CMDBError, Exception) as e:
            raise DocapiTemplateManagerGetError(err=e)

    def insert_template(self, data: (DocapiTemplate, dict)) -> int:
        """
        Insert new DocapiTemplate Object
        Args:
            data: init data
        Returns:
            Public ID of the new DocapiTemplate in database
        """
        if isinstance(data, dict):
            try:
                new_object = DocapiTemplate(**data)
            except CMDBError as e:
                raise DocapiTemplateManagerInsertError(e)
        elif isinstance(data, DocapiTemplate):
            new_object = data
        try:
            ack = self.dbm.insert(
                collection=DocapiTemplate.COLLECTION,
                data=new_object.to_database()
            )
            if self._event_queue:
                event = Event("cmdb.docapi.added", {"id": new_object.get_public_id(),
                                                    "active": new_object.get_active(),
                                                    "user_id": new_object.get_author_id()})
                self._event_queue.put(event)
        except CMDBError as e:
            raise DocapiTemplateManagerInsertError(e)
        return ack

    def update_template(self, data: (dict, DocapiTemplate), request_user: UserModel) -> str:
        """
        Update new DocapiTemplat Object
        Args:
            data: init data
            request_user: current user, to detect who triggered event
        Returns:
            Public ID of the DocapiTemplate in database
        """
        if isinstance(data, dict):
            update_object = DocapiTemplate(**data)
        elif isinstance(data, DocapiTemplate):
            update_object = data
        else:
            raise DocapiTemplateManagerUpdateError(f'Could not update template with ID: {data.get_public_id()}')
        update_object.last_execute_date = datetime.utcnow()
        ack = self._update(
            collection=DocapiTemplate.COLLECTION,
            public_id=update_object.get_public_id(),
            data=update_object.to_database()
        )
        if self._event_queue:
            event = Event("cmdb.docapi.updated", {"id": update_object.get_public_id(),
                                                  "active": update_object.get_active(),
                                                  "user_id": request_user.get_public_id()})
            self._event_queue.put(event)
        return ack.acknowledged

    def delete_template(self, public_id: int, request_user: UserModel) -> bool:
        try:
            ack = self._delete(collection=DocapiTemplate.COLLECTION, public_id=public_id)
            if self._event_queue:
                event = Event("cmdb.docapi.deleted", {"id": public_id, "active": False,
                                                      "user_id": request_user.get_public_id()})
                self._event_queue.put(event)
            return ack
        except Exception:
            raise DocapiTemplateManagerDeleteError(f'Could not delete template with ID: {public_id}')


class DocapiTemplateManagerGetError(ManagerGetError):

    def __init__(self, err):
        super(DocapiTemplateManagerGetError, self).__init__(err)


class DocapiTemplateManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super(DocapiTemplateManagerInsertError, self).__init__(err)


class DocapiTemplateManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super(DocapiTemplateManagerUpdateError, self).__init__(err)


class DocapiTemplateManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super(DocapiTemplateManagerDeleteError, self).__init__(err)
