"""
Framework pages
"""
from cmdb.utils import get_logger
from cmdb.utils.error import CMDBError
from cmdb.interface.cmdb_holder import CmdbManagerHolder
from flask import Blueprint, render_template, jsonify, current_app
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from flask import request, abort


LOGGER = get_logger()

framework_pages = Blueprint('framework_pages', __name__, template_folder='templates', url_prefix='/framework')
default_breadcrumb_root(framework_pages, '.framework_pages')

with current_app.app_context():
    MANAGER_HOLDER = CmdbManagerHolder()
    MANAGER_HOLDER = current_app.manager_holder


@framework_pages.route('/')
@register_breadcrumb(framework_pages, '.', 'Framework')
def overview_page():
    return render_template('framework/index.html')


@framework_pages.route('/categories/')
@register_breadcrumb(framework_pages, '.categories', 'Categories')
def categories_page():
    category_tree = MANAGER_HOLDER.get_object_manager().get_category_tree()
    all_categories = MANAGER_HOLDER.get_object_manager().get_all_categories()
    return render_template('framework/categories.html', category_tree=category_tree, all_categories=all_categories)
