import datetime
from types import FunctionType


def label_active(s):
    from flask import Markup
    if bool(s):
        return Markup('<span class="badge badge-primary">Active</span>')
    else:
        return Markup('<span class="badge badge-secondary">Inactive</span>')


def display_icon(icon):
    if icon is not None:
        return icon
    else:
        return 'line-icon-folder'


def encode_date(date):
    try:
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return date


def eval_input(caller):
    call = eval(caller)
    if call is FunctionType:
        return call()
    else:
        return call


def cmdb_exception_handler(handling: FunctionType):
    from cmdb.utils.error import CMDBError
    try:
        return handling()
    except (CMDBError, Exception):
        return None
