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

from cmdb.plugins.plugin_system import PluginBase
from cmdb.security.auth.auth_errors import AuthenticationProviderNotExistsError
from cmdb.security.auth import AuthenticationProvider


class AuthPluginBase(PluginBase):

    def __init__(self, plugin_name: str, provider_class):
        if not issubclass(provider_class, AuthenticationProvider):
            raise AuthenticationProviderNotExistsError(provider_class)
        self.provider_class = provider_class
        super(PluginBase, self).__init__(plugin_name, 'auth')

    def get_provider_class(self):
        return self.provider_class
