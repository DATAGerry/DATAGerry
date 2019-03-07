"""
Admin/Settings Pages
"""
import logging
from cmdb.utils.error import CMDBError
from cmdb.interface.cmdb_holder import CmdbManagerHolder
from flask import Blueprint, render_template, jsonify, current_app
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from flask import request, abort

LOGGER = logging.getLogger(__name__)

settings_pages = Blueprint('settings_pages', __name__, template_folder='templates', url_prefix='/settings')
default_breadcrumb_root(settings_pages, '.settings_pages')

with current_app.app_context():
    MANAGER_HOLDER = CmdbManagerHolder()
    MANAGER_HOLDER = current_app.manager_holder


@settings_pages.route('/')
@register_breadcrumb(settings_pages, '.', 'Settings')
def settings_page():
    return render_template('settings/default.html')


@settings_pages.route('/user-management/', methods=['GET'])
@register_breadcrumb(settings_pages, '.user_management', 'User Management')
def user_management_index():
    user_manager_instance = MANAGER_HOLDER.get_user_manager()
    user_submit_token = 'TODO'
    return render_template('settings/user_management/index.html', user_manager=user_manager_instance,
                           user_submit_token=user_submit_token)


@settings_pages.route('/user-management/add_user/', methods=['POST'])
@register_breadcrumb(settings_pages, '.user_management.add_user', 'Add new user')
def user_management_add_user():
    """
    TODO: Add submit token validation
    Returns:

    """
    from cmdb.user_management.user import User
    from cmdb.user_management.user_manager import UserInsertError
    from datetime import datetime
    user_manager_instance = MANAGER_HOLDER.get_user_manager()
    security_manager_instance = MANAGER_HOLDER.get_security_manager()
    database_manager_instance = MANAGER_HOLDER.get_database_manager()
    add_user = None
    error = None
    if request.method != 'POST':
        abort(500)

    form_data = request.form.to_dict()
    form_data = {k: v for k, v in form_data.items() if v is not ''}

    # Add application side data
    form_data['registration_time'] = datetime.utcnow()
    form_data['group_id'] = int(form_data['group_id'])
    form_data['authenticator'] = 'LocalAuthenticationProvider'
    form_data['password'] = security_manager_instance.generate_hmac(form_data['password'])
    form_data['public_id'] = database_manager_instance.get_highest_id(collection=User.COLLECTION) + 1

    user_submit_token = 'TODO'
    LOGGER.debug("User add data: {}".format(form_data))
    try:
        add_user = User(**form_data)
        user_manager_instance.insert_user(add_user)
    except UserInsertError as e:
        error = e
        LOGGER.error("Error while adding user into database: {}".format(e.message))
    except CMDBError as e:
        error = e
        LOGGER.error("Error while init user for adding into database: {}".format(form_data))

    return render_template('settings/user_management/add_user.html', add_user=add_user,
                           user_submit_token=user_submit_token, error=error)


@settings_pages.route('/user-management/groups/', methods=['GET'])
@register_breadcrumb(settings_pages, '.user_management.groups', 'Groups')
def user_management_groups():
    """
    TODO: IMPLEMENT EDIT GROUPS
    """
    user_manager_instance = MANAGER_HOLDER.get_user_manager()
    group_list = user_manager_instance.get_all_groups()
    right_list = user_manager_instance._load_rights()
    return render_template('settings/user_management/groups.html', user_manager=user_manager_instance,
                           group_list=group_list, right_list=right_list)


@settings_pages.route('/user-management/groups/<int:public_id>/rights/', methods=['POST'])
def user_management_group_right_change(public_id):

    def _convert_to_list(form_rights: dict):
        convert_list = []
        for confirm_right in form_rights:
            convert_list.append(confirm_right)
        return convert_list

    user_manager_instance = MANAGER_HOLDER.get_user_manager()
    right_list = _convert_to_list(request.form.to_dict())
    try:
        choosen_group = user_manager_instance.get_group(public_id)
        choosen_group.set_rights(right_list)
        user_manager_instance.update_group(choosen_group)
    except CMDBError as e:
        return jsonify({"error": e.message})
    return jsonify(right_list)


@settings_pages.route('/user-management/rights/', methods=['GET'])
@register_breadcrumb(settings_pages, '.user_management.rights', 'Rights')
def user_management_rights():
    user_manager_instance = MANAGER_HOLDER.get_user_manager()
    right_list = user_manager_instance._load_rights()
    from cmdb.user_management.user_right import GLOBAL_IDENTIFIER, BaseRight
    security_levels = BaseRight._nameToLevel
    global_right_ident = GLOBAL_IDENTIFIER
    return render_template('settings/user_management/rights.html', user_manager=user_manager_instance,
                           right_list=right_list, global_right_ident=global_right_ident,
                           security_levels=security_levels)


@settings_pages.route('/type-config/')
@register_breadcrumb(settings_pages, '.type_config', 'Type config')
def type_config_page():
    from cmdb.utils.example_data import list_example_files
    possible_example_files = list_example_files()
    return render_template('settings/type_config.html', possible_example_files=possible_example_files)


@settings_pages.route('/type-config/_load_example_data/', methods=['POST'])
def _type_config_load_example_data_ajax():
    """
    TODO: FIX BSON ENCODING ERROR
    TODO: ADD RESULT IN HTML
    Returns:

    """
    from cmdb.utils.example_data import import_example_data
    selected_data_files = request.form.getlist('example_data_files')
    if len(selected_data_files) > 0:
        imports = import_example_data(selected_data_files)
        LOGGER.debug(imports)
    return jsonify({'result': imports})


@settings_pages.route('/security/', methods=['GET'])
@register_breadcrumb(settings_pages, '.security_settings', 'Security Settings')
def security_page_get():
    ssr = MANAGER_HOLDER.get_system_settings_reader()
    data = ssr.get_all_values_from_section('security')[0]
    return render_template('settings/security.html', data=data)


@settings_pages.route('/security/', methods=['POST'])
@register_breadcrumb(settings_pages, '.security_settings', 'Security Settings')
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
