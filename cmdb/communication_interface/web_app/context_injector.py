def inject_object_manager():
    def object_manager():
        from cmdb.object_framework import OBJECT_MANAGER
        return OBJECT_MANAGER
    return dict(object_manager=object_manager())


def inject_frontend_info():
    def frontend(key):
        from cmdb.application_utils import SYSTEM_SETTINGS_READER
        return SYSTEM_SETTINGS_READER.get_value(key, 'frontend')
    return dict(frontend=frontend)


def inject_current_url():
    def current_url():
        from flask import request
        return request.base_url
    return dict(current_url=current_url)


def inject_sidebar():
    def sidebar_categories():
        from cmdb.object_framework import OBJECT_MANAGER
        cats = OBJECT_MANAGER.get_all_categories()
        return cats
    return dict(sidebar_categories=sidebar_categories)
