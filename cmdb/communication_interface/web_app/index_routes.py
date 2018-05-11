"""
Index Page
"""
from flask import Blueprint
from flask import render_template
from cmdb.object_framework import OBJECT_MANAGER

index_pages = Blueprint('index_pages', __name__, template_folder='templates')


@index_pages.route('/')
@index_pages.route('/dashboard')
def index_page():
    objects = OBJECT_MANAGER.get_objects_by(sort='creation_time')

    return render_template('index.html', objects=objects[:10])
