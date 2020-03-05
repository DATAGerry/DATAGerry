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
from typing import List, Any

import pytest

from cmdb.search.query import Query, Pipeline
from cmdb.search.query.builder import Builder
from cmdb.search.query.pipe_builder import PipelineBuilder
from cmdb.search.query.query_builder import QueryBuilder


class TestBuilder:
    """Test suite for the search builder"""

    def test_base(self):
        """Test base method raises implementation errors"""
        builder = Builder()
        with pytest.raises(NotImplementedError):
            len(builder)
        with pytest.raises(NotImplementedError):
            builder.clear()

    def test_base_class(self):
        """Test base method operations"""
        expressions: List[dict] = [{_: _} for _ in range(0, 10)]
        field: str = 'f'
        page: int = 10
        values: List[Any] = [_ for _ in range(0, 10)]
        value = values[0]
        criteria: dict = {'test': 1}
        regex = '^T.*est$'

        assert Builder.and_(expressions) == {'$and': expressions}
        assert Builder.or_(expressions) == {'$or': expressions}
        assert Builder.not_(expressions[0]) == {'$not': expressions[0]}
        assert Builder.nor_(expressions) == {'$nor': expressions}
        assert Builder.eq_(field, value) == {field: {'$eq': value}}
        assert Builder.gt_(field, value) == {field: {'$gt': value}}
        assert Builder.gte_(field, value) == {field: {'$gte': value}}
        assert Builder.in_(field, values) == {field: {'$in': values}}
        assert Builder.lt_(field, value) == {field: {'$lt': value}}
        assert Builder.lte_(field, value) == {field: {'$lte': value}}
        assert Builder.ne_(field, value) == {field: {'$ne': value}}
        assert Builder.nin_(field, values) == {field: {'$nin': values}}
        assert Builder.exists_(field, False) == {field: {'$exists': False}}
        assert Builder.exists_(field) == {field: {'$exists': True}}
        assert Builder.element_match_(field, criteria) == {field: {'$elemMatch': criteria}}
        assert Builder.regex_(field, regex) == {field: {'$regex': regex, '$options': ''}}
        assert Builder.match_(criteria) == {'$match': criteria}
        assert Builder.count_(field) == {'$count': field}
        assert Builder.limit_(page) == {'$limit': page}
        assert Builder.skip_(page) == {'$skip': page}

    def test_query_builder(self):
        """Test the query builder"""
        # preset
        preset = Query({'find': 1})
        query_builder = QueryBuilder(preset)
        assert query_builder.query == preset

        # clear
        empty = Query({})
        query_builder.clear()
        assert query_builder.query == empty

    def test_pipeline_builder(self):
        """Test the pipeline builder"""
        # preset
        preset = Pipeline([{'find': 1}])
        pipeline_builder = PipelineBuilder(preset)
        assert pipeline_builder.pipeline == preset

        # clear
        empty = Pipeline([])
        pipeline_builder.clear()
        assert pipeline_builder.pipeline == empty
