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
        self.entry_length = entry_length
        self.header = header
        super(CsvObjectParserResponse, self).__init__(count=count, entries=entries)


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

    def parse(self, file) -> (dict, list, CsvObjectParserResponse):
        run_config = self.get_config()
        LOGGER.info(f'Starting parser with CONFIG: {run_config}')
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

        with open(f'{file}', 'r', newline=run_config.get('newline')) as csv_file:
            csv_reader = csv.reader(csv_file, **dialect)
            if run_config.get('header'):
                parsed['header'] = next(csv_reader)
                parsed['entry_length'] = len(parsed['header'])
            else:
                parsed['entries'].append(next(csv_reader))
                parsed['entry_length'] = len(parsed['entries'][0])
            for row in csv_reader:
                parsed['entries'].append(row)
        parsed['count'] = len(parsed['entries'])
        return CsvObjectParserResponse(**parsed)
