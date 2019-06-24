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


@pytest.mark.usefixtures("key_holder")
def test_key_gen(key_holder):
    from cmdb.security.token import TokenGenerator
    token_gen = TokenGenerator(key_holder=key_holder)
    token = token_gen.generate_token({'test': 'test'})
    token_gen.validate_token_claims(token)
    assert 1 == 1
