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
"""
This module handles all predefined section templates
"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            SectionTemplateCreator - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class SectionTemplateCreator:
    """
    This class handles all iteractions with predefined section templates
    """

    def get_predefined_templates(self) -> list:
        """Retrieves all predefined section templates"""
        predefined_templates: list[dict] = []

        predefined_templates.append(self.__get_network_template())
        predefined_templates.append(self.__get_rack_mounting_template())
        predefined_templates.append(self.__get_model_spec_template())

        return predefined_templates

# -------------------------------------------------- HELPER SECTION -------------------------------------------------- #

    def __get_template_section(self, name: str, label) -> dict:
        """
        Retrieves the base section template model

        Args:
            name (str): name for section template
            label (_type_): label for section template

        Returns:
            dict: Base section template construct
        """
        return {
            'is_global': True,
            'predefined': True,
            'name': name,
            'label': label,
            'type': "section",
            'fields': []
        }


    def __get_template_section_field(self,
                                     field_type: str,
                                     name: str,
                                     label: str,
                                     options: list[dict] = None,
                                     regex: str = None,
                                     helper_text: str = None) -> dict:
        """
        Retrieves a field model for a section template

        Args:
            field_type (str): Type of the field like 'text', 'select' etc.
            name (str): Unique identifier for the field
            label (str): label of the field
            options (list[dict], optional): Options for a field of type 'select'. Defaults to None.
            regex (str): The regex which should be applied for the input. Defaults to None.

        Returns:
            dict: The configured field for the section
        """
        field_values = {
            'type': field_type,
            'name': name,
            'label': label
        }

        if options:
            field_values['options'] = options

        if regex:
            field_values['regex'] = regex

        if helper_text:
            field_values['helperText'] = helper_text

        return field_values

# --------------------------------------------------- DATA SECTION --------------------------------------------------- #

    def __get_network_template(self) -> dict:
        """Retrieves the 'Network' predefined section template"""
        network_section = self.__get_template_section("dg-network", "Network")

        network_fields: list[dict] = []

        ipv4_regex: str = ("(\\b25[0-5]|\\b2[0-4][0-9]|\\b[01]?[0-9][0-9]?)"
                           "(\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}")

        ipv4_submask_regex : str =("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}"
                                   "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\/(3[0-2]|[1-2]?\\d)$")

        network_fields.append(self.__get_template_section_field("text",
                                                                "dg-network-ipaddress",
                                                                "IP address",
                                                                None,
                                                                ipv4_regex))
        network_fields.append(self.__get_template_section_field("text", "dg-network-hostname", "Hostname"))
        network_fields.append(self.__get_template_section_field("text", "dg-network-dns", "DNS"))
        network_fields.append(self.__get_template_section_field("text",
                                                                "dg-network-layer3",
                                                                "Layer3-Net",
                                                                None,
                                                                ipv4_submask_regex,
                                                                "IP/Subnet mask"))

        network_section['fields'] = network_fields

        return network_section


    def __get_rack_mounting_template(self) -> dict:
        """Retrieves the 'Rack mounting' predefined section template"""
        rack_section = self.__get_template_section("dg-rackmounting", "Rack mounting")

        rack_fields: list[dict] = []

        positive_integer_regex: str = "^\\d+$"

        rack_fields.append(self.__get_template_section_field("text",
                                                             "dg-rackmounting-ru",
                                                             "Rack units",
                                                             None,
                                                             positive_integer_regex))
        rack_fields.append(self.__get_template_section_field("text",
                                                             "dg-rackmounting-position",
                                                             "Mounting position",
                                                             None,
                                                             positive_integer_regex))

        rack_field_options: list = [
            {
                'name': 'horizontal',
                'label': 'Horizontal'
            },
            {
                'name': 'vertical',
                'label': 'Vertical'
            }
        ]

        rack_fields.append(self.__get_template_section_field("select",
                                                             "dg-rackmounting-orientation",
                                                             "Mounting orientation",
                                                             rack_field_options))

        rack_section['fields'] = rack_fields

        return rack_section


    def __get_model_spec_template(self) -> dict:
        """Retrieves the 'Model specifications' predefined section template"""
        model_spec_section = self.__get_template_section("dg-modelspec", "Model specifications")

        model_spec_fields: list[dict] = []

        model_spec_fields.append(self.__get_template_section_field("text", "dg-modelspec-manufacturer", "Manufacturer"))
        model_spec_fields.append(self.__get_template_section_field("text", "dg-modelspec-model", "Model name"))
        model_spec_fields.append(self.__get_template_section_field("text", "dg-modelspec-serial", "Serial number"))

        model_spec_section['fields'] = model_spec_fields

        return model_spec_section
