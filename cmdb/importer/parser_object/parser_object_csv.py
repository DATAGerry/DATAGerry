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
import logging

from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_errors import ParserError
from cmdb.importer.parser_result import ParserResult
from cmdb.utils.helpers import str_to_bool

LOGGER = logging.getLogger(__name__)


class CsvParser(BaseObjectParser):
    CONTENT_TYPE = 'text/csv'
    FILE_TYPE = 'csv'

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
        if parser_config['escapeChar'] == 'null':
            parser_config['escapeChar'] = None
        parser_config['header'] = str_to_bool(parser_config['header'])
        super(CsvParser, self).__init__(parser_config)

    def parse(self, file) -> dict:
        run_config = self.get_config()
        dialect = {
            'delimiter': run_config.get('delimiter'),
            'quotechar': run_config.get('quoteChar'),
            'escapechar': run_config.get('escapeChar'),
            'skipinitialspace': True
        }
        output = {
            'header': None,
            'lines': [],
            'count': 0,
            'parser_config': self.get_config()
        }
        try:
            with open(f'/tmp/{file}', 'r', newline=run_config.get('newline')) as csv_file:
                csv_reader = csv.reader(csv_file, **dialect)
                if str_to_bool(run_config.get('header')):
                    output['header'] = next(csv_reader)
                for row in csv_reader:
                    output['lines'].append(row)
            output['count'] = len(output['lines'])
        except Exception as e:
            raise ParserError(e)
        return ParserResult(**output)
