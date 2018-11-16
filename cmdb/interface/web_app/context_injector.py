from cmdb.interface.web_app import MANAGER_HOLDER
from cmdb.utils.error import CMDBError
from cmdb.utils.logger import get_logger

LOGGER = get_logger()


def inject_current_user():
    def current_user():
        # TODO: extract current user
        from flask import request
        from jwcrypto import jwt
        return 1

    return dict(current_user_id=current_user())


def inject_object_manager():
    def object_manager():
        return MANAGER_HOLDER.get_object_manager()

    return dict(object_manager=object_manager)


def inject_sidebar():
    def sidebar():
        try:
            categories = MANAGER_HOLDER.get_object_manager().get_all_categories()
        except CMDBError:
            return []
        return categories

    return dict(sidebar=sidebar)


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
