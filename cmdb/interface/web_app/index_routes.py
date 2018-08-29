"""
Index Page
"""
from cmdb.utils.interface_wraps import login_required
from flask import Blueprint
from flask import render_template
# from flask import current_app

index_pages = Blueprint('index_pages', __name__, template_folder='templates')


@index_pages.route('/')
@index_pages.route('/dashboard')
@login_required
def index_page():
    return render_template('index.html')
