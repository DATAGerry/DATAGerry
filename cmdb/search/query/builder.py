# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import List, Any

LOGGER = logging.getLogger(__name__)


class Builder:
    """Base builder prototype"""

    def __len__(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    # Logical Query Operators
    @classmethod
    def and_(cls, expressions: List[dict]) -> dict:
        """Joins query clauses with a logical AND."""
        return {'$and': expressions}

    @classmethod
    def or_(cls, expressions: List[dict]) -> dict:
        """Joins query clauses with a logical OR."""
        return {'$or': expressions}

    @classmethod
    def not_(cls, expression: dict) -> dict:
        """Inverts the effect of a query expression."""
        return {'$not': expression}

    @classmethod
    def nor_(cls, expressions: List[dict]) -> dict:
        """Joins query clauses with a logical NOR."""
        return {'$nor': expressions}

    # Comparison
    @classmethod
    def eq_(cls, field: str, value: Any) -> dict:
        """Matches values that are equal to a specified value."""
        return {field: {'$eq': value}}

    @classmethod
    def gt_(cls, field: str, value: Any) -> dict:
        """Matches values that are greater than a specified value."""
        return {field: {'$gt': value}}

    @classmethod
    def gte_(cls, field: str, value: Any) -> dict:
        """Matches values that are greater than or equal to a specified value."""
        return {field: {'$gte': value}}

    @classmethod
    def in_(cls, field: str, values: List[Any]) -> dict:
        """Matches any of the values specified in an array."""
        return {field: {'$in': values}}

    @classmethod
    def lt_(cls, field: str, value: Any) -> dict:
        """Matches values that are less than a specified value."""
        return {field: {'$lt': value}}

    @classmethod
    def lte_(cls, field: str, value: Any) -> dict:
        """Matches values that are less than or equal to a specified value."""
        return {field: {'$lte': value}}

    @classmethod
    def ne_(cls, field: str, value: Any) -> dict:
        """Matches all values that are not equal to a specified value."""
        return {field: {'$ne': value}}

    @classmethod
    def nin_(cls, field: str, values: List[Any]) -> dict:
        """Matches none of the values specified in an array."""
        return {field: {'$nin': values}}

    # Element
    @classmethod
    def exists_(cls, field: str, exist: bool = True) -> dict:
        """Matches documents that have the specified field."""
        return {field: {'$exists': exist}}

    @classmethod
    def element_match_(cls, field: str, criteria: dict) -> dict:
        """If element in the array field matches all the specified $elemMatch conditions."""
        return {field: {'$elemMatch': criteria}}

    # Evaluation
    @classmethod
    def regex_(cls, field: str, regex: str, options: str = 'imsx') -> dict:
        """Where values match a specified regular expression"""
        return {field: {'$regex': regex, '$options': options}}

    # Aggregations
    @classmethod
    def match_(cls, query: dict) -> dict:
        """Filters the document stream to allow only matching documents to pass
        unmodified into the next pipeline stage."""
        return {'$match': query}

    @classmethod
    def count_(cls, name: str) -> dict:
        """Returns a count of the number of documents at this stage of the aggregation pipeline."""
        return {'$count': name}

    @classmethod
    def skip_(cls, value: int) -> dict:
        """Skips over the specified number of documents that pass into the stage."""
        return {'$skip': value}

    @classmethod
    def limit_(cls, value: int) -> dict:
        """Limits the number of documents passed to the next stage in the pipeline."""
        return {'$limit': value}

    @classmethod
    def facet_(cls, stages: dict) -> dict:
        """Processes multiple aggregation pipelines within a single stage on the same set of input documents."""
        return {'$facet': stages}

    @classmethod
    def group_(cls, _id: str, value: dict = None) -> dict:
        """Groups input documents by the specified _id expression and for each distinct grouping, outputs a document."""
        statement = {'_id': _id}
        if value:
            statement.update(value)
        return {'$group': statement}

    @classmethod
    def lookup_(cls, _from: str, _local: str, _foreign: str, _as: str) -> dict:
        """ Performs a left outer join to an unsharded collection in the same database to filter in documents
            from the “joined” collection for processing.
            Args:
                _from:      Specifies the collection in the same database to perform the join with.
                _local:     Specifies the field from the documents input to the $lookup stage.
                _foreign:   Specifies the field from the documents in the from collection.
                _as:        Specifies the name of the new array field to add to the input documents.
            """
        return {'$lookup': {'from': _from, 'localField': _local, 'foreignField': _foreign, 'as': _as}}

    @classmethod
    def lookup_sub_(cls, from_: str, let_: dict, pipeline_: list, as_: str) -> dict:
        """ Performs uncorrelated subqueries between two collections as well as allow other join conditions besides a
            single equality match, the $lookup stage has the following syntax.
            Args:
                from_:      Specifies the collection in the same database to perform the join with.
                let_:       Optional. Specifies variables to use in the pipeline field stages.
                pipeline_:  The pipeline determines the resulting documents from the joined collection.
                as_:        Specifies the name of the new array field to add to the input documents.
            """
        return {'$lookup': {'from': from_, 'let': let_, 'pipeline': pipeline_, 'as': as_}}

    @classmethod
    def unwind_(cls, path: str):
        """Duplicates each document in the pipeline, once per array element."""
        return {'$unwind': path}

    @classmethod
    def project_(cls, specification: dict):
        """Passes along the documents with the requested fields to the next stage in the pipeline."""
        return {'$project': specification}

    @classmethod
    def sort_(cls, sort: str, order: int) -> dict:
        """Sorts all input documents and returns them to the pipeline in sorted order."""
        if order != 1 and order != -1:
            raise ValueError('Order value must be 1 (ascending) or -1 (descending)')
        return {'$sort': {sort: order}}

    # Type Expression Operators
    @classmethod
    def type_(cls, expression) -> dict:
        """Return the BSON data type of the field."""
        return {'$type': expression}
