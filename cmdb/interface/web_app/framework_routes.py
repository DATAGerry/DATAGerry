"""
Framework pages
"""
import logging
from flask import Blueprint, render_template
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import app

LOGGER = logging.getLogger(__name__)

framework_pages = Blueprint('framework_pages', __name__, template_folder='templates', url_prefix='/framework')
default_breadcrumb_root(framework_pages, '.framework_pages')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


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
