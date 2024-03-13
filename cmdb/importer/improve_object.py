# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class ImproveObject:
    """TODO: document"""

    def __init__(self, entry: dict, property_entries, field_entries, possible_fields):
        """
        Basic improve super class for object imports
        Args:
            entry: Numbered values of the fields
            property_entries: Object properties (active, public_id, etc)
            field_entries: Field attributes
            possible_fields: Field types
        """
        self.entry = entry
        self.property_entries = property_entries
        self.field_entries = field_entries
        self.possible_fields = possible_fields
        self.value = None
        super()


    def improve_entry(self) -> dict:
        """
        This method converts field values to the appropriate type
        Returns: dict

        """
        # improve properties
        for property_entry in self.property_entries:
            self.value = self.entry.get(property_entry.get_value())
            if property_entry.get_name() == "active":
                self.entry.update({property_entry.get_value(): ImproveObject.improve_boolean(self.value)})

        # improve fields
        for entry_field in self.field_entries:
            for item in self.possible_fields:
                self.value = self.entry.get(entry_field.get_value())
                if item["name"] == entry_field.get_name():
                    if item['type'] == 'date':
                        self.entry.update({entry_field.get_value(): ImproveObject.improve_date(self.value)})
                    if item['type'] == 'text' and not isinstance(self.value, str):
                        self.entry.update({entry_field.get_value(): str(self.value)})
        return self.entry


    @staticmethod
    def improve_boolean(value) -> bool:
        """
        This method converts the value from Type: String to Type: Boolean

        Returns:
            True if value in ['True', 'true', 'TRUE', '1']
            False if value in ['False', 'false', 'FALSE', '0', 'no']

        """
        if isinstance(value, str):
            if value in ['False', 'false', 'FALSE', '0', 'no']:
                return False

            if value in ['True', 'true', 'TRUE', '1']:
                return True

        return value


    @staticmethod
    def improve_date(value):
        """
        This method converts the date format
        Returns:
            datetime parsed from a string

        """
        import datetime

        try:
            if isinstance(value, dict) and value.get('$date'):
                return datetime.datetime.fromtimestamp(value["$date"]/1000)
        except Exception:
            pass

        if isinstance(value, str):
            dt_format = ('%Y/%m/%d', '%Y-%m-%d', '%Y.%m.%d', '%Y,%m,%d',
                         '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d,%m,%Y',
                         '%d.%m.%y %H:%M', '%d.%m.%y %H:%M:%S', '%y.%m.%d %H:%M', '%y.%m.%d %H:%M:%S',
                         '%d.%m.%Y %H:%M', '%d.%m.%Y %H:%M:%S', '%Y.%m.%d %H:%M', '%Y.%m.%d %H:%M:%S',
                         '%d-%m-%y %H:%M', '%d-%m-%y %H:%M:%S', '%y-%m-%d %H:%M', '%y-%m-%d %H:%M:%S',
                         '%d-%m-%Y %H:%M', '%d-%m-%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S')
            for fmt in dt_format:
                try:
                    return datetime.datetime.strptime(str(value), fmt)
                except ValueError:
                    pass
        return value
