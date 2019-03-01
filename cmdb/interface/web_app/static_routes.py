from flask import Blueprint
from flask import render_template

static_pages = Blueprint('static_pages', __name__, template_folder='templates')


@static_pages.route('/licence/')
def licence_page():
    return render_template('static/licence.html')


@static_pages.route('/contact/')
def contact_page():
    return render_template('contact.html')


@static_pages.route('/faq/')
def faq_page():
    return render_template('faq.html')
