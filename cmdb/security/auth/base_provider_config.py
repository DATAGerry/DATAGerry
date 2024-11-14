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
#                                              AuthProviderConfig - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseAuthProviderConfig:
    """Base provider config"""

    DEFAULT_CONFIG_VALUES = {
        'active': True
    }

    def __init__(self, active: bool, **kwargs):
        """Base init constructor
        Args:
            active: is provider activated/deactivated
            **kwargs:
        """
        self.active: bool = active
        # auto set parameters as attribute
        for key, value in kwargs.items():
            setattr(self, key, value)


    def is_active(self) -> bool:
        """TODO: document"""
        return self.active
