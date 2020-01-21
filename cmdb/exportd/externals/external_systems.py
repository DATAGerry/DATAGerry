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
import re
from cmdb.exportd.exporter_base import ExternalSystem, ExportVariable


class ExternalSystemDummy(ExternalSystem):

    parameters = [
        {"name": "ip-address", "required": False, "description": "Set static IP addresses", "default": "192.168.0.2"},
        {"name": "ssid-name", "required": True, "description": "Router for Login", "default": "host-name"},
        {"name": "password", "required": True, "description": "Password for Login", "default": "1234"}
    ]

    variables = [
        {"name": "dummy1", "required": False, "description": "No dummy1 are needed."},
        {"name": "dummy2", "required": False, "description": "No dummy2 are needed."},
        {"name": "dummy3", "required": False, "description": "No dummy3 are needed."},
        {"name": "dummy4", "required": False, "description": "No dummy4 are needed."}
    ]

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemDummy, self).__init__(destination_parms, export_vars)
        # init destination vars
        self.__ip = self._destination_parms.get("ip-address")
        self.__user = self._destination_parms.get("ssid-name")
        self.__password = self._destination_parms.get("password")
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
        {"name": "exportSnmpConfig", "required": False, "description": "also export SNMP configuration for nodes", "default": "false"},
        {"name": "exportSnmpConfigRetries", "required": False, "description": "export SNMP configuration for nodes: set SNMP retries", "default": "1"},
        {"name": "exportSnmpConfigTimeout", "required": False, "description": "export SNMP configuration for nodes: set SNMP timeout", "default": "2000"}
    ]

    variables = [
        {"name": "nodelabel", "required": True, "description": "nodelabel for the OpenNMS node."},
        {"name": "ip", "required": True, "description": "ip address to add in OpenNMS"},
        {"name": "furtherIps", "required": False, "description": "further ip addresses to add to OpenNMS node. Format: IP1;IP2;IP3."},
        {"name": "asset_", "required": False, "description": "content for asset field e.g. - asset_city for adding information to the city field"},
        {"name": "category_", "required": False, "description": "use variable value of the field to define a category e.g. - category_1"},
        {"name": "snmp_community", "required": False, "description": "SNMP community of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true."},
        {"name": "snmp_version", "required": False, "description": "SNMP version of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true. Currently the exporter supports only v1/v2c"}
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
        # init destination vars
        self.__services = self._destination_parms.get("services").split()
        self.__snmp_export = False
        if bool(self._destination_parms.get("exportSnmpConfig")):
            self.__snmp_export = True
        # init error handling
        self.__obj_successful = []
        self.__obj_warning = []
        # init variables
        self.__timeout = 10
        self.__xml = None

    def prepare_export(self):
        # check connection to OpenNMS
        self.__onms_check_connection()
        # init XML object for OpenNMS REST API
        attributes = {}
        attributes["foreign-source"] = self._destination_parms["requisition"]
        self.__xml = ET.Element("model-import", attributes)

    def add_object(self, cmdb_object):
        # init error handling
        warning = False

        # get node variables
        node_foreignid = cmdb_object.object_information['object_id']
        node_label = self._export_vars.get("nodelabel", ExportVariable("nodelabel", "undefined")).get_value(cmdb_object)
        node_location = self._export_vars.get("location", ExportVariable("location", "default")).get_value(cmdb_object)

        # get interface information
        interfaces_in = []
        interfaces_in.append(self._export_vars.get("ip", ExportVariable("ip", "127.0.0.1")).get_value(cmdb_object))
        interfaces_in.extend(self._export_vars.get("furtherIps", ExportVariable("furtherIps", "[]")).get_value(cmdb_object).split(";"))
        # validate interfaces
        interfaces = []
        for interface in interfaces_in:
            if self.__check_ip(interface):
                interfaces.append(interface)
            else:
                warning = True
        interfaces = list(set(interfaces))

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
        self.__obj_successful.append(cmdb_object.object_information['object_id'])
        if warning:
            self.__obj_warning.append(cmdb_object.object_information['object_id'])

    def finish_export(self):
        self.__onms_update_requisition()
        self.__onms_sync_requisition()
        # create result message
        msg = "Export to OpenNMS finished. "
        msg += "{} objects exported. ".format(len(self.__obj_successful))
        msg += "The following objects were exported with warnings: {}".format(self.__obj_warning)
        self.set_msg(msg)

    def __onms_check_connection(self):
        url = "{}/info".format(self._destination_parms["resturl"])
        try:
            response = requests.get(url, auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]), verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except Exception:
            self.error("Can't connect to OpenNMS API")
        return True

    def __onms_update_requisition(self):
        url = "{}/requisitions".format(self._destination_parms["resturl"])
        data = ET.tostring(self.__xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.post(url, data=data, headers=headers, auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]),
                                     verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except Exception:
            self.error("Can't connect to OpenNMS API")
        return True

    def __onms_sync_requisition(self):
        url = "{}/requisitions/{}/import".format(self._destination_parms["resturl"], self._destination_parms["requisition"])
        try:
            response = requests.put(url, data="", auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]), verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except Exception:
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
        snmp_retries_xml.text = self._destination_parms["exportSnmpConfigRetries"]
        snmp_timeout_xml = ET.SubElement(snmp_config_xml, "timeout")
        snmp_timeout_xml.text = self._destination_parms["exportSnmpConfigTimeout"]
        snmp_version = ET.SubElement(snmp_config_xml, "version")
        snmp_version.text = version

        # send XML to OpenNMS
        url = "{}/snmpConfig/{}".format(self._destination_parms["resturl"], ip)
        data = ET.tostring(snmp_config_xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.put(url, data=data, headers=headers, auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]),
                                    verify=False, timeout=self.__timeout)
            if response.status_code > 204:
                self.error("Error communicating to OpenNMS: HTTP/{}".format(str(response.status_code)))
        except Exception:
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
        except Exception:
            return None
        if asset_length and len(asset_value) > asset_length:
            asset_value = asset_value[:asset_length]
        return asset_value


