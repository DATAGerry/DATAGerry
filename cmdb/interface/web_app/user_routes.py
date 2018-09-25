"""
User Pages
"""
from cmdb.utils.interface_wraps import right_required
from cmdb.utils import get_logger
from flask import Blueprint, render_template, abort
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER

LOGGER = get_logger()

user_pages = Blueprint('user_pages', __name__, template_folder='templates', url_prefix='/user')
default_breadcrumb_root(user_pages, '.user_pages')


@user_pages.route('/')
@register_breadcrumb(user_pages, '.', 'User')
def user_base():
    abort(404)


@user_pages.route('/<int:public_id>')
@register_breadcrumb(user_pages, '.profile', 'Profile')
def user_profile_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    view_user = usm.get_user(public_id=public_id)
    return render_template('user/profile.html', view_user=view_user)


