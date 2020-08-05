from functools import wraps

from flask import Blueprint, abort, request

from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.route_utils import auth_is_valid


class APIBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        self.nested_blueprints = []
        super(APIBlueprint, self).__init__(*args, **kwargs)

    def protect(self, auth: bool = True, right: str = None, excepted: dict = None):
        def _protect(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                if auth and not auth_is_valid():
                    return abort(401)

                if right:
                    pass
                return f(*args, **kwargs)

            return _decorate

        return _protect

    @classmethod
    def parse_collection_parameters(cls):
        """
        Wrapper function for the flask routes.
        Auto parses the collection based parameters to the route.
        """
        def _parse(f):
            @wraps(f)
            def _decorate(*args, **kwargs):
                try:
                    params = CollectionParameters.from_http(
                        str(request.query_string, 'utf-8'), **request.args.to_dict()
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
