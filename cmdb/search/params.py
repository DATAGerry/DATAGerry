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
import logging
from typing import List

LOGGER = logging.getLogger(__name__)


class SearchParam:
    POSSIBLE_FORM_TYPES = [
        'text',
        'type',
        'category',
        'publicID'
    ]

    def __init__(self, search_text, search_form: str, settings: dict = None):
        """SearchParamDAO constructor
        Args:
            search_text: searchable user input for database search
            search_form: kind of search parameter
            settings: optional settings based on the search form
        """
        self.search_text = search_text
        if search_form not in self.POSSIBLE_FORM_TYPES:
            raise ValueError(f'{search_form} is not a possible param type ')
        self.search_form = search_form
        self.settings: dict = settings or {}

    def __repr__(self):
        return f'[SearchParam] {self.search_text} - {self.search_form}'

    @classmethod
    def from_request(cls, request) -> List['SearchParam']:
        """Build a SearchParamDAO list from http request"""
        param_list: List[cls] = []
        for param in request:
            try:
                param_list.append(cls(param['searchText'], param['searchForm'], param.get('settings', None)))
            except Exception as err:
                LOGGER.error(f'[SearchParamDAO](from_request): {err}')
                continue
        return param_list
