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

import xml.etree.ElementTree as ET
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



class ExternalSystemOpenNMS(ExternalSystem):

    parameters = [
        {"name": "resturl", "required": True, "description": "OpenNMS REST URL", "default": "http://127.0.0.1:8980/opennms/rest"},
        {"name": "restuser", "required": True, "description": "OpenNMS REST user", "default": "admin"},
        {"name": "restpassword", "required": True, "description": "OpenNMS REST password", "default": "admin"},
        {"name": "requisition", "required": True, "description": "OpenNMS requisition to use", "default": "cmdb"},
        {"name": "services", "required": False, "description": "name of services to bind on each node sepetated by space", "default": "ICMP SNMP"},
        {"name": "sslVerify", "required": False, "description": "disable SSL peer verification", "default": "false"},
        {"name": "rescanExisting", "required": False, "description": "set rescanExisting flag for OpenNMS import", "default": "dbOnly"},
        {"name": "exportSnmpConfig", "required": False, "description": "also export SNMP configuration for nodes", "default": "false"},
        {"name": "exportSnmpConfigRetries", "required": False, "description": "export SNMP configuration for nodes: set SNMP retries", "default": "1"},
        {"name": "exportSnmpConfigTimeout", "required": False, "description": "export SNMP configuration for nodes: set SNMP timeout", "default": "2000"}
    ]

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemOpenNMS, self).__init__(destination_parms, export_vars)
        # ToDo: init destination vars
        self.__requisition = self._destination_parms.get("requisition", None)
        self.__services = self._destination_parms.get("services", "ICMP SNMP").split()
        if not (self.__requisition):
            raise ExportJobConfigException()


    def prepare_export(self):
        # init XML object for OpenNMS REST API
        attributes = {}
        attributes["foreign-source"] = self.__requisition
        self.__xml = ET.Element("model-import", attributes)

    def add_object(self, cmdb_object):
        # get node variables
        node_foreignid = cmdb_object.get_public_id()
        node_label = self._export_vars.get("nodelabel", ExportVariable("nodelabel", "undefined")).get_value(cmdb_object)
        node_location = self._export_vars.get("location", ExportVariable("location", "default")).get_value(cmdb_object)

        # get interface information
        interfaces_in = []
        interfaces_in.append(self._export_vars.get("ip", ExportVariable("ip", "127.0.0.1")).get_value(cmdb_object))
        # ToDo
        #interfaces_in = interfaces_in + self._export_vars.get("furtherIps", ExportVariable("furtherIps", "")).get_value(cmdb_object)).split()
        # validate interfaces
        interfaces = []
        for interface in interfaces_in:
            if self.__check_ip(interface):
                interfaces.append(interface)
        # ToDo: remove dupplicate IPs

        # get category information
        categories = []
        for export_var in self._export_vars:
            if export_var.startswith("category_"):
                categories.append(self._export_vars.get(export_var).get_value(cmdb_object))

        # get asset information
        assets = {}
        for export_var in self._export_vars:
            if export_var.startswith("asset_"):
                asset_name = export_var.replace("asset_", "", 1)
                # ToDo: check asset field length
                assets[asset_name] = self._export_vars.get(export_var).get_value(cmdb_object)


        # create node XML structure
        # XML: node
        node_xml_attr = {}
        node_xml_attr["foreign-id"] = str(node_foreignid)
        node_xml_attr["node-label"] = str(node_label)
        if node_location != "default":
            node_xml_attr["location"] = str(node_location)
        node_xml = ET.Element("node", node_xml_attr)
        # XML: interface
        for interface in interfaces:
            interface_xml_attr = {}
            interface_xml_attr["ip-addr"] = str(interface)
            interface_xml = ET.SubElement(node_xml, "interface", interface_xml_attr)
            for service in self.__services:
                service_xml_attr = {}
                service_xml_attr["service-name"] = str(service)
                service_xml = ET.SubElement(interface_xml, "monitored-service", service_xml_attr)
        # XML: categories
        for category in categories:
            cat_xml_attr = {}
            cat_xml_attr["name"] = str(category)
            ET.SubElement(node_xml, "category", cat_xml_attr)
        # XML: assets
        for asset in assets:
            asset_xml_attr = {}
            asset_xml_attr["name"] = asset
            asset_xml_attr["value"] = assets[asset]
            ET.SubElement(node_xml, "asset", asset_xml_attr)
        # XML: append structure
        self.__xml.append(node_xml)


    def finish_export(self):
        print(ET.tostring(self.__xml, encoding="unicode", method="xml"))


    def __check_ip(self, input_ip):
        # ToDo
        return True
