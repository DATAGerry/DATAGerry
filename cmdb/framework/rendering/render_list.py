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
from typing import Union

from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.cmdb_object import CmdbObject
from cmdb.user_management.models.user import UserModel
from cmdb.framework.rendering.render_result import RenderResult
from cmdb.framework.rendering.cmdb_render import CmdbRender
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  RenderList - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class RenderList:
    """TODO: document"""
    def __init__(self,
                 object_list: list[CmdbObject],
                 request_user: UserModel,
                 ref_render=False,
                 objects_manager: ObjectsManager = None):
        """TODO: document"""
        self.object_list: list[CmdbObject] = object_list
        self.request_user = request_user
        self.ref_render = ref_render
        self.objects_manager = objects_manager


    def render_result_list(self, raw: bool = False) -> list[Union[RenderResult, dict]]:
        """TODO: document"""
        preparation_objects: list[RenderResult] = []

        for passed_object in self.object_list:
            tmp_render = CmdbRender(passed_object,
                                    self.objects_manager.get_object_type(passed_object.type_id),
                                    self.request_user,
                                    self.ref_render,
                                    self.objects_manager.dbm)

            if raw:
                current_render_result = tmp_render.result().__dict__
            else:
                current_render_result = tmp_render.result()
            preparation_objects.append(current_render_result)

        return preparation_objects
