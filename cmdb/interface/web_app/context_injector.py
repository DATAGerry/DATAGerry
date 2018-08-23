from flask import current_app


def inject_object_manager():
    def object_manager():
        return current_app.obm
    return dict(object_manager=object_manager())


def inject_current_url():
    def current_url():
        from flask import request
        return request.base_url
    return dict(current_url=current_url)