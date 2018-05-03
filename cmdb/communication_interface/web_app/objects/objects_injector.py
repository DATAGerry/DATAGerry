from flask import Markup


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


def inject_link_table():
    def generate_link_table(link_ids: list):
        from cmdb.object_framework import OBJECT_MANAGER
        output = Markup('<table class="table table-striped">')
        output += Markup('<thead><tr><th>ID</th><th>Type</th><th>Author</th><th>Date</th></tr></thead>')
        output += Markup('<tbody>')
        for link in link_ids:
            output += Markup('<tr>')
            buffer_object = OBJECT_MANAGER.get_object(link['public_id'])
            buffer_type = OBJECT_MANAGER.get_type(buffer_object.get_type_id())
            output += Markup('<td><a href="/object/{0}">{1}</a></td>').format(buffer_object.get_public_id(), buffer_object.get_public_id())
            output += Markup('<td>{}</td>').format(buffer_type.get_title())
            output += Markup('<td>{}</td>').format(link['adding_id'])
            output += Markup('<td>{}</td>').format(link['adding_time'])
            output += Markup('</tr>')
        output += Markup('</tbody>')
        output += Markup('</table>')
        return output
    return dict(generate_link_table=generate_link_table)
