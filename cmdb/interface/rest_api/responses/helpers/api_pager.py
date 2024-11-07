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
#                                                   APIPager - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class APIPager:
    """
    Pager for api responses.
    Shows data of the current page and meta data of other pages.
    """

    __slots__ = 'page', 'page_size', 'total_pages'

    def __init__(self, page: int, page_size: int, total_pages: int = None):
        """
        Constructor of the APIPager.

        Args:
            page: Current page number.
            page_size: Number of elements on this page.
            total_pages: Total number of pages for this query.
        """
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages


    def to_dict(self) -> dict:
        """TODO: document"""
        return {
            'page': self.page,
            'page_size': self.page_size,
            'total_pages': self.total_pages,
        }
