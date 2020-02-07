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

from typing import List


class AuthProviderConfigFormEntry:
    """Frontend config element"""

    def __init__(self, name: str, type: str, description: str = None, default=None, **kwargs):
        self.name = name
        self.label = self.name.title().replace("_", " ")
        self.type = type
        self.description = description
        self.default = default
        for key in kwargs:
            setattr(self, key, kwargs[key])


class AuthProviderConfigFormSection:
    """Frontend config section"""

    def __init__(self, name: str, label: str = None, entries: List[AuthProviderConfigFormEntry] = None,
                 sections: List['AuthProviderConfigFormSection'] = None):
        self.name = name
        self.label = label or self.name.title().replace("_", " ")
        self.entries: List[AuthProviderConfigFormEntry] = entries or []
        self.sections: List['AuthProviderConfigFormSection'] = sections or []


class AuthProviderConfigForm:
    """Form wrapper for frontend config"""

    DEFAULT_CONFIG_FORM = {
        'entries': [
            AuthProviderConfigFormEntry(name='active', type='checkbox')
        ]
    }

    def __init__(self, entries: List[AuthProviderConfigFormEntry] = None,
                 sections: List[AuthProviderConfigFormSection] = None):
        self.entries: List[AuthProviderConfigFormEntry] = entries or []
        self.sections: List[AuthProviderConfigFormSection] = sections or []

    def add_entry(self, entry: AuthProviderConfigFormEntry):
        self.entries.append(entry)

    def remove_entry(self, entry: AuthProviderConfigFormEntry):
        self.entries.remove(entry)

    def add_section(self, section: AuthProviderConfigFormSection):
        self.sections.append(section)

    def remove_section(self, section: AuthProviderConfigFormSection):
        self.sections.remove(section)
