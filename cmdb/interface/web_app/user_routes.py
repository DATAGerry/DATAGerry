"""
User Pages
"""
import logging
import json
from cmdb.utils.interface_wraps import login_required
from flask import Blueprint, render_template, request, url_for, redirect
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)

user_pages = Blueprint('user_pages', __name__, template_folder='templates', url_prefix='/user')
default_breadcrumb_root(user_pages, '.user_pages')


@user_pages.route('/')
@register_breadcrumb(user_pages, '.', 'User')
@login_required
def user_base():
    scm = MANAGER_HOLDER.get_security_manager()
    current_user_token = request.cookies['access-token']
    current_user = json.loads(scm.decrypt_token(current_user_token))
    return redirect(url_for('user_pages.user_profile_page', public_id=current_user['public_id']))


@user_pages.route('/password/')
def new_password_request():
    return "test"


@user_pages.route('/<int:public_id>/')
@register_breadcrumb(user_pages, '.profile', 'Profile')
@login_required
def user_profile_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    view_user = usm.get_user(public_id=public_id)
    user_group = usm.get_group(view_user.get_group())
    authentication_provider = usm.get_authentication_provider(view_user.get_authenticator())
    return render_template('user/profile.html',
                           edit_able=False,
                           view_user=view_user,
                           user_group=user_group,
                           provider=authentication_provider
                           )


@user_pages.route('/<int:public_id>/edit/')
@register_breadcrumb(user_pages, '.edit', 'Profile Edit')
@login_required
def user_profile_page_edit(public_id,):
    usm = MANAGER_HOLDER.get_user_manager()
    view_user = usm.get_user(public_id=public_id)
    user_group = usm.get_group(view_user.get_group())
    authentication_provider = usm.get_authentication_provider(view_user.get_authenticator())
    return render_template('user/profile.html',
                           edit_able=True,
                           view_user=view_user,
                           user_group=user_group,
                           provider=authentication_provider
                           )
