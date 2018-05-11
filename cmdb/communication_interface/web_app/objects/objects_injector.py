def inject_calc_url():
    def calc_url(url, url_object):
        import re
        new_url = str(url)
        links = re.findall('\%(.*?)\%', url)
        for field in links:
            field_val = url_object.get_value(field)
            new_url = new_url.replace('%'+field+'%', field_val)
        return new_url
    return dict(calc_url=calc_url)


def inject_input_generator():
    def parse_input(**field):
        from flask import Markup
        from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
        field.update({'public_id': 1})
        current_field = CmdbFieldType(**field)
        return Markup(current_field.get_html_output())
    return dict(parse_input=parse_input)