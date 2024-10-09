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
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.docapi_template_manager import DocapiTemplateManager

from cmdb.framework.cmdb_render import CmdbRender
from cmdb.docapi.document_generator import ObjectDocumentGenerator
from cmdb.docapi.doctypes import PdfDocumentType
# -------------------------------------------------------------------------------------------------------------------- #

class DocApiRenderer:
    """TODO: document"""
    def __init__(self, template_manager: DocapiTemplateManager, object_manager, objects_manager: ObjectsManager):
        self.template_manager = template_manager
        self.object_manager = object_manager
        self.objects_manager = objects_manager


    def render_object_template(self, doctpl_id: int, object_id: int):
        """TODO: document"""
        template = self.template_manager.get_template(doctpl_id)
        cmdb_object = self.objects_manager.get_object(object_id)
        type_instance = self.objects_manager.get_object_type(cmdb_object.get_type_id())
        cmdb_render_object = CmdbRender(cmdb_object,
                                        type_instance,
                                        None,
                                        self.object_manager,
                                        False,
                                        self.objects_manager)

        generator = ObjectDocumentGenerator(template,
                                            self.object_manager,
                                            cmdb_render_object.result(),
                                            PdfDocumentType(),
                                            self.objects_manager)

        return generator.generate_doc()
