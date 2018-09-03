from flask import Blueprint
from flask import render_template
from flask import request
from cmdb.utils import get_logger
from cmdb.interface.web_app import MANAGER_HOLDER
CMDB_LOGGER = get_logger()

auth_pages = Blueprint('auth_pages', __name__, template_folder='templates')


@auth_pages.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_pages.route('/login', methods=['POST'])
def login_page_post():
    from cmdb.user_management.user_manager import NoUserFoundExceptions
    user_name = request.form['user_name']
    password = request.form['password']

    try:
        login_user = MANAGER_HOLDER.get_user_manager().get_user_by_name(user_name)
    except NoUserFoundExceptions:
        CMDB_LOGGER.info("Wrong login try - user {} not found".format(password))
        return render_template('login.html')
    print(login_user)
    return render_template('login.html')


@auth_pages.route('/logout')
def logout_page():
    return render_template('logout.html')


@auth_pages.route('/register')
def register_page():
    return render_template('register.html')


@auth_pages.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot-password.html')