class ExternalSystemCpanelDns(ExternalSystem):

    parameters = [
        {"name": "cpanelApiUrl",        "required": True,   "description": "cPanel API base URL", "default": "https://1.2.3.4:2083/json-api"},
        {"name": "cpanelApiUser",       "required": True,   "description": "cPanel username", "default": "admin"},
        {"name": "cpanelApiPassword",   "required": True,   "description": "cPanel password", "default": "admin"},
        {"name": "cpanelApiToken",      "required": True,   "description": "cPanel token", "default": ""},
        {"name": "domainName",          "required": True,   "description": "DNS Zone managed by cPanel for adding DNS A records", "default": "objects.datagerry.com"},
        {"name": "cpanelApiSslVerify",  "required": False,  "description": "disable SSL peer verification", "default": False}
    ]

    variables = [
        {"name": "hostname",    "required": True,   "description": "host part of the DNS A record. e.g. - test"},
        {"name": "ip",          "required": True,   "description": "ip address of the DNS A record. e.g. - 8.8.8.8"}
    ]

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemCpanelDns, self).__init__(destination_parms, export_vars)

        self.__variables = export_vars

        # get parameters for cPanel access
        self.__cpanel_api_user = self._destination_parms.get("cpanelApiUser")
        self.__cpanel_api_password = self._destination_parms.get("cpanelApiPassword")
        self.__cpanel_api_token = self._destination_parms.get("cpanelApiToken")
        self.__domain_name = self._destination_parms.get("domainName")
        self.__cpanel_api_url = self._destination_parms.get("cpanelApiUrl")
        self.__cpanel_api_url += "/cpanel?cpanel_jsonapi_user={}".format(self.__cpanel_api_user)
        self.__cpanel_api_url += "&cpanel_jsonapi_apiversion=2&"

        if not (self.__cpanel_api_user and self.__cpanel_api_password and self.__domain_name and self.__cpanel_api_url):
            self.error("Parameters for ExternalSystem not set correctly")

        # SSL verify option
        self.__cpanel_api_ssl_verify = self._destination_parms.get("cpanelApiSslVerify")

        # get all existing DNS records from cPanel
        self.__existing_records = self.get_a_records(self.__domain_name)
        self.__created_records = {}

    def add_object(self, cmdb_object):
        # get variables from object
        hostname = self.format_hostname(str(self._export_vars.get("hostname", ExportVariable("hostname", "default")).get_value(cmdb_object)))
        ip = self.format_ip(str(self._export_vars.get("ip", ExportVariable("ip", "")).get_value(cmdb_object)))

        # ignore CmdbObject,
        if ip == "" or hostname == "":
            self.set_msg('Ignore CmdbObject ID:%s. IP and/or hostname is invalid' % cmdb_object.object_information['object_id'])

        # check if a DNS record exist for object
        if hostname in self.__existing_records.keys():
            # check if entry has changed
            if self.__existing_records[hostname]["data"] != ip:
                if hostname not in self.__created_records.keys():
                    # recreate entry
                    self.delete_a_records(self.__domain_name, hostname)
                    self.add_a_record(self.__domain_name, hostname, ip)

            # delete entry from exitsing records array
            del self.__existing_records[hostname]
        else:
            # if not create a new one
            if hostname not in self.__created_records.keys():
                self.add_a_record(self.__domain_name, hostname, ip)

        # save to created records
        self.__created_records[hostname] = ip

    def finish_export(self):
        # delete all DNS A records that does not exist in DATAGERRY
        for hostname in self.__existing_records:
            self.delete_a_records(self.__domain_name, hostname)

    def get_a_records(self, cur_domain: str):
        """
        Gets all DNS A records for the given domain
        Args:
            cur_domain: DNS zone to get the A records.
        Returns:
            A records with hostname -> IP
        """
        url_parameters = "cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=fetchzone&domain={}{}".format(cur_domain, "&type=A")
        json_result = self.get_data(url_parameters)

        if json_result['cpanelresult']['data'][0]['status'] == 0:
            self.error(json_result['cpanelresult']['data'][0]['statusmsg'])

        records = json_result['cpanelresult']['data'][0]['record']

        # create output array
        output = {}

        for record in records:
            record_hostname = ''
            record_data = ''
            record_line = ''

            if 'name' in record:
                record_hostname = record['name']
            if 'address' in record:
                record_data = record['address']
            if 'line' in record:
                record_line = record['line']

            # format hostname
            matches = re.search(r'(.*?).%s?.' % cur_domain, record_hostname)
            if matches:
                record_hostname = matches.group(1)
                output.update({record_hostname: {"data": record_data, "line": record_line}})

        return output

    def get_data(self, url: str):
        """
        Sends an HTTP request to cPanel and returns result
        Args:
            url: part of the URL request to use.
        Returns:
            JSON data, which are returned from API
        """
        from requests.exceptions import HTTPError
        json_result = {}

        try:
            # curl request
            __session__ = requests.Session()
            __session__.auth = (self.__cpanel_api_user, self.__cpanel_api_password)

            headers = {
                'Authorization': 'WHM %s:%s' % (self.__cpanel_api_user, self.__cpanel_api_token),
            }
            url = self.__cpanel_api_url + url
            response = requests.get(url,
                                    headers=headers,
                                    auth=(self.__cpanel_api_user, self.__cpanel_api_password),
                                    )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            # get JSON data
            json_result = response.json()
            __session__.close()
        except HTTPError as http_err:
            self.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            self.error(f'Other error occurred: {err}')

        return json_result

    def add_a_record(self, cur_domain, cur_hostname, cur_ip):
        """
        Adds an A record to the given domain in cPanel
        Args:
            cur_domain:     domain for adding the record
            cur_hostname:   host part
            cur_ip:         IP address

        Returns:

        """
        url_parameters = "cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=add_zone_record"
        url_parameters += "&domain={}".format(cur_domain)
        url_parameters += "&name={}".format(cur_hostname)
        url_parameters += "&type=A&address={}".format(cur_ip)
        self.get_data(url_parameters)

    def delete_a_records(self, cur_domain, cur_hostname):
        """
        Adds an A record to the given domain in cPanel
        Args:
            cur_domain:     domain for adding the record
            cur_hostname:   host part

        Returns:

        """
        # get all A records in zone
        records = self.get_a_records(cur_domain)
        for r_name in records:
            # check if record has the correct name
            if r_name == cur_hostname:
                # delete enty
                url_parameters = "cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=remove_zone_record"
                url_parameters += "&domain={}&line={}".format(cur_domain, str(records[r_name]['line']))
                self.get_data(url_parameters)

    def format_hostname(self, value: str) -> str:
        """
    Checks, if a hostname has the correct format.
        Args:
            value: input in the correct format.
        Returns:
            Value in the correct format.
        """
        value = re.sub(r' ', "", value)
        value = re.sub(r'[^A-Za-z0-9\-\.]', "", value)
        return value

    def format_ip(self, value) -> str:
        """
        Checks if an IPv4 address has the correct format
        Args:
            value: input address.
        Returns:
            The correct format. Empty string, if not.
        """
        import ipaddress
        try:
            if ipaddress.IPv4Address(value) or ipaddress.IPv6Address(value):
                return value
        except:
            return ""
        return ""


class ExternalSystemCsv(ExternalSystem):

    parameters = [
        {"name": "csv_filename", "required": False, "description": "name of the output CSV file. Default: stdout",
         "default": "/tmp/testfile.csv"},
        {"name": "csv_delimiter", "required": False, "description": "CSV delimiter. Default: ';'", "default": ";"},
        {"name": "csv_enclosure", "required": False, "description": "CSV enclosure. Default: '“'", "default": '”'}
    ]

    variables = [{}]

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemCsv, self).__init__(destination_parms, export_vars)
        self.__variables = export_vars

        # get parameters for cPanel access
        self.filename = self._destination_parms.get("csv_filename")
        self.delimiter = self._destination_parms.get("csv_delimiter")
        self.enclosure = self._destination_parms.get("csv_enclosure")
        self.header = set([])
        self.rows = []

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object):
        row = {}
        fields = cmdb_object.fields
        for key in self.__variables:
            self.header.add(key)
            for field in fields:
                row.update({key: str(self._export_vars.get(key, ExportVariable(key, "")).get_value(cmdb_object))})
        self.rows.append(row)

    def finish_export(self):
        import csv
        with open(self.filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header, delimiter=self.delimiter, quotechar=self.enclosure)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)
