import logging
from cmdb.utils.interface_wraps import login_required
from flask import Blueprint, render_template, abort, request
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.utils.error import CMDBError
from cmdb.interface.interface_parser import InterfaceParser
from cmdb.interface.web_app import app

LOGGER = logging.getLogger(__name__)

type_pages = Blueprint('type_pages', __name__, template_folder='templates', url_prefix='/type')
default_breadcrumb_root(type_pages, '.type_pages')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@type_pages.route('/')
@register_breadcrumb(type_pages, '.', 'Type')
def index_page():
    all_types = MANAGER_HOLDER.get_object_manager().get_all_types()
    return render_template('types/index.html', all_types=all_types)


@type_pages.route('/<int:public_id>')
@type_pages.route('/view/<int:public_id>')
@register_breadcrumb(type_pages, '.Type', 'View')
@login_required
def view_page(public_id):
    type_instance = None
    render = None
    try:
        type_instance = MANAGER_HOLDER.get_object_manager().get_type(public_id=public_id)
        render = InterfaceParser(type_instance, mode=InterfaceParser.SHOW_MODE)
    except CMDBError as e:
        LOGGER.warning(e.message)
        abort(500)
    return render_template('types/view.html', public_id=public_id, type_instance=type_instance, render=render,
                           user_manager=MANAGER_HOLDER.get_user_manager())


@type_pages.route('/edit/<int:public_id>')
@type_pages.route('/edit/<int:public_id>/')
@register_breadcrumb(type_pages, '.Type', 'Edit')
def edit_page(public_id):
    current_type = None
    try:
        current_type = MANAGER_HOLDER.get_object_manager().get_type(public_id=public_id)
    except CMDBError as e:
        LOGGER.warning(e.message)

    return render_template('types/edit.html', public_id=public_id, type=current_type)
