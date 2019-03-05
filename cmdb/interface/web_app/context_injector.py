import logging
import json
from cmdb.interface.web_app import app
from cmdb.utils.error import CMDBError
from cmdb.user_management.user import User
from types import FunctionType

LOGGER = logging.getLogger(__name__)

with app.app_context():
    MANAGER_HOLDER = app.manager_holder


def inject_modus():
    def modus():
        from cmdb import __MODE__
        return __MODE__

    return dict(mode=modus())


def inject_exception_handler():
    def exception_handler(func: FunctionType, *args):
        try:
            return func(*args)
        except CMDBError:
            return None
    return dict(exception_handler=exception_handler)


def inject_all_types():
    def all_types():
        all_types_in_db = MANAGER_HOLDER.get_object_manager().get_all_types()
        type_list = []
        for type_in_db in all_types_in_db:
            type_list.append({
                'public_id': type_in_db.get_public_id(),
                'label': type_in_db.get_label()
            })
        return type_list

    return dict(all_types=all_types())


def inject_user_names():
    def all_users():

        all_users_in_db = MANAGER_HOLDER.get_user_manager().get_all_users()
        user_list = []
        for user_name in all_users_in_db:
            try:
                user_list.append({
                    'public_id': user_name.get_public_id(),
                    'name': user_name.get_name()
                })
            except CMDBError:
                LOGGER.warning("User {} not initable".format(user_name))
                continue
        return user_list

    return dict(all_users=all_users())


def inject_current_user():
    def current_user():
        curr_user = None
        try:
            from flask import request
            security_manager_instance = MANAGER_HOLDER.get_security_manager()
            user_string = json.loads(
                security_manager_instance.decrypt_token(request.cookies.get('access-token')).decode())
            curr_user = User(**user_string)
        except (CMDBError, Exception):
            return None
        return curr_user

    return dict(current_user=current_user())


def inject_object_manager():
    def object_manager():
        return MANAGER_HOLDER.get_object_manager()

    return dict(object_manager=object_manager())


def inject_user_manager():
    def user_manager():
        return MANAGER_HOLDER.get_user_manager()

    return dict(user_manager=user_manager())


def inject_sidebar_hidden():
    def sidebar_hidden():
        import flask
        if 'sidebar_hidden' in flask.request.cookies:
            return True
        return False

    return dict(sidebar_hidden=sidebar_hidden())


def inject_current_url():
    def current_url():
        from flask import request
        return request.base_url

    return dict(current_url=current_url)
