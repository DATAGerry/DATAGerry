def label_active(s):
    from flask import Markup
    if bool(s):
        return Markup('<span class="badge badge-primary">Active</span>')
    else:
        return Markup('<span class="badge badge-secondary">Inactive</span>')
