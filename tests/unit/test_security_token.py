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


class TestTokenGenerator:

    def test_token_generation(self):
        from cmdb.security.token.generator import TokenGenerator
        from cmdb.security.token.validator import TokenValidator
        token_gen = TokenGenerator()
        token_validator = TokenValidator()
        token = token_gen.generate_token(payload={'test': 'test'})
        print(token_validator.validate_token(token))
