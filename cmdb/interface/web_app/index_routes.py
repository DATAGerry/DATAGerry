"""
Index Page
"""
from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.object_framework import CMDBError
from cmdb.utils import get_logger
from cmdb.utils.interface_wraps import login_required
from flask import Blueprint
from flask import render_template
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root

# from flask import current_app

logger = get_logger()

index_pages = Blueprint('index_pages', __name__, template_folder='templates')
default_breadcrumb_root(index_pages, '.')


@index_pages.route('/')
@index_pages.route('/dashboard')
@register_breadcrumb(index_pages, '.', 'Home')
@login_required
def index_page():
    try:
        obm = MANAGER_HOLDER.get_object_manager()
        uum = MANAGER_HOLDER.get_user_manager()
        new_objects = obm.get_objects_by(sort='creation_time', active={"$eq": True})[:25]
        last_objects = obm.get_objects_by(sort='last_edit_time', active={"$eq": True})[:25]
    except CMDBError as cmdb_e:
        logger.warning(cmdb_e.message)
        return render_template('index.html', object_manager=obm, user_manager=uum, new_objects=new_objects,
                               last_objects=None)
    return render_template('index.html', object_manager=obm, user_manager=uum, new_objects=new_objects,
                           last_objects=last_objects)
