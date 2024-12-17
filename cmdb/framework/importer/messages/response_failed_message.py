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
#                                             ResponseFailedMessage - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class ResponseFailedMessage:
    """Message wrapper for failed objects"""

    def __init__(self, error_message: str, status: int, public_id: int = None, obj: dict = None):
        """Init message
        Args:
            status: the given status code of exceptions
            error_message: reason why it failed - exception error or something
            public_id (optional): failed public_id
            obj (optional): failed dict
        """
        self.status = status
        self.public_id = public_id
        self.error_message = error_message
        self.obj = obj


    def to_dict(self) -> dict:
        """TODO: document"""
        return {
            'status': self.status,
            'public_id': self.public_id,
            'error_message': self.error_message,
            'obj': self.obj,
        }
