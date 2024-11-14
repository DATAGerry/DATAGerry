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
from cerberus import Validator
from flask import Blueprint, abort, request, current_app

from cmdb.manager.users_manager import UsersManager

from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.route_utils import auth_is_valid, user_has_right, parse_authorization_header
from cmdb.models.user_model.user import UserModel
from cmdb.security.token.validator import TokenValidator

from cmdb.errors.manager.user_manager import UserManagerGetError
from cmdb.errors.security import TokenValidationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 APIBlueprint - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class APIBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                                users_manager = UsersManager(current_app.database_manager)

                            token = parse_authorization_header(request.headers['Authorization'])
                            try:
                                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
                            except TokenValidationError:
                                return abort(401, "Invalid Token")

                            try:
                                user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

                                if current_app.cloud_mode:
                                    database = decrypted_token['DATAGERRY']['value']['user']['database']
                                    users_manager = UsersManager(current_app.database_manager, database)

                                user_dict: dict = UserModel.to_dict(users_manager.get_user(user_id))

                                if excepted:
                                    for exe_key, exe_value in excepted.items():
                                        try:
                                            route_parameter = kwargs[exe_value]
                                        except KeyError:
                                            return abort(403, f'User has not the required right {right}')

                                        if exe_key not in user_dict:
                                            return abort(403, f'User has not the required right {right}')

                                        if user_dict[exe_key] == route_parameter:
                                            return f(*args, **kwargs)
                            except UserManagerGetError:
                                return abort(403, "Could not retrieve user!")
                        return abort(403, f'User has not the required right {right}')

                return f(*args, **kwargs)

            return _decorate

        return _protect


    @classmethod
    def validate(cls, schema=None):
        """TODO: document"""
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
    def parse_request_parameters(cls, **optional):
        """TODO: document"""
        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                """TODO: document"""
                try:
                    request_args = request.args.to_dict()
                except Exception as error:
                    return abort(400, str(error))

                return f(request_args)

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


#TODO: CLASS-FIX
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


#TODO: CLASS-FIX
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
