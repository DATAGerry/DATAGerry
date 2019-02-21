"""
Index Page
"""
from cmdb.interface.web_app import app
from cmdb.utils.error import CMDBError
from cmdb.utils import get_logger
from cmdb.utils.interface_wraps import login_required
from flask import Blueprint, render_template, request
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root

logger = get_logger()

index_pages = Blueprint('index_pages', __name__, template_folder='templates')
default_breadcrumb_root(index_pages, '.')

with app.app_context():
    MANAGER_HOLDER = app.manager_holder


@index_pages.route('/')
@index_pages.route('/dashboard/')
@register_breadcrumb(index_pages, '.', 'Home')
@login_required
def index_page():
    import json
    try:
        obm = MANAGER_HOLDER.get_object_manager()
        uum = MANAGER_HOLDER.get_user_manager()
        scm = MANAGER_HOLDER.get_security_manager()
        new_objects = obm.get_objects_by(sort='creation_time', active={"$eq": True})
        all_objects_count = len(obm.get_all_objects())
        all_types_count = len(obm.get_all_types())
        current_user_token = request.cookies['access-token']
        current_user = json.loads(scm.decrypt_token(current_user_token))
        all_user_objects_count = len(obm.get_objects_by(author_id=current_user['public_id']))
        if len(new_objects) > 25:
            new_objects = new_objects[: 25]
        last_objects = obm.get_objects_by(sort='last_edit_time', active={"$eq": True})
        if len(last_objects) > 25:
            last_objects = last_objects[: 25]
    except CMDBError as e:
        logger.warning(e.message)
        return render_template('index.html',
                               all_objects_count=all_objects_count,
                               all_types_count=all_types_count,
                               all_user_objects_count=all_user_objects_count,
                               user_manager=uum,
                               new_objects=new_objects,
                               last_objects=None)
    return render_template('index.html', all_objects_count=all_objects_count, all_types_count=all_types_count,
                           user_manager=uum, new_objects=new_objects, all_user_objects_count=all_user_objects_count,
                           last_objects=last_objects)
