from enum import Enum
from typing import NewType

Parameter = NewType('Parameter', str)


class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = -1


class ApiParameters:

    def __init__(self, query_string: Parameter = None, **optional):
        self.query_string: Parameter = query_string or Parameter('')
        self.optional = optional or {}


class CollectionParameters(ApiParameters):

    def __init__(self, query_string: Parameter, filter: dict = None, limit: int = None, sort: str = None,
                 order: int = None, page: int = None, **optional):
        self.filter: dict = filter or {}
        self.limit: int = limit or 10
        self.sort: str = sort or Parameter('public_id')
        self.order: int = order or SortOrder.ASCENDING.value
        self.page: int = page or 1
        self.skip: int = (self.page - 1) * self.limit
        super(CollectionParameters, self).__init__(query_string=query_string, **optional)

    def __repr__(self):
        return f'Params({self.__dict__})'

    @classmethod
    def from_http(cls, query_string: str, request_arguments: dict = None, **optional):
        return cls(Parameter(query_string),
                   filter=request_arguments.get('filter', {}),
                   limit=int(request_arguments.get('limit', 10)),
                   sort=str(request_arguments.get('sort', 'public_id')),
                   order=int(request_arguments.get('order', 1)),
                   page=int(request_arguments.get('page', 1)),
                   **optional)
