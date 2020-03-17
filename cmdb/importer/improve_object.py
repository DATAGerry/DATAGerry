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

import logging

LOGGER = logging.getLogger(__name__)


class ImproveObject:
    def __init__(self, entry: dict, field_entries, possible_fields):
        """
        Basic improve super class for object imports
        Args:
            entry: Numbered values of the fields
            field_entries: Field attributes
            possible_fields: Field types
        """
        self.entry = entry
        self.field_entries = field_entries
        self.possible_fields = possible_fields
        self.value = None
        super(ImproveObject, self)

    def improve_entry(self) -> dict:
        for entry_field in self.field_entries:
            for item in self.possible_fields:
                self.value = self.entry.get(entry_field.get_value())
                if item['type'] == 'date' and item["name"] == entry_field.get_name():
                    self.entry.update({entry_field.get_value(): self.improve_date()})
                if item['type'] == 'ref' and item["name"] == entry_field.get_name():
                    self.improve_ref()
        return self.entry

    def improve_date(self):
        import datetime

        try:
            if isinstance(self.value, dict) and self.value.get('$date'):
                return datetime.datetime.fromtimestamp(self.value["$date"]/1000)
        except Exception:
            pass

        if isinstance(self.value, str):
            dt_format = ('%Y/%m/%d', '%Y-%m-%d', '%Y.%m.%d', '%Y,%m,%d',
                         '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d,%m,%Y',
                         '%d.%m.%y %H:%M', '%d.%m.%y %H:%M:%S', '%y.%m.%d %H:%M', '%y.%m.%d %H:%M:%S',
                         '%d.%m.%Y %H:%M', '%d.%m.%Y %H:%M:%S', '%Y.%m.%d %H:%M', '%Y.%m.%d %H:%M:%S')
            for fmt in dt_format:
                try:
                    return datetime.datetime.strptime(str(self.value), fmt)
                except ValueError:
                    pass
        return self.value

    def improve_ref(self):
        # TODO: Consultation necessary.
        #  Which value is set if no reference exists.
        pass
