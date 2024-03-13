# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: ducoment"""

def boolify(s):
    """TODO: ducoment"""
    if s in ('True', 'true'):
        return True

    if s in ('False', 'false'):
        return False

    raise ValueError('Not Boolean Value!')


def noneify(s):
    """TODO: ducoment"""
    if s in ('None', 'null'):
        return None

    raise ValueError('Not None Value!')


def auto_cast(val):
    """TODO: ducoment"""
    for caster in (boolify, int, noneify, float, str):
        try:
            return caster(val)
        except ValueError:
            pass

    return val
