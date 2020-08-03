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

from cmdb.templates.template_engine import TemplateEngine
from cmdb.templates.template_data import ObjectTemplateData

class DocumentGenerator:

    def generate_doc():
        pass


class ObjectDocumentGenerator:

    # default CSS to make the document styling in TinyMCE look like the styling in the PDF
    default_css = """
        img {
            zoom: 70%;
        }
    """

    def __init__(self, template, object_manager, cmdb_object, doctype):
        self.__template = template
        self.__object_manager = object_manager
        self.__cmdb_object = cmdb_object
        self.__doctype = doctype

    def generate_doc(self):
        # render template data
        template_data = ObjectTemplateData(self.__object_manager, self.__cmdb_object).get_template_data()
        template_engine = TemplateEngine()
        rendered_template = template_engine.render_template_string(self.__template.get_template_data(), template_data)

        # create full HTML document
        html = '<html><head>'
        html = html + '<title>' + self.__template.get_label() + '</title>'
        html = html + '<style>' + self.default_css + self.__template.get_template_style() + '</style>'
        html = html + '</head>'
        html = html + '<body>' + rendered_template + '</body></html>'

        # create document
        return self.__doctype.create_doc(html)
