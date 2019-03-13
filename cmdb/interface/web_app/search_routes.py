"""
Search Pages
"""
import logging
from cmdb.interface.web_app import app
from cmdb.utils.interface_wraps import login_required, right_required
from flask import Blueprint, render_template
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root

LOGGER = logging.getLogger(__name__)


search_pages = Blueprint('search_pages', __name__, template_folder='templates', url_prefix='/search')
default_breadcrumb_root(search_pages, '.search_pages')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@search_pages.route('/')
@register_breadcrumb(search_pages, '.', 'Search')
@login_required
@right_required('base.framework.object.view')
def default_search_page():
    return render_template('search/index.html')
