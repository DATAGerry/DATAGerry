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

import csv
import json
import logging

from cmdb.importer.importer_errors import ParserRuntimeError
from cmdb.utils.cast import auto_cast
from cmdb.importer.content_types import JSONContent, CSVContent
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_response import ObjectParserResponse

LOGGER = logging.getLogger(__name__)


class JsonObjectParserResponse(ObjectParserResponse):

    def __init__(self, count: int, entries: list):
        super(JsonObjectParserResponse, self).__init__(count=count, entries=entries)


class JsonObjectParser(BaseObjectParser, JSONContent):
    DEFAULT_CONFIG = {
        'indent': 2,
        'encoding': 'UTF-8'
    }

    def __init__(self, parser_config: dict = None):
        super(JsonObjectParser, self).__init__(parser_config)

    def parse(self, file) -> (dict, list, JsonObjectParserResponse):
        run_config = self.get_config()
        with open(file, 'r', encoding=run_config.get('encoding')) as json_file:
            parsed = json.load(json_file)
        return JsonObjectParserResponse(count=len(parsed), entries=parsed)


class CsvObjectParserResponse(ObjectParserResponse):

    def __init__(self, count: int, entries: list, entry_length: int, header: list = None):
        self.entry_length: int = entry_length
        self.header: list = header
        super(CsvObjectParserResponse, self).__init__(count=count, entries=entries)

    def get_entry_length(self) -> int:
        return self.entry_length

    def get_header_list(self) -> list:
        if not self.header:
            return []
        return self.header


class CsvObjectParser(BaseObjectParser, CSVContent):
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
        super(CsvObjectParser, self).__init__(parser_config)

    def parse(self, file) -> CsvObjectParserResponse:
        run_config = self.get_config()

        dialect = {
            'delimiter': run_config.get('delimiter'),
            'quotechar': run_config.get('quoteChar'),
            'escapechar': run_config.get('escapeChar'),
            'skipinitialspace': True
        }
        parsed = {
            'count': 0,
            'header': None,
            'entries': [],
            'entry_length': 0
        }
        try:
            with open(f'{file}', 'r', newline=run_config.get('newline')) as csv_file:
                csv_reader = csv.reader(csv_file, dialect=dialect)
                if run_config.get('header'):
                    first_line = next(csv_reader)
                    parsed['header'] = first_line
                for row in csv_reader:
                    row_list = []
                    for entry in row:
                        row_list.append(auto_cast(entry))
                    parsed.get('entries').append(row_list)
                    parsed['count'] = parsed['count'] + 1

                if len(parsed.get('entries')) > 0:
                    parsed['entry_length'] = len(parsed.get('entries')[0])
                else:
                    raise ParserRuntimeError(self.__class__.__name__, 'No content data!')
        except Exception as err:
            LOGGER.error(err)
            raise ParserRuntimeError(self.__class__.__name__, err)
        return CsvObjectParserResponse(**parsed)
