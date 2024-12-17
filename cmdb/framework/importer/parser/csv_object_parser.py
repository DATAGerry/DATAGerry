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
import csv
import logging

from cmdb.utils.cast import auto_cast
from cmdb.framework.importer.content_types import CSVContent
from cmdb.framework.importer.parser.base_object_parser import BaseObjectParser
from cmdb.framework.importer.responses.csv_object_parser_response import CsvObjectParserResponse

from cmdb.errors.importer import ParserRuntimeError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                CsvObjectParser - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class CsvObjectParser(BaseObjectParser, CSVContent):
    """TODO: document"""

    BYTE_ORDER_MARK = '\ufeff'
    BAD_DELIMITERS = ['\r', '\n', '"', BYTE_ORDER_MARK]
    DEFAULT_QUOTE_CHAR = '"'
    DEFAULT_CONFIG = {
        'delimiter': ',',
        'newline': '',
        'quoteChar': DEFAULT_QUOTE_CHAR,
        'escapeChar': None,
        'header': True
    }

    def __init__(self, parser_config: dict = None):
        super().__init__(parser_config)


    @staticmethod
    def __generate_index_pair(row: list) -> dict:
        line: dict = {}
        idx: int = 0
        for col in row:
            line.update({
                idx: col
            })
            idx = idx + 1
        return line


    def parse(self, file) -> CsvObjectParserResponse:
        run_config = self.get_config()
        parsed = {
            'count': 0,
            'header': None,
            'entries': [],
            'entry_length': 0
        }
        try:
            with open(f'{file}', 'r', encoding='utf-8', newline=run_config.get('newline')) as csv_file:
                csv_reader = csv.reader(csv_file,
                                        delimiter=run_config.get('delimiter'),
                                        quotechar=run_config.get('quoteChar'),
                                        escapechar=run_config.get('escapeChar'),
                                        skipinitialspace=True)
                if run_config.get('header'):
                    parsed['header'] = next(csv_reader)
                for row in csv_reader:
                    row_list = []
                    for entry in row:
                        row_list.append(auto_cast(entry))
                    parsed.get('entries').append(self.__generate_index_pair(row_list))
                    parsed['count'] = parsed['count'] + 1

                if len(parsed.get('entries')) > 0:
                    parsed['entry_length'] = len(parsed.get('entries')[0])
                else:
                    raise ParserRuntimeError(f"[{self.__class__.__name__}]: No content data!")
        except Exception as err:
            LOGGER.error(str(err))
            raise ParserRuntimeError(f"[{self.__class__.__name__}]: An error occured: {str(err)}") from err

        return CsvObjectParserResponse(**parsed)
