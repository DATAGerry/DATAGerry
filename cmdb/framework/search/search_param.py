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
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  SearchParam - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class SearchParam:
    """TODO: document"""
    POSSIBLE_FORM_TYPES = [
        'text',
        'regex',
        'type',
        'category',
        'disjunction',
        'publicID'
    ]

    def __init__(self, search_text, search_form: str, settings: dict = None, disjunction: bool = False):
        """SearchParamDAO constructor
        Args:
            search_text: searchable user input for database search
            search_form: kind of search parameter
            settings: optional settings based on the search form
            disjunction: optional kind of search parameter
        """
        self.search_text = search_text
        if search_form not in self.POSSIBLE_FORM_TYPES:
            raise ValueError(f'{search_form} is not a possible param type ')
        self.search_form = search_form
        self.settings: dict = settings or {}
        self.disjunction: bool = disjunction


    def __repr__(self):
        return f'[SearchParam] {self.search_text} - {self.search_form}'


    @classmethod
    def from_request(cls, request) -> list['SearchParam']:
        """Build a SearchParamDAO list from http request"""
        param_list: list[cls] = []
        for param in request:
            try:
                param_list.append(cls(
                        param['searchText'],
                        param['searchForm'],
                        param.get('settings', None),
                        param.get('disjunction', True)
                    )
                )
            except Exception as err:
                #TODO: ERROR-FIX
                LOGGER.error("[from_request] Exception: %s, Type: %s", err, type(err))
                continue

        return param_list
