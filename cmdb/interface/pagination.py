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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from urllib.parse import urlparse, ParseResult
from cmdb.interface.api_parameters import CollectionParameters


class APIPagination:
    """
    Pagination data for rest api calls.
    Reference to RFC 5988 and should be used as a cursor.
    """

    def __init__(self, current: str, first, prev=None, next=None, last=None):
        self.current = current
        self.first = first
        self.prev = prev
        self.next = next
        self.last = last

    @classmethod
    def create(cls, url: str, params: CollectionParameters, total: int = None):
        parsed_url: ParseResult = urlparse(url)
        print(parsed_url.query)
        return cls(url, '')

    def to_dict(self) -> dict:
        return {
            'current': self.current,
            'first': self.first,
            'prev': self.prev,
            'next': self.next,
            'last': self.last
        }
