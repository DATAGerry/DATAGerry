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
# along with this program. If not, see <https://www.gnu.org/licenses/>
"""TODO: document"""
from typing import Union
# -------------------------------------------------------------------------------------------------------------------- #

class BuilderParameters:
    """TODO: document"""

    def __init__(self,
                 criteria: Union[dict, list[dict]],
                 limit: int = 0,
                 skip: int = 0,
                 sort: str = 'public_id',
                 order: int = 1):

        self.criteria = criteria
        #TODO: raise exception if limit is smaller than 0
        self.limit = limit
        self.skip = skip
        self.sort = sort
        #TODO: raise exception if order is neither 1 nor -1
        self.order = order

    def __repr__(self):
        return f"""
                criteria:{self.criteria}, limit: {self.limit}, skip:{self.skip}, sort:{self.sort}, order:{self.order}
                """


    def get_criteria(self) -> Union[dict, list[dict]]:
        """Returns criteria attriute"""
        return self.criteria


    def get_limit(self) -> int:
        """Returns limit attribute"""
        return self.limit


    def has_limit(self) -> bool:
        """Returns if limit is set to value higher than 0(limitless)"""
        return self.limit > 0


    def get_skip(self) -> int:
        """Returns skip attribute"""
        return self.skip


    def get_sort(self) -> str:
        """Returns sort attribute"""
        return self.sort


    def get_order(self) -> int:
        """Returns order attribute"""
        return self.order
