from cmdb.utils.interface_wraps import login_required
from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.object_framework.cmdb_object_field_type import FieldNotFoundError
from cmdb.object_framework.cmdb_object_manager import ObjectInsertError, ObjectUpdateError
from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_log import CmdbLog
from cmdb.object_framework.cmdb_render import CmdbRender
from flask import Blueprint, render_template, request, abort
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import app
from cmdb.interface.interface_parser import InterfaceParser

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

import datetime
import json
import logging

LOGGER = logging.getLogger(__name__)

object_pages = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object')
default_breadcrumb_root(object_pages, '.object_pages')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@object_pages.route('/')
@object_pages.route('/list/')
@register_breadcrumb(object_pages, '.', 'Objects')
@login_required
def list_page():
    uum = MANAGER_HOLDER.get_user_manager()
    all_objects = MANAGER_HOLDER.get_object_manager().get_all_objects()

    return render_template('objects/list.html', user_manager=uum,
                           all_objects=all_objects)


@object_pages.route('/newest/')
@register_breadcrumb(object_pages, '.newest', 'Newest')
def newest_objects_page():
    only_active = MANAGER_HOLDER.only_active()
    try:
        object_limit = int(request.args.get('limit') or 25)
    except ValueError:
        object_limit = 25
    newest_objects = []
    try:
        type_buffer_list = {}
        if only_active:
            newest_objects_list = MANAGER_HOLDER.get_object_manager().get_objects_by(sort='creation_time',
                                                                                     limit=object_limit,
                                                                                     active={"$eq": True})
        else:
            newest_objects_list = MANAGER_HOLDER.get_object_manager().get_objects_by(sort='creation_time',
                                                                                     limit=object_limit)
        for passed_object in newest_objects_list:
            current_type = None
            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = MANAGER_HOLDER.get_object_manager().get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError as e:
                    LOGGER.warning("Newest object type - error: {}".format(e.message))
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            newest_objects.append(tmp_render)
        LOGGER.debug(newest_objects)
    except CMDBError:
        newest_objects = None
    return render_template('objects/newest.html', newest_objects=newest_objects, limit=object_limit)


@object_pages.route('/latest/')
@register_breadcrumb(object_pages, '.latest', 'Latest')
def latest_objects_page():
    try:
        object_limit = int(request.args.get('limit') or 25)
    except ValueError:
        object_limit = 25
    latest_objects = []
    try:
        type_buffer_list = {}
        latest_objects_list = MANAGER_HOLDER.get_object_manager().get_objects_by(sort='last_edit_time',
                                                                                 limit=object_limit,
                                                                                 last_edit_time={
                                                                                     "$ne": None,
                                                                                     "$type": "date"
                                                                                 },
                                                                                 active={"$eq": True})
        for passed_object in latest_objects_list:
            current_type = None
            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = MANAGER_HOLDER.get_object_manager().get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError as e:
                    LOGGER.warning("Latest object type - error: {}".format(e.message))
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            latest_objects.append(tmp_render)
        LOGGER.debug(latest_objects)
    except CMDBError:
        latest_objects = None
    return render_template('objects/latest.html', latest_objects=latest_objects, limit=object_limit)


@object_pages.route('/most-viewed/')
@register_breadcrumb(object_pages, '.most', 'Most viewed')
def most_viewed_objects_page():
    try:
        object_limit = int(request.args.get('limit') or 25)
    except ValueError:
        object_limit = 25
    viewed_objects = []
    try:
        type_buffer_list = {}
        viewed_objects_list = MANAGER_HOLDER.get_object_manager().get_objects_by(sort='views',
                                                                                 limit=object_limit,
                                                                                 active={"$eq": True})
        for passed_object in viewed_objects_list:
            current_type = None
            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = MANAGER_HOLDER.get_object_manager().get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError as e:
                    LOGGER.warning("Viewed object type - error: {}".format(e.message))
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            viewed_objects.append(tmp_render)
        LOGGER.debug(viewed_objects)
    except CMDBError:
        viewed_objects = None
    return render_template('objects/most_viewed.html', most_viewed_objects=viewed_objects, limit=object_limit)


@object_pages.route('/user/<int:user_id>/')
@register_breadcrumb(object_pages, '.user_created', 'Your objects')
@login_required
def show_user_owned_objects(user_id):
    obm = MANAGER_HOLDER.get_object_manager()
    user_objects_list = list()
    user_objects = list()
    try:
        current_user = MANAGER_HOLDER.get_user_manager().get_user(public_id=user_id)
        user_objects = MANAGER_HOLDER.get_object_manager().get_objects_by(author_id=current_user.get_public_id())
    except CMDBError:
        abort(500)
    for user_object in user_objects:
        try:
            user_objects_list.append(CmdbRender(obm.get_type(user_object.get_type_id()), user_object))
        except CMDBError:
            continue
    return render_template('objects/user_owned.html', user_objects=user_objects_list)


