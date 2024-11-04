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
from typing import Any
from werkzeug.wrappers import Response

from cmdb.interface.rest_api.responses.base_api_response import BaseAPIResponse
from cmdb.interface.rest_api.responses.helpers.operation_type_enum import OperationType
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            GetSingleValueResponse - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class GetSingleValueResponse(BaseAPIResponse):
    """TODO: document"""
    def __init__(self, value: Any):
        """TODO: document"""
        self.value = value
        super().__init__(OperationType.GET)


    def make_response(self, *args, **kwargs) -> Response:
        """
        Make a valid http response

        Returns:
            Instance of Response with a HTTP 200 status code
        """
        return self.make_api_response(self.value)
