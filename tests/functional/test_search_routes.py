# Net|CMDB - OpenSource Enterprise CMDB
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


@pytest.mark.usefixtures("client", "init_config_reader")
class TestSeach:

    def test_text_search(self, client, init_config_reader):
        resp = client.get('/search/green')
        assert resp.status_code == 200

    def test_get_search(self, client, init_config_reader):
        resp = client.get('/search/?value=green')
        assert resp.status_code == 200

    def test_get_search_limit(self, client, init_config_reader):
        resp = client.get('/search/?value=green&limit=2')
        assert resp.status_code == 200

