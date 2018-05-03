from flask import Blueprint, render_template, abort
from cmdb.data_storage.database_manager import NoDocumentFound
object_pages = Blueprint('object_pages', __name__, template_folder='objects/templates', url_prefix="/object")


@object_pages.route("/<int:public_id>")
def view_single_object(public_id):
    from cmdb.object_framework import OBJECT_MANAGER
    try:
        single_object = OBJECT_MANAGER.get_object(public_id)
        single_object.update_view_counter()
    except NoDocumentFound:
        abort(404)
    OBJECT_MANAGER.update_object(single_object.to_database())
    concurrent_type = OBJECT_MANAGER.get_type(single_object.get_type_id())
    links_list = single_object.get_links()
    return render_template('view_object.html', object=single_object, type=concurrent_type, linked_objects=links_list)
