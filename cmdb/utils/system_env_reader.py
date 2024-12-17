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
import os
import re

from cmdb.utils.system_reader import SystemReader
# -------------------------------------------------------------------------------------------------------------------- #

class SystemEnvironmentReader(SystemReader):
    """
    Settings reader loads settings from environment variables
    """

    def __init__(self):
        # get all environment variables and store them in config dict
        self.__config = {}
        pattern = re.compile("DATAGERRY_(.*)_(.*)")

        for key, value in os.environ.items():
            match = pattern.fullmatch(key)

            if match:
                section = match.group(1)
                name = match.group(2)

                # save value in config dict
                if section not in self.__config:
                    self.__config[section] = {}
                self.__config[section][name] = value

        super().__init__()


    def get_value(self, name, section):
        """TODO: document"""
        return self.__config[section][name]


    def get_sections(self):
        """TODO: document"""
        return self.__config.keys()


    def get_all_values_from_section(self, section):
        """TODO: document"""
        return self.__config[section]


    def setup(self):
        """TODO: document"""
        raise NotImplementedError
