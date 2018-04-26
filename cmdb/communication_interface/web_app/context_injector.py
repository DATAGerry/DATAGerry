def inject_frontend_info():
    def frontend(key):
        from cmdb.application_utils import SYSTEM_SETTINGS_READER
        return SYSTEM_SETTINGS_READER.get_value(key, 'frontend')
    return dict(frontend=frontend)

