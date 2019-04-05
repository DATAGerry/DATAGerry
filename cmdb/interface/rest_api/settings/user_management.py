from cmdb.interface.route_utils import NestedBlueprint
from cmdb.interface.rest_api.settings_routes import settings_rest

user_management_routes = NestedBlueprint(settings_rest, url_prefix='/user-management')


@user_management_routes.route('/', methods=['GET'])
def test2():
    return "test23"
