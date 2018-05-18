from functools import wraps
from flask import request, abort


def json_required(f):
    @wraps(f)
    def _json_required(*args, **kwargs):
        if not request or not request.json:
            abort(400)
        return f(*args, **kwargs)
    return _json_required
