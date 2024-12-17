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
#                                                 CategoryMeta - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CategoryMeta:
    """TODO: document"""
    def __init__(self, icon: str = '', order: int = None):
        self.icon = icon
        self.order = order


    def get_icon(self) -> str:
        """Get a icon, string or unicode symbol"""
        return self.icon


    def has_icon(self) -> bool:
        """Check if icon is set"""
        if self.icon:
            return True

        return False


    def get_order(self) -> int:
        """Get the order"""
        return self.order


    def has_order(self) -> bool:
        """Check if order is set"""
        if self.order:
            return True

        return False
