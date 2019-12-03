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

import ipaddress
import xml.etree.ElementTree as ET
import requests
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
            self.error("missing parameters")
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
        {"name": "rescanExisting", "required": False, "description": "set rescanExisting flag for OpenNMS import", "default": "dbOnly"},
        {"name": "exportSnmpConfig", "required": False, "description": "also export SNMP configuration for nodes", "default": "false"},
        {"name": "exportSnmpConfigRetries", "required": False, "description": "export SNMP configuration for nodes: set SNMP retries", "default": "1"},
        {"name": "exportSnmpConfigTimeout", "required": False, "description": "export SNMP configuration for nodes: set SNMP timeout", "default": "2000"}
    ]

    onms_assetfields = {
        "category": None,
        "manufacturer": None,
        "vendor": None,
        "modelNumber": None,
        "serialNumber": None,
        "description": None,
        "circuitId": None,
        "assetNumber": None,
        "operatingSystem": None,
        "rack": None,
        "rackunitheight": 2,
        "slot": None,
        "port": None,
        "region": None,
        "division": None,
        "department": None,
        "address1": None,
        "address2": None,
        "city": None,
        "state": None,
        "zip": None,
        "building": None,
        "floor": None,
        "room": None,
        "vendorPhone": None,
        "vendorFax": None,
        "vendorAssetNumber": None,
        "dateInstalled": 64,
        "lease": None,
        "leaseExpires": 64,
        "supportPhone": None,
        "maintcontract": None,
        "maintContractExpiration": 64,
        "displayCategory": None,
        "notifyCategory": None,
        "pollerCategory": None,
        "thresholdCategory": None,
        "comment": None,
        "username": None,
        "password": None,
        "enable": None,
        "connection": 32,
        "cpu": None,
        "ram": None,
        "storagectrl": None,
        "hdd1": None,
        "hdd2": None,
        "hdd3": None,
        "hdd4": None,
        "hdd5": None,
        "hdd6": None,
        "admin": None,
        "snmpcommunity": 32,
        "country": None,
        "latitude": 32,
        "longitude": 32
    }

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemOpenNMS, self).__init__(destination_parms, export_vars)
        # ToDo: init destination vars; get default values from parameters
        self.__resturl = self._destination_parms.get("resturl", "http://127.0.0.1:8980/opennms/rest")
        self.__restuser = self._destination_parms.get("restuser", "admin")
        self.__restpassword = self._destination_parms.get("restpassword", "admin")
        self.__requisition = self._destination_parms.get("requisition", "cmdb")
        self.__services = self._destination_parms.get("services", "ICMP SNMP").split()
        if not (self.__requisition):
            self.error("configuration error: parameter requisition not set")
        self.__snmp_export = False
        if self._destination_parms.get("exportSnmpConfig", "false") in ["True", "true"]:
            self.__snmp_export = True
        self.__snmp_retries = self._destination_parms.get("exportSnmpConfigRetries", "1")
        self.__snmp_timeout = self._destination_parms.get("exportSnmpConfigTimeout", "2000")
        # init error handling
        self.__counter_successful = 0
        self.__counter_failed = 0
        self.__timeout = 10



    def prepare_export(self):
        # check connection to OpenNMS
        self.__onms_check_connection()
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
                asset_value = self.__check_asset(asset_name, self._export_vars.get(export_var).get_value(cmdb_object))
                if asset_value:
                    assets[asset_name] = asset_value


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
                ET.SubElement(interface_xml, "monitored-service", service_xml_attr)
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

        # update SNMP config if option is set
        if self.__snmp_export:
            snmp_ip = str(self._export_vars.get("ip", ExportVariable("ip", "127.0.0.1")).get_value(cmdb_object))
            snmp_community = str(self._export_vars.get("snmp_community", ExportVariable("snmp_community", "public")).get_value(cmdb_object))
            snmp_version = str(self._export_vars.get("snmp_version", ExportVariable("snmp_version", "v2c")).get_value(cmdb_object))
            self.__onms_update_snmpconf_v12(snmp_ip, snmp_community, snmp_version)

        # update error counter
        self.__counter_successful += 1


    def finish_export(self):
        self.__onms_update_requisition()
        self.__onms_sync_requisition()
        self.set_msg("{} objects exported to OpenNMS".format(self.__counter_successful))

    def __onms_check_connection(self):
        url = "{}/info".format(self.__resturl)
        try:
            response = requests.get(url, auth=(self.__restuser, self.__restpassword), verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except:
            self.error("Can't connect to OpenNMS API")
        return True

    def __onms_update_requisition(self):
        url = "{}/requisitions".format(self.__resturl)
        data = ET.tostring(self.__xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.post(url, data=data, headers=headers, auth=(self.__restuser, self.__restpassword),
                                     verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except:
            self.error("Can't connect to OpenNMS API")
        return True

    def __onms_sync_requisition(self):
        url = "{}/requisitions/{}/import".format(self.__resturl, self.__requisition)
        try:
            response = requests.put(url, data="", auth=(self.__restuser, self.__restpassword), verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except:
            self.error("Can't connect to OpenNMS API")
        return True

    def __onms_update_snmpconf_v12(self, ip, community, version="v2c", port="161"):
        # create XML
        snmp_config_xml = ET.Element("snmp-info")
        snmp_community_xml = ET.SubElement(snmp_config_xml, "readCommunity")
        snmp_community_xml.text = community
        snmp_port_xml = ET.SubElement(snmp_config_xml, "port")
        snmp_port_xml.text = port
        snmp_retries_xml = ET.SubElement(snmp_config_xml, "retries")
        snmp_retries_xml.text = self.__snmp_retries
        snmp_timeout_xml = ET.SubElement(snmp_config_xml, "timeout")
        snmp_timeout_xml.text = self.__snmp_timeout
        snmp_version = ET.SubElement(snmp_config_xml, "version")
        snmp_version.text = version
        
        # send XML to OpenNMS
        url = "{}/snmpConfig/{}".format(self.__resturl, ip)
        data = ET.tostring(snmp_config_xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.put(url, data=data, headers=headers, auth=(self.__restuser, self.__restpassword),
                                    verify=False, timeout=self.__timeout)
            if response.status_code > 204:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except:
            self.error("Can't connect to OpenNMS API")
        return True


    def __check_ip(self, input_ip):
        try:
            ipaddress.ip_address(input_ip)
        except ValueError:
            return False
        return True

    def __check_asset(self, asset_name, asset_value):
        try:
            asset_length = self.__class__.onms_assetfields[asset_name]
        except:
            return None
        if asset_length and len(asset_value) > asset_length:
            asset_value = asset_value[:asset_length]
        return asset_value
