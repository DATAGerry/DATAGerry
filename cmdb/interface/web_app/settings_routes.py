"""
Admin/Settings Pages
"""
from cmdb.utils.interface_wraps import right_required
from cmdb.utils import get_logger
from flask import Blueprint, render_template
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from flask import request, abort

LOGGER = get_logger()

settings_pages = Blueprint('settings_pages', __name__, template_folder='templates', url_prefix='/settings')
default_breadcrumb_root(settings_pages, '.settings_pages')


@right_required
@settings_pages.route('/')
@register_breadcrumb(settings_pages, '.', 'Settings')
def settings_page():
    return render_template('settings/default.html')


@right_required
@settings_pages.route('/user/')
@register_breadcrumb(settings_pages, '.settings_page', 'User Management')
def user_page():
    usm = MANAGER_HOLDER.get_user_manager()
    complete_user_list = usm.get_all_users()
    user_list = []
    dict_filter = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    formatter = ('public_id', 'user_name', 'first_name', 'last_name', 'registration_time')
    for user_element in complete_user_list:
        user_buffer = dict_filter(user_element, formatter)
        user_buffer['group_name'] = usm.get_group(user_element['group_id']).get_name()
        user_list.append(user_buffer)

    return render_template('settings/user.html', user_list=user_list)


@settings_pages.route('/security/', methods=['GET'])
@register_breadcrumb(settings_pages, '.settings_page', 'Security Settings')
def security_page_get():
    ssr = MANAGER_HOLDER.get_system_settings_reader()
    data = ssr.get_all_values_from_section('security')[0]
    return render_template('settings/security.html', data=data)


@settings_pages.route('/security/', methods=['POST'])
@register_breadcrumb(settings_pages, '.settings_page', 'Security Settings')
def security_page_post():
    if request.method == 'POST':
        ssr = MANAGER_HOLDER.get_system_settings_reader()
        ssw = MANAGER_HOLDER.get_system_settings_writer()
        form_data = request.form.to_dict()
        try:
            ssw.update('security', form_data)
        except Exception as e:
            LOGGER.critical(e)
            abort(500)
        data = ssr.get_all_values_from_section('security')[0]
        return render_template('settings/security.html', data=data)
    else:
        abort(400)
