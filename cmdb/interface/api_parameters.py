from enum import Enum
from typing import NewType

Parameter = NewType('Parameter', str)


class SortOrder(Enum):
    """Sort enum for http parameters"""
    ASCENDING = 1
    DESCENDING = -1


class ApiParameters:
    """Rest API Parameter superclass"""

    def __init__(self, query_string: Parameter = None, **filter):
        self.query_string: Parameter = query_string or Parameter('')
        self.filter: dict = filter or {}

    def __repr__(self):
        return f'Parameters: Query({self.query_string}) | Filter({self.filter})'


class CollectionParameters(ApiParameters):
    """Rest API class for collection parsing"""

    def __init__(self, query_string: Parameter, limit: int = None, sort: str = None,
                 order: int = None, page: int = None, **filter):
        self.limit: int = int(limit or 10)
        self.sort: str = sort or Parameter('public_id')
        self.order: int = int(order or SortOrder.ASCENDING.value)
        self.page: int = int(page or 1)
        self.skip: int = (self.page - 1) * self.limit
        super(CollectionParameters, self).__init__(query_string=query_string, **filter)

    @classmethod
    def from_http(cls, query_string: str, **parameters) -> "CollectionParameters":
        """
        Create a collection parameter instance from a http query string
        Args:
            query_string: raw query string
            **parameters: list of optional http parameters

        Returns:
            CollectionParameters instance
        """
        return cls(Parameter(query_string), **parameters)
