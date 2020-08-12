from enum import Enum
from typing import NewType

Parameter = NewType('Parameter', str)


class SortOrder(Enum):
    """Sort enum for http parameters"""
    ASCENDING = 1
    DESCENDING = -1


class ApiParameters:
    """Rest API Parameter superclass"""

    def __init__(self, query_string: Parameter = None, **kwargs):
        self.query_string: Parameter = query_string or Parameter('')
        self.optional = kwargs

    @classmethod
    def from_http(cls, *args, **kwargs) -> "ApiParameters":
        raise NotImplementedError

    def __repr__(self):
        return f'Parameters: Query({self.query_string}) | Optional({self.optional})'


class CollectionParameters(ApiParameters):
    """Rest API class for collection parsing"""

    def __init__(self, query_string: Parameter, limit: int = None, sort: str = None,
                 order: int = None, page: int = None, filter: dict = None, **kwargs):
        self.limit: int = int(limit or 10)
        self.sort: str = sort or Parameter('public_id')
        self.order: int = int(order or SortOrder.ASCENDING.value)
        self.page: int = int((page or 1) or page < 1)
        self.skip: int = (self.page - 1) * self.limit
        self.filter: dict = filter or {}
        super(CollectionParameters, self).__init__(query_string=query_string, **kwargs)

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
