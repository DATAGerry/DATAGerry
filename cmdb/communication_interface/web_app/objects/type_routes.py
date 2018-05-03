from flask import Blueprint, render_template
from cmdb.communication_interface.web_app.utils import Pagination
type_pages = Blueprint('type_pages', __name__, template_folder='templates', url_prefix='/type')


@type_pages.route("/<int:public_id>", defaults={'page': 1})
@type_pages.route("/<int:public_id>/<int:page>")
def view_type_list(public_id: int, page):
    from cmdb.application_utils import SYSTEM_SETTINGS_READER
    pagi_steps = int(SYSTEM_SETTINGS_READER.get_value('pagination_step', 'frontend'))
    from cmdb.object_framework import OBJECT_MANAGER
    selected_type = OBJECT_MANAGER.get_type(public_id=public_id)
    type_objects = OBJECT_MANAGER.get_objects_by_type(type_id=public_id)
    type_object_list = [type_objects[i:i+pagi_steps] for i in range(0, len(type_objects), pagi_steps)]
    pagination = Pagination(page, pagi_steps, len(type_objects))
    return render_template('view_type_list.html', type=selected_type, objects=type_object_list[page-1],
                           object_counts=len(type_objects), page=pagination)
