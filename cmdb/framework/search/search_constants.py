# DataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2026 becon GmbH
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
"""
Constants for the object search of DataGerry
"""
import re

from cmdb.utils import BaseStrEnum
# -------------------------------------------------------------------------------------------------------------------- #

#: Flag string handed to `bson.Regex` for every search pattern: case-insensitive, multi-line, and
#: dot-matches-newline, so a search term hits regardless of casing or line breaks in a field value
SEARCH_REGEX_FLAGS: str = 'ims'

#: The `re` module equivalent of `SEARCH_REGEX_FLAGS`, used when a malformed pattern falls back to a
#: literal (escaped) match. Both must stay in sync so a fallback behaves like a successful compile
SEARCH_REGEX_RE_FLAGS: int = re.IGNORECASE | re.MULTILINE | re.DOTALL


class SearchResultKey(BaseStrEnum):
    """
    Enumeration of the keys in a serialized `SearchResult`

    This is the body of `GET|POST /rest/search/`. The Angular `SearchResultList` model mirrors it,
    so the members are a frontend-visible contract
    """
    LIMIT = 'limit'
    SKIP = 'skip'
    GROUPS = 'groups'
    TOTAL_RESULTS = 'total_results'
    NUMBER_OF_RESULTS = 'number_of_results'
    RESULTS = 'results'


class SearchResultMapKey(BaseStrEnum):
    """
    Enumeration of the keys in a serialized `SearchResultMap`

    One entry of `SearchResultKey.RESULTS`. The Angular `SearchResult` model mirrors it, so the
    members are a frontend-visible contract
    """
    RESULT = 'result'
    MATCHES = 'matches'


class SearchFormType(BaseStrEnum):
    """
    The kinds of search parameter a request may carry

    A **frontend-visible contract**: the Angular search bar builds these strings itself
    (`addTag('text' | 'regex' | 'type' | 'category')`) and the result bar appends the DISJUNCTION
    marker, so a member removed here rejects a payload the UI still sends.

    Four of the six drive a pipeline stage. The other two do not, and both are deliberate:

      - PUBLIC_ID is accepted from API clients; the frontend expresses "search by id" as a TEXT tag
        carrying a `publicID` setting instead
      - DISJUNCTION is a marker the result bar appends when type filtering switches to OR. Nothing
        reads it: the OR itself comes from each TYPE parameter's own `disjunction` flag, which
        defaults to True. It is accepted so the UI's payload validates - see discussion-backlog for
        whether it should be implemented or dropped
    """
    TEXT = 'text'
    REGEX = 'regex'
    TYPE = 'type'
    CATEGORY = 'category'
    DISJUNCTION = 'disjunction'
    PUBLIC_ID = 'publicID'


class SearchParamKey(BaseStrEnum):
    """
    Keys of one search parameter as the frontend sends it

    Mirrors the Angular `SearchBarTag`, so these spellings are a frontend-visible contract
    """
    SEARCH_TEXT = 'searchText'
    SEARCH_FORM = 'searchForm'
    SETTINGS = 'settings'
    DISJUNCTION = 'disjunction'
