"""
Search Pages
"""
import logging
from cmdb.interface.web_app import app
from cmdb.object_framework.cmdb_render import CmdbRender
from cmdb.utils.interface_wraps import login_required, right_required
from flask import Blueprint, render_template, request, make_response
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from bson import Regex

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)

search_pages = Blueprint('search_pages', __name__, template_folder='templates', url_prefix='/search')
default_breadcrumb_root(search_pages, '.search_pages')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@search_pages.route('/', methods=['GET'])
@register_breadcrumb(search_pages, '.', 'Search')
@login_required
@right_required('base.framework.object.view')
def default_search_page_get():
    type_list = MANAGER_HOLDER.get_object_manager().get_all_types()
    user_list = MANAGER_HOLDER.get_user_manager().get_all_users()
    return render_template('search/index.html', type_list=type_list, user_list=user_list)


@search_pages.route('/', methods=['POST'])
@login_required
@right_required('base.framework.object.view')
def default_search_page_post():
    """TODO: exclude wont work right now"""
    search_text_input = request.form.get('search_text_input', '')
    search_text_input_exclude = request.form.get('search_text_input_exclude', '')
    text_search = bool(search_text_input)
    type_id = request.form.get('search_type_id', None)
    author_id = request.form.get('search_author_id', None)
    query = {
        'fields.value': Regex(search_text_input, 'i')
    }

    if search_text_input_exclude != '':
        query.update({
            "$nor": [
                {'fields.value': Regex(search_text_input_exclude, 'i')}
            ]
        })
    if type_id:
        query.update({
            'type_id': int(type_id)
        })
    if author_id:
        query.update({
            'author_id': int(author_id)
        })
    LOGGER.debug("QUERY {}".format(query))
    object_manager = MANAGER_HOLDER.get_object_manager()
    search_results = object_manager.search_objects(query)
    result_renders = list()
    result_type_buffer = dict()
    for result in search_results:
        try:
            type_id = result.get_type_id()
            if type_id in result_type_buffer:
                type_instance = result_type_buffer.get(type_id)
            else:
                type_instance = object_manager.get_type(type_id)
                result_type_buffer.update({type_id: type_instance})
            render_instance = CmdbRender(type_instance=type_instance, object_instance=result)
            if search_text_input:
                render_instance.set_matched_fieldset(search_results[result])
            result_renders.append(render_instance)
        except CMDBError:
            continue
    return render_template('search/include_results.html', results=result_renders, text_search=text_search,
                           results_counter=len(search_results))