@object_pages.route('/type/<int:type_id>/add', methods=['GET'])
@object_pages.route('/type/<int:type_id>/add/', methods=['GET'])
@register_breadcrumb(object_pages, '.add', 'Add')
@login_required
def add_new_page(type_id):
    try:
        object_type = MANAGER_HOLDER.get_object_manager().get_type(type_id)
    except (CMDBError, Exception) as e:
        LOGGER.critical(e)
        abort(500, e.message)
    try:
        status_list = MANAGER_HOLDER.get_object_manager().get_status_by_type(type_id)
    except (CMDBError, Exception):
        status_list = []

    render = InterfaceParser(type_instance=object_type, mode=InterfaceParser.ADD_MODE)
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
            object_type = MANAGER_HOLDER.get_object_manager().get_type(type_id)
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
                public_id=int(MANAGER_HOLDER.get_object_manager().get_highest_id(CmdbObject.COLLECTION) + 1),
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
            insert_ack = MANAGER_HOLDER.get_object_manager().insert_object(new_object)
            LOGGER.debug(insert_ack)
            if insert_ack:
                inserted_object = MANAGER_HOLDER.get_object_manager().get_object(insert_ack)
        except (CMDBError, Exception) as e:
            LOGGER.warning(e)
            raise ObjectInsertError(e)
    except (CMDBError, ObjectInsertError) as e:
        LOGGER.warning(e)
        error = e
        return render_template('objects/add_post.html', error=error)
    return render_template('objects/add_post.html', inserted_object=inserted_object, object_type=object_type,
                           form_data=form_data, error=error)


@object_pages.route('/<int:public_id>')
@object_pages.route('/<int:public_id>/')
@register_breadcrumb(object_pages, '.view', 'View')
@login_required
def view_page(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    try:
        view_object = MANAGER_HOLDER.get_object_manager().get_object(public_id=public_id)
        view_object.update_view_counter()
        MANAGER_HOLDER.get_object_manager().update_object(view_object)
        view_type = MANAGER_HOLDER.get_object_manager().get_type(public_id=view_object.get_type_id())
        render = CmdbRender(view_type, view_object)
    except CMDBError:
        abort(500)

    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    parser = InterfaceParser(view_type, view_object)
    references_objects = MANAGER_HOLDER.get_object_manager().get_object_references(public_id)
    reference_list = list()

    for reference in references_objects:
        reference_list.append(
            CmdbRender(MANAGER_HOLDER.get_object_manager().get_type(public_id=reference.get_type_id()), reference))
    return render_template('objects/view.html',
                           object_base=object_base,
                           author_name=author_name,
                           view_object=view_object,
                           view_type=view_type,
                           references=reference_list,
                           parser=parser,
                           render=render
                           )


@object_pages.route('<int:public_id>/edit/', methods=['GET'])
@register_breadcrumb(object_pages, '.edit', 'Edit')
@login_required
def edit_page_get(public_id):
    usm = MANAGER_HOLDER.get_user_manager()
    ssm = MANAGER_HOLDER.get_security_manager()
    view_object = MANAGER_HOLDER.get_object_manager().get_object(public_id=public_id)
    view_type = MANAGER_HOLDER.get_object_manager().get_type(public_id=view_object.get_type_id())
    author_name = usm.get_user(view_object.author_id).get_name()
    object_base = ssm.encode_object_base_64(view_object.get_all_fields())

    render = InterfaceParser(view_type, view_object, mode=InterfaceParser.EDIT_MODE)

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
    old_object = MANAGER_HOLDER.get_object_manager().get_object(public_id=public_id)
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
        log_state = MANAGER_HOLDER.get_object_manager().generate_log_state(old_field_values)
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
    if error is None:
        try:
            MANAGER_HOLDER.get_object_manager().update_object(new_object)
        except (CMDBError, Exception) as e:
            error = ObjectUpdateError("Update error while inserting into database: {}".format(e))
    return render_template('objects/edit_post.html', old_object=old_object, new_object=new_object, error=error)


@object_pages.route('<int:public_id>/delete/', methods=['GET'])
@register_breadcrumb(object_pages, '.delete', 'Delete')
def delete_page(public_id):
    error = None
    try:
        delete_object = MANAGER_HOLDER.get_object_manager().get_object(public_id)
    except CMDBError:
        abort(404)
    delete_token = MANAGER_HOLDER.get_security_manager().generate_delete_token(delete_object)
    return render_template('objects/delete.html', delete_object=delete_object, delete_token=delete_token, error=error)


@object_pages.route('<int:public_id>/delete/', methods=['POST'])
def delete_page_confirm(public_id):
    error = None
    try:
        delete_object = MANAGER_HOLDER.get_object_manager().get_object(public_id)
        delete_token_request = request.form.to_dict()['delete_token']
        delete_token = MANAGER_HOLDER.get_security_manager().decrypt_token(delete_token_request)
        if not delete_token:
            abort(500)
        MANAGER_HOLDER.get_object_manager().delete_object(public_id)
    except CMDBError:
        abort(404)
    return render_template('objects/delete_post.html', delete_object=delete_object, delete_token=delete_token,
                           error=error)
