from typing import Generic, TypeVar, Union, Type

from cmdb.framework.cmdb_dao import CmdbDAO

C = TypeVar('C', bound=CmdbDAO)


class IterationResult(Generic[C]):

    def __init__(self, results: Union[C, dict], total: int):
        self.results = results
        self.count = len(self.results)
        self.total = total

    def convert_to(self, c: Type[C]):
        self.results = [c.from_data(result) for result in self.results]

    @classmethod
    def from_aggregation(cls, aggregation):
        aggregation_result = next(aggregation)
        return cls(aggregation_result['results'], total=aggregation_result['meta'][0]['total'])
