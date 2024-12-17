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

from cmdb.manager.objects_manager import ObjectsManager

from cmdb.framework.rendering.cmdb_render import CmdbRender
from cmdb.framework.docapi.abstract_template_data import AbstractTemplateData

from cmdb.errors.manager.object_manager import ObjectManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ObjectTemplateData - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectTemplateData(AbstractTemplateData):
    """TODO: document"""

    def __init__(self, cmdb_object, objects_manager: ObjectsManager):
        super().__init__()
        self.objects_manager = objects_manager
        self._template_data = self.__get_objectdata(cmdb_object, 3)


    def __get_objectdata(self, cmdb_object, iteration):
        data = {}
        data["id"] = cmdb_object.object_information['object_id']
        data["fields"] = {}

        for field in cmdb_object.fields:
            try:
                field_name = field["name"]

                if (field["type"] == "ref" or field["type"] == "location") and field["value"] and iteration > 0:
                    # resolve type
                    current_object = self.objects_manager.get_object(field["value"])
                    type_instance = self.objects_manager.get_object_type(current_object.get_type_id())

                    cmdb_render_object = CmdbRender(current_object,
                                                    type_instance,
                                                    None,
                                                    False,
                                                    self.objects_manager.dbm)

                    data["fields"][field_name] = self.__get_objectdata(cmdb_render_object.result(), iteration - 1)
                elif field['type'] == 'ref-section-field':
                    data['fields'][field_name] = {'fields': {}}

                    for section_ref_field in field['references']['fields']:
                        data['fields'][field_name]['fields'][section_ref_field['name']] = section_ref_field['value']
                else:
                    data["fields"][field_name] = field["value"]
            except ObjectManagerGetError:
                continue
            except Exception as err:
                #TODO: ERROR-FIX
                LOGGER.error(err)

        return data
