# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

from functools import wraps
import logging

from cerberus import Validator
from flask import Blueprint, abort, request, current_app

from cmdb.manager import ManagerGetError
from cmdb.interface.api_parameters import CollectionParameters, APIParameters
from cmdb.interface.route_utils import auth_is_valid, user_has_right, parse_authorization_header
from cmdb.security.token.validator import TokenValidator, ValidationError
from cmdb.user_management import UserModel
from cmdb.user_management.managers.user_manager import UserManager

LOGGER = logging.getLogger(__name__)

class APIBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        super(APIBlueprint, self).__init__(*args, **kwargs)

    @staticmethod
    def protect(auth: bool = True, right: str = None, excepted: dict = None):
        """Active auth and right protection for flask routes"""

        def _protect(f):
            @wraps(f)
            def _decorate(*args, **kwargs):

                if auth:
                    if not auth_is_valid():
                        return abort(401)

                if auth and right:
                    if not user_has_right(right):
                        if excepted:
                            with current_app.app_context():
                                user_manager = UserManager(current_app.database_manager)

                            token = parse_authorization_header(request.headers['Authorization'])
                            try:
                                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
                            except ValidationError as err:
                                return abort(401)
                            try:
                                user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']
                                user_dict: dict = UserModel.to_dict(user_manager.get(user_id))

                                if excepted:
                                    for exe_key, exe_value in excepted.items():
                                        try:
                                            route_parameter = kwargs[exe_value]
                                        except KeyError:
                                            return abort(403, f'User has not the required right {right}')

                                        if exe_key not in user_dict.keys():
                                            return abort(403, f'User has not the required right {right}')

                                        if user_dict[exe_key] == route_parameter:
                                            return f(*args, **kwargs)
                            except ManagerGetError:
                                return abort(404)
                        return abort(403, f'User has not the required right {right}')

                return f(*args, **kwargs)

            return _decorate

        return _protect

    @classmethod
    def validate(cls, schema=None):
        validator = Validator(schema, purge_unknown=True)

        def _validate(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                data = request.get_json()
                try:
                    validation_result = validator.validate(data)
                except Exception as err:
                    return abort(400, str(err))
                if not validation_result:
                    return abort(400, {'validation_error': validator.errors})
                return f(data=validator.document, *args, **kwargs)

            return _decorate

        return _validate

    @classmethod
    def parse_parameters(cls, parameters_class, **optional):
        """
        Parse generic parameters from http to a class
        Args:
            parameters_class: Wrapper class of the ApiParameters
            **optional: Dynamic route parameters

        Returns:
            APIParameters: Wrapper class
        """

        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                try:
                    params = parameters_class.from_http(
                        str(request.query_string, 'utf-8'), **{**optional, **request.args.to_dict()}
                    )
                except Exception as e:
                    return abort(400, str(e))
                return f(params=params, *args, **kwargs)

            return _decorate

        return _parse

    @classmethod
    def parse_location_parameters(cls, **optional):
        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):

                try:
                    locationArgs = request.args.to_dict()
                except Exception as error:
                    return abort(400, str(error))
                return f(locationArgs)
            return _decorate
        return _parse

    @classmethod
    def parse_collection_parameters(cls, **optional):
        """
        Wrapper function for the flask routes.
        Auto parses the collection based parameters to the route.

        TODO:
            Move to global method like up.

        Args:
            **optional: dict of optional collection parameters for given route function.
        """

        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                try:
                    params = CollectionParameters.from_http(
                        str(request.query_string, 'utf-8'), **{**optional, **request.args.to_dict()}
                    )
                except Exception as e:
                    return abort(400, str(e))
                return f(params=params, *args, **kwargs)

            return _decorate

        return _parse


class RootBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        super(RootBlueprint, self).__init__(*args, **kwargs)
        self.nested_blueprints = []

    def register_nested_blueprint(self, nested_blueprint):
        """Add a 'sub' blueprint to root element
        Args:
            nested_blueprint (NestedBlueprint): Blueprint for sub routes
        """
        self.nested_blueprints.append(nested_blueprint)


class NestedBlueprint:
    """Default Blueprint class but with parent prefix route
    """

    def __init__(self, blueprint, url_prefix):
        self.blueprint = blueprint
        self.prefix = '/' + url_prefix
        super(NestedBlueprint, self).__init__()

    def route(self, rule, **options):
        rule = self.prefix + rule
        return self.blueprint.route(rule, **options)
