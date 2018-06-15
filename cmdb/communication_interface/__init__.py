"""
Init module for http server + apps
"""
from cmdb.communication_interface.gunicorn import HTTPServer, DispatcherMiddleware
from cmdb.communication_interface.web_app import create_web_app
from cmdb.communication_interface.rest_api import create_rest_api

application = DispatcherMiddleware(
    app=create_web_app(),
    mounts={'/rest': create_rest_api()}
)


