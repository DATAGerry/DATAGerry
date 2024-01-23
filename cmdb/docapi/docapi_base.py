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
from cmdb.framework.cmdb_render import CmdbRender
from cmdb.docapi.document_generator import ObjectDocumentGenerator
from cmdb.docapi.doctypes import PdfDocumentType
# -------------------------------------------------------------------------------------------------------------------- #

class DocApiManager:
    """TODO: document"""
    def __init__(self, template_manager, object_manager):
        self.__template_manager = template_manager
        self.__obm = object_manager


    def render_object_template(self, doctpl_id: int, object_id: int):
        """TODO: document"""
        template = self.__template_manager.get_template(doctpl_id)
        cmdb_object = self.__obm.get_object(object_id)
        type_instance = self.__obm.get_type(cmdb_object.get_type_id())
        cmdb_render_object = CmdbRender(object_instance=cmdb_object, type_instance=type_instance,
                                        render_user=None, object_manager=self.__obm)
        generator = ObjectDocumentGenerator(template, self.__obm, cmdb_render_object.result(), PdfDocumentType())

        return generator.generate_doc()
