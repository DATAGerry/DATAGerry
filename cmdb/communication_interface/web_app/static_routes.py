"""
Flask routes for all static sites like login
"""
from flask import Blueprint
from flask import render_template

static_pages = Blueprint('static_pages', __name__, template_folder='templates')


@static_pages.route('/licence')
def licence_page():
    return render_template('licence.html')


@static_pages.route('/contact')
def contact_page():
    return render_template('contact.html')


@static_pages.route('/faq')
def faq_page():
    return render_template('faq.html')


@static_pages.route('/login')
def login_page():
    """
    user login page
    :return: login site
    """
    return render_template('login.html')


@static_pages.route('/logout')
def logout_page():
    """
    logout page
    :return: logout site
    """
    return render_template('logout.html')


@static_pages.route('/register')
def register_page():
    """
    register page
    :return: register site
    """
    return render_template('register.html')
