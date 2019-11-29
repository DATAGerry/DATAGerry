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
from cmdb.utils.error import CMDBError


class ImportRuntimeError(CMDBError):
    def __init__(self, importer_type, message):
        self.message = f'Error while importing with importer {importer_type}: {message}'
        super(ImportRuntimeError, self).__init__()


class ParserRuntimeError(CMDBError):
    def __init__(self, parser_type, message):
        self.message = f'Error while parsing with parser {parser_type}: {message}'
        super(ParserRuntimeError, self).__init__()


class ImporterLoadError(CMDBError):
    def __init__(self, importer_type, importer_name):
        self.message = f'Could not load importer {importer_name} of type {importer_type}'
        super(ImporterLoadError, self).__init__()


class ParserLoadError(CMDBError):
    def __init__(self, parser_type, parser_name):
        self.message = f'Could not load parser {parser_name} of type {parser_type}'
        super(ParserLoadError, self).__init__()