from enum import Enum
from typing import NewType, TypeVar, Generic

P = TypeVar('P')
Parameter = NewType('Parameter', str)


class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = -1


class ApiParameters:

    def __init__(self, raw_query: Parameter = None, **optional):
        self.raw_query: Parameter = raw_query or Parameter('')
        self.optional = optional or {}


class CollectionParameters(ApiParameters):

    def __init__(self, raw_query: Parameter, filter_: dict = None, limit: int = None, sort: str = None,
                 order: int = None, page: int = None, **optional):
        self.filter_: dict = filter_ or {}
        self.limit: int = limit or 10
        self.sort: str = sort or Parameter('public_id')
        self.order: int = order or SortOrder.ASCENDING
        self.page: int = page or 1
        self.skip: int = (self.page - 1) * self.limit
        super(CollectionParameters, self).__init__(raw_query=raw_query, **optional)

    @classmethod
    def from_http(cls, query_string: str, request_arguments: dict = None, **optional):
        return cls(Parameter(query_string),
                   filter_=request_arguments.get('filter'),
                   limit=request_arguments.get('limit'),
                   sort=request_arguments.get('sort'),
                   order=request_arguments.get('order'),
                   page=request_arguments.get('page'),
                   **optional)
