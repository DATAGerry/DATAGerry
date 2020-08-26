from functools import wraps

from cerberus import Validator
from flask import Blueprint, abort, request

from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.route_utils import auth_is_valid, user_has_right


class APIBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        self.nested_blueprints = []
        super(APIBlueprint, self).__init__(*args, **kwargs)

    @staticmethod
    def protect(auth: bool = True, right: str = None):
        """Active auth and right protection for flask routes"""

        def _protect(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                if auth and not auth_is_valid():
                    return abort(401)

                if right and not user_has_right(right):
                    return abort(401)
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
    def parse_collection_parameters(cls, **optional):
        """
        Wrapper function for the flask routes.
        Auto parses the collection based parameters to the route.

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

    def register_nested_blueprint(self, nested_blueprint):
        """Add a 'sub' blueprint to root element
        Args:
            nested_blueprint (NestedBlueprint): Blueprint for sub routes
        """
        self.nested_blueprints.append(nested_blueprint)


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
