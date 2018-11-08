from flask import Blueprint, request, render_template, make_response, url_for, redirect
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
    from cmdb.user_management.user import NoValidAuthenticationProviderError
    from cmdb.user_management.user_authentication import WrongUserPasswordError
    user_name = str(request.form['user_name']).lower()
    password = request.form['password']

    correct = False
    try:
        login_user = MANAGER_HOLDER.get_user_manager().get_user_by_name(user_name)
        auth_method = login_user.get_authenticator()
        correct = auth_method.authenticate(
            user=login_user,
            password=password
        )
    except NoUserFoundExceptions as e:
        CMDB_LOGGER.info("Wrong login try - user {} not found".format(password))
        return render_template('login.html', error=e.message)
    except WrongUserPasswordError as e:
        CMDB_LOGGER.info("Wrong password login try for user {}".format(password))
        return render_template('login.html', error=e.message)
    except NoValidAuthenticationProviderError as e:
        CMDB_LOGGER.info("{}".format(e))
        return render_template('login.html', error=e)

    if correct is True:
        resp = make_response(redirect(url_for('index_pages.index_page')))
        import time
        timeout = MANAGER_HOLDER.get_system_settings_reader().get_value('token_timeout', 'security')
        expire_date = time.time() + (timeout * 60)
        resp.set_cookie('access-token',
                        MANAGER_HOLDER.get_security_manager().encrypt_token(login_user, timeout=timeout*60),
                        expires=expire_date)
        return resp
    return render_template('login.html')


@auth_pages.route('/logout')
def logout_page():
    resp = make_response(redirect(url_for('auth_pages.login_page')))
    resp.set_cookie('access-token', '', expires=0)
    return resp


@auth_pages.route('/register')
def register_page():
    return render_template('register.html')


@auth_pages.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot-password.html')
