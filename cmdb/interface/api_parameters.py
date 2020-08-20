from enum import Enum
from typing import NewType, List, Union

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

    def to_dict(self) -> dict:
        """Get the object as a dict"""
        return {
            'optional': self.optional
        }

    def __repr__(self):
        return f'Parameters: Query({self.query_string}) | Optional({self.optional})'


class CollectionParameters(ApiParameters):
    """Rest API class for parameters passed by a http request on a collection route"""

    def __init__(self, query_string: Parameter, limit: int = None, sort: str = None,
                 order: int = None, page: int = None, filter: Union[List[dict], dict] = None, **kwargs):
        """
        Constructor of the CollectionParameters.

        Args:
            query_string: The raw http query string. Can be used when the parsed parameters are not enough.
            limit: The max number of resources returned (pageSize).
            sort: The query element which is used as the sort id (nested resources are possible via (.) dot).
            order: The order sequence in which `way` the sort should be returned.
            page: The current page. N number of elements will be skip based on (limit * page)
            filter: A generic query filter based on https://docs.mongodb.com/compass/master/query/filter/
            **kwargs:
        """
        self.limit: int = int(limit or 10)
        self.sort: str = sort or Parameter('public_id')
        self.order: int = int(order or SortOrder.ASCENDING.value)
        self.page: int = int((page or 1) or page < 1)
        self.skip: int = (self.page - 1) * self.limit
        self.filter: Union[List[dict], dict] = filter or {}
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
        from json import loads
        if 'filter' in parameters:
            parameters['filter'] = loads(parameters['filter'])
        return cls(Parameter(query_string), **parameters)

    def to_dict(self) -> dict:
        """Get the object as a dict"""
        return {
            **{
                'limit': self.limit,
                'sort': self.sort,
                'order': self.order,
                'page': self.page,
                'filter': self.filter,
            },
            **super(CollectionParameters, self).to_dict()
        }
