from functools import wraps
from flask import request, abort
from cmdb.utils.logger import get_logger
LOGGER = get_logger()


def json_required(f):
    @wraps(f)
    def _json_required(*args, **kwargs):
        LOGGER.warn(request)
        from pprint import pprint
        pprint(request.__dict__)
        if not request or not request.json:
            abort(400)
        return f(*args, **kwargs)
    return _json_required
