from cmdb.utils.interface_wraps import login_required
from cmdb.utils import get_logger
from flask import Blueprint, render_template
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.object_framework import CmdbRender

LOGGER = get_logger()

object_pages = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object')
default_breadcrumb_root(object_pages, '.object_pages')

obm = MANAGER_HOLDER.get_object_manager()


@object_pages.route('/')
@object_pages.route('/list')
@register_breadcrumb(object_pages, '.', 'Objects')
def list_page():
    uum = MANAGER_HOLDER.get_user_manager()
    all_objects = obm.get_all_objects()
    return render_template('objects/list.html', object_manager=obm, user_manager=uum, all_objects=all_objects)


@object_pages.route('/type/<int:type_id>/add')
@object_pages.route('/type/<int:type_id>/add/')
@register_breadcrumb(object_pages, '.add', 'Add')
def add_new_page(type_id):
    object_type = obm.get_type(type_id)
    status_list = obm.get_status_by_type(type_id)
    return render_template('objects/add.html', object_type=object_type, status_list=status_list)


@object_pages.route('/<int:public_id>')
@register_breadcrumb(object_pages, '.view', 'View')
def view_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_object.update_view_counter()
    ack = MANAGER_HOLDER.get_object_manager().update_object(view_object.to_database())
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbRender(view_object, view_type)

    return render_template('objects/view.html',
                           object_base=object_base,
                           author_name=author_name,
                           view_object=view_object,
                           view_type=view_type,
                           render=render
                           )


@object_pages.route('<int:public_id>/edit/')
@register_breadcrumb(object_pages, '.edit', 'Edit')
def edit_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbRender(view_object, view_type, mode=CmdbRender.EDIT_MODE)

    return render_template('objects/view.html',
                           object_base=object_base,
                           author_name=author_name,
                           view_object=view_object,
                           view_type=view_type,
                           render=render
                           )
