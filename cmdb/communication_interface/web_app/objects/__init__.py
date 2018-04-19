from flask import Blueprint

OBJECT_PAGES = Blueprint('object_pages', __name__, template_folder='templates', url_prefix='/object/')
TYPE_PAGES = Blueprint('type_pages', __name__, template_folder='templates', url_prefix='/type/')