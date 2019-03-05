from cmdb.utils.interface_wraps import login_required
from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.object_framework.cmdb_object_field_type import FieldNotFoundError
from cmdb.object_framework.cmdb_object_manager import ObjectInsertError, ObjectUpdateError
from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_log import CmdbLog
from cmdb.utils import get_logger
from cmdb.utils.error import CMDBError
from flask import Blueprint, render_template, request, abort
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.object_framework import CmdbParser
from cmdb.event_management.event import Event
import datetime
import json

LOGGER = get_logger()

object_pages = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object')
default_breadcrumb_root(object_pages, '.object_pages')

obm = MANAGER_HOLDER.get_object_manager()


@object_pages.route('/')
@object_pages.route('/list')
@register_breadcrumb(object_pages, '.', 'Objects')
@login_required
def list_page():
    uum = MANAGER_HOLDER.get_user_manager()
    # ToDo: event sending does not make sense here, is just for testing
    evm = MANAGER_HOLDER.get_event_queue()
    event = Event("cmdb.core.objects.listed", {})
    evm.put(event)
    all_objects = obm.get_all_objects()
    return render_template('objects/list.html', object_manager=obm, user_manager=uum, all_objects=all_objects)


@object_pages.route('/type/<int:type_id>/add', methods=['GET'])
@object_pages.route('/type/<int:type_id>/add/', methods=['GET'])
@register_breadcrumb(object_pages, '.add', 'Add')
@login_required
def add_new_page(type_id):
    try:
        object_type = obm.get_type(type_id)
    except (CMDBError, Exception) as e:
        LOGGER.critical(e)
        abort(500, e.message)
    try:
        status_list = obm.get_status_by_type(type_id)
    except (CMDBError, Exception):
        status_list = []

    render = CmdbParser(type_instance=object_type, mode=CmdbParser.ADD_MODE)
    return render_template('objects/add.html', render=render, status_list=status_list)


@object_pages.route('/type/<int:type_id>/add', methods=['POST'])
@object_pages.route('/type/<int:type_id>/add/', methods=['POST'])
@register_breadcrumb(object_pages, '.add', 'Add')
@login_required
def add_new_page_post(type_id):
    error = None
    object_type = None
    form_data = request.form.to_dict()
    LOGGER.debug("Object insert FORM_DATA: {}".format(form_data))
    log_message = None
    if form_data['log_message']:
        log_message = form_data['log_message']
        del form_data['log_message']
    inserted_object = None

    try:
        try:
            object_type = obm.get_type(type_id)
            scm = MANAGER_HOLDER.get_security_manager()
            current_user_token = request.cookies['access-token']
            current_user = json.loads(scm.decrypt_token(current_user_token))
            insert_data = []
            for value_key in form_data:
                insert_data.append({
                    'name': value_key,
                    'value': form_data[value_key]
                })
            new_object = CmdbObject(
                public_id=int(obm.get_highest_id(CmdbObject.COLLECTION) + 1),
                type_id=type_id,
                creation_time=datetime.datetime.utcnow(),
                author_id=MANAGER_HOLDER.get_user_manager().get_user(current_user['public_id']).get_public_id(),
                last_edit_time=None,
                active=True,
                status=None,
                fields=insert_data
            )
            new_log = CmdbLog(
                author_id=MANAGER_HOLDER.get_user_manager().get_user(current_user['public_id']).get_public_id(),
                action='create',
                message=log_message or 'New object of type {} created'.format(object_type.get_label()),
                date=datetime.datetime.utcnow()
            )
            new_object.add_log(new_log)
            insert_ack = obm.insert_object(new_object)
            LOGGER.debug(insert_ack)
            if insert_ack:
                inserted_object = obm.get_object(insert_ack)
        except (CMDBError, Exception) as e:
            LOGGER.warning(e)
            raise ObjectInsertError(e)
    except (CMDBError, ObjectInsertError) as e:
        LOGGER.warning(e)
        error = e
        return render_template('objects/add_post.html', error=error)
    return render_template('objects/add_post.html', inserted_object=inserted_object, object_type=object_type,
                           form_data=form_data, error=error)


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

    render = CmdbParser(view_type, view_object)
    references = obm.get_object_references(public_id)
    LOGGER.debug("TSET")
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
@login_required
def edit_page_get(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = obm.get_object(public_id=public_id)
    view_type = obm.get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = CmdbParser(view_type, view_object, mode=CmdbParser.EDIT_MODE)

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
        return render_template('objects/edit_post.html', old_object=old_object, new_object=new_object, error=error)
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
    return render_template('objects/edit_post.html', old_object=old_object, new_object=new_object, error=error)


@object_pages.route('<int:public_id>/delete/', methods=['GET'])
@register_breadcrumb(object_pages, '.delete', 'Delete')
def delete_page(public_id):
    error = None
    try:
        delete_object = obm.get_object(public_id)
    except CMDBError:
        abort(404)
    delete_token = MANAGER_HOLDER.get_security_manager().generate_delete_token(delete_object)
    return render_template('objects/delete.html', delete_object=delete_object, delete_token=delete_token, error=error)


@object_pages.route('<int:public_id>/delete/', methods=['POST'])
def delete_page_confirm(public_id):
    error = None
    try:
        delete_object = obm.get_object(public_id)
        delete_token_request = request.form.to_dict()['delete_token']
        delete_token = MANAGER_HOLDER.get_security_manager().decrypt_token(delete_token_request)
        if not delete_token:
            abort(500)
        obm.delete_object(public_id)
    except CMDBError:
        abort(404)
    return render_template('objects/delete_post.html', delete_object=delete_object, delete_token=delete_token,
                           error=error)
