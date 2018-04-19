"""
Flask routes for all static sites like login
"""
from flask import Blueprint
from flask import render_template

STATIC_PAGES = Blueprint('static_pages', __name__, template_folder='templates')


@STATIC_PAGES.route('/licence')
def licence_page():
    return render_template('licence.html')


@STATIC_PAGES.route('/contact')
def contact_page():
    return render_template('contact.html')


@STATIC_PAGES.route('/faq')
def faq_page():
    return render_template('faq.html')


@STATIC_PAGES.route('/login')
def login_page():
    """
    user login page
    :return: login site
    """
    return render_template('login.html')


@STATIC_PAGES.route('/logout')
def logout_page():
    """
    logout page
    :return: logout site
    """
    return render_template('logout.html')


@STATIC_PAGES.route('/register')
def register_page():
    """
    register page
    :return: register site
    """
    return render_template('register.html')
