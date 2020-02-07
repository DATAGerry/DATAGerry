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

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class ExportdHeader(object):
    def __init__(self, data: str = '', mimetype: str = 'application/json', charset: str = 'utf-8', status: int = 200, **kwargs):
        """
        Args:
            data: name of this job
            mimetype: Notifies the server of the type of data that can be returned
            charset: Notifies the server which character set the client understands.
            status: The HTTP Status code
            **kwargs: optional params
        """
        self.data = data
        self.mimetype = mimetype
        self.charset = charset
        self.status = status
        super(ExportdHeader, self).__init__(**kwargs)
