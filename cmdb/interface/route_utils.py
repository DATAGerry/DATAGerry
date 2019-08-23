# dataGerry - OpenSource Enterprise CMDB
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

import json

from flask import Blueprint, request

from cmdb.framework.cmdb_dao import CmdbDAO
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

    def __init__(self, *args, **kwargs):
        super(RootBlueprint, self).__init__(*args, **kwargs)
        self.nested_blueprints = []

    def register_nested_blueprint(self, nested_blueprint):
        self.nested_blueprints.append(nested_blueprint)


def make_response(instance: (CmdbDAO, list, dict), status_code=200):
    """
    make json http response with indent settings and auto encoding
    Args:
        instance: instance of a cmdbDao instance or instance of the subclass
        status_code: optional status code
    Returns:
        http valid response
    """
    from flask import make_response as flask_response
    # set indent to None of min value exists in the request - DEFAULT: 2 steps
    indent = None if 'min' in request.args else 2
    # encode the dict data from the object to json data
    resp = flask_response(json.dumps(instance, default=json_encoding.default, indent=indent), status_code)
    # add header informations
    resp.mimetype = DEFAULT_MIME_TYPE
    return resp
