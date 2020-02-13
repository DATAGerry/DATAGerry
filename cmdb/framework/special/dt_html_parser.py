# -*- coding: utf-8 -*-
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from flask import abort


class DtHtmlParser:

    def __init__(self, object_manager: CmdbObjectManager, current_field=None):
        self.object_manager: CmdbObjectManager = object_manager
        self.current_field = current_field

    def field_to_html(self, field_type):
        """Dispatch method"""
        method_name = str(field_type)
        # Get the method from 'self'. Default to a lambda.
        default = '<span>%s<span>' % '' if not self.current_field['value'] else self.current_field['value']
        method = getattr(self, method_name, lambda: default)
        # Call the method as we return it
        return method()

    def password(self):
        return '<i class="far fa-eye-slash text-center w-100"></i>'

    def checkbox(self):
        if self.current_field['value']:
            return '<i class="far fa-check-square text-center w-100"></i>'
        else:
            return '<i class="far fa-square text-center w-100"></i>'

    def date(self):
        from datetime import datetime
        datetime_str = '' if not self.current_field['value'] else self.current_field['value']
        if isinstance(datetime_str, datetime):
            datetime_str = datetime_str.strftime('%d/%m/%Y')
        else:
            datetime_str = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
        return '<span>%s<span>' % datetime_str

    def ref(self):
        html_content = 'No reference set'
        if self.current_field['value']:
            try:
                ref_object = self.object_manager.get_object(self.current_field['value'])
            except ObjectManagerGetError as err:
                return abort(404)

            try:
                ref_type = self.object_manager.get_type(ref_object.get_type_id())
                html_content = '<i class="%s"></i> %s #%s' % (ref_type.get_icon(), ref_type.label, ref_object.public_id)
                html_content += ' - '

                summaries = ref_type.get_summary().fields
                for field in summaries:
                    html_content += str([x for x in ref_object.fields if x['name'] == field['name']][0]['value'])
                    if field != summaries[-1]:
                        html_content += ' | '
            except ObjectManagerGetError as err:
                return abort(404)

        return '<span>%s</span>' % html_content
