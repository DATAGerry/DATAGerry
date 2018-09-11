from cmdb.utils.interface_wraps import right_required
from cmdb.utils import get_logger
from flask import Blueprint, render_template
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb
from cmdb.interface.web_app import MANAGER_HOLDER
from flask import request, abort

LOGGER = get_logger()

object_pages = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object')
default_breadcrumb_root(object_pages, '.object_pages')


@right_required
@object_pages.route('/<int:public_id>')
@register_breadcrumb(object_pages, '.', 'Objects')
def view_page(public_id):
    return render_template('objects/view.html')

