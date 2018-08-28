from flask import Blueprint
from flask import render_template
from flask import request

auth_pages = Blueprint('auth_pages', __name__, template_folder='templates')


@auth_pages.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_pages.route('/login', methods=['POST'])
def login_page_post():
    return request.form['password'], request.form['password']


@auth_pages.route('/logout')
def logout_page():
    return render_template('logout.html')


@auth_pages.route('/register')
def register_page():
    return render_template('register.html')