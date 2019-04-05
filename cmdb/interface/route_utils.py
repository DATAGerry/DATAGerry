import json
from flask import Blueprint, request
from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.utils import json_encoding

DEFAULT_MIME_TYPE = 'Content-Type: application/json'


class NestedBlueprint:
    def __init__(self, blueprint, url_prefix):
        super(NestedBlueprint, self).__init__()
        self.blueprint = blueprint
        self.prefix = '/' + url_prefix

    def route(self, rule, **options):
        rule = self.prefix + rule
        return self.blueprint.route(rule, **options)


class RootBlueprint(Blueprint):

    def register_nested_blueprint(self, nested_blueprint):
        pass


def make_response(instance: (CmdbDAO, list, dict)):
    """
    make json http response with indent settings and auto encoding
    Args:
        instance: instance of a cmdbDao instance or instance of the subclass

    Returns:
        http valid response
    """
    from flask import make_response as flask_response
    # set indent to None of min value exists in the request - DEFAULT: 2 steps
    indent = None if 'min' in request.args else 2
    # encode the dict data from the object to json data
    resp = flask_response(json.dumps(instance, default=json_encoding.default, indent=indent))
    # add header informations
    resp.mimetype = DEFAULT_MIME_TYPE
    return resp
