from cmdb.interface.web_app import MANAGER_HOLDER


def inject_object_manager():
    def object_manager():
        return MANAGER_HOLDER.get_object_manager()
    return dict(object_manager=object_manager())


def inject_current_url():
    def current_url():
        from flask import request
        return request.base_url
    return dict(current_url=current_url)