def label_active(s):
    from flask import Markup
    if bool(s):
        return Markup('<span class="badge badge-success">A</span>')
    else:
        return Markup('<span class="badge badge-danger">D</span>')


def default_cat_icon(s):
    if s:
        return s
    else:
        return str("far fa-folder")