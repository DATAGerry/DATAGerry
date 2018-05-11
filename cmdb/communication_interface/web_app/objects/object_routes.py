from flask import Blueprint, render_template, abort, request, redirect, url_for
from cmdb.object_framework import OBJECT_MANAGER, CmdbObject
from cmdb.data_storage.database_manager import NoDocumentFound

object_pages = Blueprint('object_pages', __name__, template_folder='objects/templates', url_prefix="/object")


@object_pages.route("/<int:public_id>")
def view_single_object(public_id):
    try:
        single_object = OBJECT_MANAGER.get_object(public_id)
        single_object.update_view_counter()
    except NoDocumentFound:
        abort(404)
    OBJECT_MANAGER.update_object(single_object.to_database())
    concurrent_type = OBJECT_MANAGER.get_type(single_object.get_type_id())
    links_list = single_object.get_links()
    return render_template('view_object.html', object=single_object, type=concurrent_type, linked_objects=links_list)


@object_pages.route("/add/<int:type_id>", methods=['GET'])
def view_add_form(type_id):
    type_object = OBJECT_MANAGER.get_type(type_id)
    return render_template('add_object.html', type=type_object)

@object_pages.route("/add/<int:type_id>", methods=['POST'])
def add_object(type_id):
    import datetime
    data = request.form
    con_type = OBJECT_MANAGER.get_type(type_id)
    new_fields = []
    dict_buffer = request.form.to_dict(flat=False)
    for k in dict_buffer:
        new_fields.append({
            'name': k,
            'value': dict_buffer[k][0]
        })
    try:
        new_object = CmdbObject(type_id=type_id, status=con_type.status, version='1.0.0',
                                creation_time=datetime.datetime.now(), creator_id=1, last_editor_id=1, last_edit_time=datetime.datetime.now(),
                            active=True, views=0, fields=new_fields, logs=None, public_id=OBJECT_MANAGER.get_highest_id(CmdbObject.COLLECTION)+1, links=[])
    except Exception as e:
        print(e.message)
    OBJECT_MANAGER.insert_object(new_object.to_database())
    return redirect(url_for('type_pages.view_type_list', public_id=type_id))
