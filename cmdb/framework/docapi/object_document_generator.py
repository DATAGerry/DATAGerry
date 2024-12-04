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

from cmdb.framework.docapi.template_engine import TemplateEngine
from cmdb.framework.docapi.object_template_data import ObjectTemplateData
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ObjectDocumentGenerator - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectDocumentGenerator:
    """TODO: document"""
    # default CSS to make the document styling in TinyMCE look like the styling in the PDF
    default_css = """
        img {
            zoom: 70%;
        }

        td {
            padding: 1px;
        }
    """

    def __init__(self, template, cmdb_object, doctype, objects_manager: ObjectsManager):
        self.__template = template
        self.__cmdb_object = cmdb_object
        self.__doctype = doctype
        self.objects_manager = objects_manager


    def generate_doc(self):
        """TODO: document"""
        # render template data
        template_data = ObjectTemplateData(self.__cmdb_object,
                                           self.objects_manager).get_template_data()
        template_engine = TemplateEngine()
        rendered_template = template_engine.render_template_string(self.__template.get_template_data(), template_data)

        # create full HTML document
        html = '<html><head>'
        html = html + '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        html = html + '<meta charset="UTF-8" />'
        html = html + '<title>' + self.__template.get_label() + '</title>'
        html = html + '<style>' + self.default_css + self.__template.get_template_style() + '</style>'
        html = html + '</head>'
        html = html + '<body>' + rendered_template + '</body></html>'

        # create document
        return self.__doctype.create_doc(html)
