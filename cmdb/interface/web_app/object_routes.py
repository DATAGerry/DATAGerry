from cmdb.utils.interface_wraps import login_required
from cmdb.utils import get_logger
from flask import Blueprint, render_template, abort
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.object_framework import CmdbRender

LOGGER = get_logger()

object_pages = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object')
default_breadcrumb_root(object_pages, '.object_pages')


@object_pages.route('/')
@register_breadcrumb(object_pages, '.', 'Objects')
@login_required
def root_object_page():
    abort(404)


@object_pages.route('/<int:public_id>')
@register_breadcrumb(object_pages, '.Objects', 'View')
@login_required
def view_page(public_id):
    obm = MANAGER_HOLDER.get_object_manager()
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbRender(view_object, view_type)

    return render_template('objects/view.html',
                           object_base=object_base,
                           author_name=author_name,
                           view_object=view_object,
                           view_type=view_type,
                           render_form=render.render_html_form(CmdbRender.VIEW_MODE)
                           )
