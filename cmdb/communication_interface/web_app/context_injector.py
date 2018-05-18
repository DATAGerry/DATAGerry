from flask import current_app


def inject_object_manager():
    def object_manager():
        return current_app.obm
    return dict(object_manager=object_manager())


def inject_frontend_info():
    def frontend(key):
        return ""
    return dict(frontend=frontend)


def inject_current_url():
    def current_url():
        from flask import request
        return request.base_url
    return dict(current_url=current_url)


def inject_sidebar():
    def sidebar_categories():
        cats = current_app.obm.get_all_categories()
        return cats
    return dict(sidebar_categories=sidebar_categories)
