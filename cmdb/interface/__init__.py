from cmdb.interface.gunicorn import HTTPServer, DispatcherMiddleware
from cmdb.interface.rest_api import create_rest_api
from cmdb.interface.web_app import create_web_app


main_application = DispatcherMiddleware(
    app=create_web_app(),
    mounts={'/rest': create_rest_api()}
)

