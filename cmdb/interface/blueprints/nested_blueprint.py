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
"""TODO: document"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                NestedBlueprint - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class NestedBlueprint:
    """Default Blueprint class but with parent prefix route
    """
    def __init__(self, blueprint, url_prefix):
        self.blueprint = blueprint
        self.prefix = '/' + url_prefix
        super().__init__()


    def route(self, rule, **options):
        """TODO: document"""
        rule = self.prefix + rule
        return self.blueprint.route(rule, **options)
