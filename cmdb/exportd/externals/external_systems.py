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

from cmdb.exportd.exporter_base import ExternalSystem, ExportJobConfigException, ExportVariable


class ExternalSystemDummy(ExternalSystem):

    parameters = [
        {"name": "ip-address", "required": False, "description": "Set static IP addresses", "default": "192.168.0.2"},
        {"name": "ssid-name", "required": True, "description": "Router for Login", "default": "host-name"},
        {"name": "password", "required": True, "description": "Password for Login", "default": "1234"}
    ]

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemDummy, self).__init__(destination_parms, export_vars)
        # init destination vars
        self.__ip = self._destination_parms.get("ip-address", None)
        self.__user = self._destination_parms.get("ssid-name", None)
        self.__password = self._destination_parms.get("password", None)
        if not (self.__ip and self.__user and self.__password):
            raise ExportJobConfigException()
        # init export vars
        self.__objectid = self._export_vars.get("objectid", ExportVariable("objectid", ""))
        self.__dummy1 = self._export_vars.get("dummy1", ExportVariable("dummy1", ""))
        self.__dummy2 = self._export_vars.get("dummy2", ExportVariable("dummy2", ""))
        self.__dummy3 = self._export_vars.get("dummy3", ExportVariable("dummy3", ""))
        self.__dummy4 = self._export_vars.get("dummy4", ExportVariable("dummy4", ""))

    def prepare_export(self):
        print("prepare export")
        print("destination parms: IP-Address={} SSID={} Password={}".format(self.__ip, self.__user, self.__password))

    def add_object(self, cmdb_object):
        # print values of export variables
        object_id = self.__objectid.get_value(cmdb_object)
        dummy1 = self.__dummy1.get_value(cmdb_object)
        dummy2 = self.__dummy2.get_value(cmdb_object)
        dummy3 = self.__dummy3.get_value(cmdb_object)
        dummy4 = self.__dummy4.get_value(cmdb_object)
        print("object {}".format(object_id))
        print("dummy1: {}; dummy2: {}; dummy3: {}; dummy4: {}".format(dummy1, dummy2, dummy3, dummy4))
        print("")

    def finish_export(self):
        print("finish export")
