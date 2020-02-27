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

import pytest
import unittest

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.search.searchers import SearcherFramework


def setup_module(module):
    print("setup module functional search")


def teardown_module(module):
    print("teardown module functional search")


@pytest.mark.usefixtures("database_manager_class")
@pytest.mark.usefixtures("object_manager_class")
class TestSearch(unittest.TestCase):

    def setUp(self):
        self.database_manager: DatabaseManagerMongo = self.database_manager

    def tearDown(self):
        self.database_manager.delete_collection('framework.objects')

    def test_search(self):
        searcher = SearcherFramework(self.object_manager)
        # result = searcher.search(query)
        assert 1 == 1

