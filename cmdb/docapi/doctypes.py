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
"""TODO: document"""
import io
from xhtml2pdf import pisa
# -------------------------------------------------------------------------------------------------------------------- #

class DocumentType:
    """TODO: document"""
    FILE_EXTENSION = None
    ICON = None
    LABEL = None

    def __init__(self):
        pass

    def create_doc(self, input_data):
        """TODO: document"""
        pass


class PdfDocumentType:
    """TODO: document"""
    FILE_EXTENSION = "pdf"
    ICON = "file-pdf"
    LABEL = "PDF"

    def __init__(self):
        pass

    def create_doc(self, input_data):
        """TODO: document"""
        output = io.BytesIO()
        # create PDF
        pdf_creator = pisa.CreatePDF(
            input_data,
            dest=output,
            encoding='utf8'
        )
        output.seek(0)
        return output
