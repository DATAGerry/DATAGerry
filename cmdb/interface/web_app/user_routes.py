"""
User Pages
"""
import logging
from cmdb.utils.interface_wraps import right_required, login_required
from cmdb.utils.error import CMDBError
from flask import Blueprint, render_template, request
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
import json

LOGGER = logging.getLogger(__name__)

user_pages = Blueprint('user_pages', __name__, template_folder='templates', url_prefix='/user')
default_breadcrumb_root(user_pages, '.user_pages')


@user_pages.route('/')
@login_required
@register_breadcrumb(user_pages, '.', 'User')
def user_base():
    scm = MANAGER_HOLDER.get_security_manager()
    current_user_token = request.cookies['access-token']
    current_user = json.loads(scm.decrypt_token(current_user_token))
    LOGGER.debug("Current user: {}, type: {}".format(current_user, type(current_user)))
    LOGGER.debug("Profil user id: {}".format(current_user['public_id']))
    return user_profile_page(current_user['public_id'])


@user_pages.route('/<int:public_id>')
@login_required
@register_breadcrumb(user_pages, '.profile', 'Profile')
def user_profile_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    view_user = usm.get_user(public_id=public_id)
    user_group = usm.get_group(view_user.get_group())
    group_rights = []
    for right in user_group.get_rights():
        try:
            group_rights.append(usm.get_right_by_name(right['name']))
        except CMDBError as e:
            LOGGER.debug(e.message)
            continue
    return render_template('user/profile.html',
                           view_user=view_user,
                           user_group=user_group,
                           group_rights=group_rights)
