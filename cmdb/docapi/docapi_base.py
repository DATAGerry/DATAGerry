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

from cmdb.document_api.document_generator import ObjectDocumentGenerator
from cmdb.document_api.document_template import DocumentTemplate
from cmdb.document_api.doctypes import PdfDocumentType

class DocumentApiManager:

    def __init__(self):
        pass

    def create_doc(self):
        html = """
        <html>
            <body>
                <h1>DATAGERRY Test</h1>
                <img src="data:image/png;base64,iVBORw0KGgoAAA
                ANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4
                //8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU
                5ErkJggg==" alt="Red dot" />
                <p style="border: 1px solid">Testdata</p>
            </body>
        </html>
        """
        template = DocumentTemplate(1, "testfile", "Testfile", html)
        cmdb_object = None
        doctype = PdfDocumentType()
        generator = ObjectDocumentGenerator(template, cmdb_object, doctype)

        return generator.generate_doc()
