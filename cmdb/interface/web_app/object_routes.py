from cmdb.utils.interface_wraps import login_required
from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.object_framework.cmdb_object_field_type import FieldNotFoundError
from cmdb.utils import get_logger
from cmdb.utils.error import CMDBError
from flask import Blueprint, render_template, request, make_response
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.object_framework import CmdbRender
import datetime
import json

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


def page_view(public_id, mode):
    pass  # TODO: refactor view + edit together


@object_pages.route('/<int:public_id>')
@object_pages.route('/<int:public_id>/')
@register_breadcrumb(object_pages, '.view', 'View')
@login_required
def view_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_object.update_view_counter()
    try:
        obm.update_object(view_object)
    except CMDBError:
        pass
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbRender(view_object, view_type)
    references = obm.get_object_references(public_id)

    return render_template('objects/view.html',
                           object_base=object_base,
                           author_name=author_name,
                           user_manager=usm,
                           view_object=view_object,
                           view_type=view_type,
                           references=references,
                           render=render
                           )


@object_pages.route('<int:public_id>/edit/', methods=['GET'])
@register_breadcrumb(object_pages, '.edit', 'Edit')
def edit_page_get(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbRender(view_object, view_type, mode=CmdbRender.EDIT_MODE)

    return render_template('objects/edit.html',
                           object_base=object_base,
                           author_name=author_name,
                           user_manager=usm,
                           view_object=view_object,
                           view_type=view_type,
                           render=render
                           )


@object_pages.route('<int:public_id>/edit/', methods=['POST'])
@register_breadcrumb(object_pages, '.edit', 'Edit')
@login_required
def edit_page_post(public_id):
    from cmdb.object_framework.cmdb_log import CmdbLog
    old_object = obm.get_object(public_id=public_id)
    new_object = None
    error = None
    if request.method != 'POST':
        error = ObjectUpdateError('Wrong HTTP Method')
        return render_template('objects/post_edit.html', old_object=old_object, new_object=new_object, error=error)
    form_data = request.form.to_dict()
    try:
        log_message = form_data['log_message']
        del form_data['log_message']
        LOGGER.debug("Form data: {}".format(form_data))

        old_field_values = old_object.get_all_fields()
        LOGGER.debug('Old field values type {} | data {} '.format(type(old_field_values), old_field_values))
        log_state = obm.generate_log_state(old_field_values)
        LOGGER.debug('Log state values type {} | data {} '.format(type(log_state), log_state))
        new_object = old_object

        new_object.add_last_log_state(log_state)

        scm = MANAGER_HOLDER.get_security_manager()
        current_user_token = request.cookies['access-token']
        current_user = json.loads(scm.decrypt_token(current_user_token))

        edit_time = datetime.datetime.utcnow()
        # User Type cast with public id check for validation

        new_log = CmdbLog(
            author_id=MANAGER_HOLDER.get_user_manager().get_user(current_user['public_id']).get_public_id(),
            action='edit',
            message=log_message,
            date=edit_time
        )
        new_object.add_log(new_log)
        new_object.last_edit_time = edit_time
        for new_value in form_data:
            try:
                new_object.set_value(new_value, form_data[new_value])
            except FieldNotFoundError:
                new_object.set_new_value(new_value, form_data[new_value])
        new_object._update_version(CmdbDAO.VERSIONING_MINOR)

    except (CMDBError, Exception) as e:
        error = ObjectUpdateError("Error during new object generation - {}".format(e))
    LOGGER.debug('New object {}'.format(new_object))
    if error is None:
        try:
            obm.update_object(new_object)
        except (CMDBError, Exception) as e:
            error = ObjectUpdateError("Update error while inserting into database: {}".format(e))
    return render_template('objects/post_edit.html', old_object=old_object, new_object=new_object, error=error)


class ObjectUpdateError(CMDBError):
    def __init__(self, msg):
        self.message = 'Something went wrong during update: {}'.format(msg)
