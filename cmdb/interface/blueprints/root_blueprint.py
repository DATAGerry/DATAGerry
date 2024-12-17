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
from functools import wraps
import logging
from flask import Blueprint, abort, request
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 RootBlueprint - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class RootBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nested_blueprints = []

    def register_nested_blueprint(self, nested_blueprint):
        """Add a 'sub' blueprint to root element
        Args:
            nested_blueprint (NestedBlueprint): Blueprint for sub routes
        """
        self.nested_blueprints.append(nested_blueprint)


    @classmethod
    def parse_assistant_parameters(cls, **optional):
        """TODO: document"""
        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                try:
                    location_args = request.args.to_dict()
                except Exception as error:
                    return abort(400, str(error))

                return f(location_args)

            return _decorate

        return _parse
