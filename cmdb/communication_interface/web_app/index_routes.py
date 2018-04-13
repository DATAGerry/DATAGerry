"""
Flask routes for all index based pages
"""
from flask import Blueprint
from flask import render_template

INDEX_PAGES = Blueprint('index_pages', __name__, template_folder='templates')


@INDEX_PAGES.route('/')
def index_page():
    """
    loads index page
    :return: html instance of index html
    """
    return render_template('index.html')
