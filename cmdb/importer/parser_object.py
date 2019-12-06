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

from openpyxl.worksheet.worksheet import Worksheet

from cmdb.importer.importer_errors import ParserRuntimeError
from cmdb.utils.cast import auto_cast
from cmdb.importer.content_types import JSONContent, CSVContent, XLSXContent
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

    def __init__(self, count: int, entries: list, entry_length: int, header: dict = None):
        self.entry_length: int = entry_length
        self.header: dict = header or {}
        super(CsvObjectParserResponse, self).__init__(count=count, entries=entries)

    def get_entry_length(self) -> int:
        return self.entry_length

    def get_header_list(self) -> dict:
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
                    parsed['header'] = self.__generate_index_pair(next(csv_reader))
                for row in csv_reader:
                    row_list = []
                    for entry in row:
                        row_list.append(auto_cast(entry))
                    parsed.get('entries').append(self.__generate_index_pair(row_list))
                    parsed['count'] = parsed['count'] + 1

                if len(parsed.get('entries')) > 0:
                    parsed['entry_length'] = len(parsed.get('entries')[0])
                else:
                    raise ParserRuntimeError(self.__class__.__name__, 'No content data!')
        except Exception as err:
            LOGGER.error(err)
            raise ParserRuntimeError(self.__class__.__name__, err)
        return CsvObjectParserResponse(**parsed)


class ExcelObjectParserResponse(ObjectParserResponse):

    def __init__(self, count: int, entries: list, entry_length: int, header: dict = None):
        self.entry_length: int = entry_length
        self.header: dict = header or {}
        super(ExcelObjectParserResponse, self).__init__(count=count, entries=entries)

    def get_entry_length(self) -> int:
        return self.entry_length

    def get_header_list(self) -> dict:
        return self.header


class ExcelObjectParser(BaseObjectParser, XLSXContent):
    DEFAULT_CONFIG = {
        'sheet_name': 'Sheet1',
        'header': True
    }

    def __init__(self, parser_config: dict = None):
        super(ExcelObjectParser, self).__init__(parser_config)

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

    def parse(self, file) -> ExcelObjectParserResponse:
        from openpyxl import load_workbook

        parsed = {
            'count': 0,
            'header': None,
            'entries': [],
            'entry_length': 0
        }

        run_config = self.get_config()
        try:
            working_sheet = run_config['sheet_name']
        except (IndexError, ValueError, KeyError) as err:
            raise ParserRuntimeError(ExcelObjectParser, err)

        wb = load_workbook(file)
        try:
            sheet: Worksheet = wb[working_sheet]
        except KeyError as err:
            raise ParserRuntimeError(ExcelObjectParser, err)

        return ExcelObjectParserResponse(0, [], 0)
