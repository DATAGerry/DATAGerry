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
"""TODO. document"""
import ipaddress
import xml.etree.ElementTree as ET
import json
import re
import os
import subprocess
import requests
import pymysql

from cmdb.exportd.exporter_base import ExternalSystem, ExportVariable
from cmdb.exportd.exportd_header.exportd_header import ExportdHeader
# -------------------------------------------------------------------------------------------------------------------- #

class ExternalSystemDummy(ExternalSystem):
    """TODO. document"""
    parameters = []

    variables = [{}]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        self.__rows = []


    def prepare_export(self):
        pass


    def add_object(self, cmdb_object, template_data):
        row = {}
        row["object_id"] = str(cmdb_object.object_information['object_id'])
        if self.event:
            row["event"] = self.event.get_param('event')
        row["variables"] = {}
        for key in self._export_vars:
            row["variables"][key] = str(self._export_vars\
                                        .get(key, ExportVariable(key, ""))\
                                        .get_value(cmdb_object, template_data))

        self.__rows.append(row)


    def finish_export(self):
        json_data = json.dumps(self.__rows)
        print(json_data)
        header = ExportdHeader(json_data)
        return header


class ExternalSystemOpenNMS(ExternalSystem):
    """TODO. document"""
    parameters = [
        {
            "name": "resturl",
            "required": True,
            "description": "OpenNMS REST URL",
            "default": "http://127.0.0.1:8980/opennms/rest"
        },
        {
            "name": "restuser",
            "required": True,
            "description": "OpenNMS REST user",
            "default": "admin"
        },
        {
            "name": "restpassword",
            "required": True,
            "description": "OpenNMS REST password",
            "default": "admin"
        },
        {
            "name": "requisition",
            "required": True,
            "description": "OpenNMS requisition to use",
            "default": "cmdb"
        },
        {
            "name": "services",
            "required": False,
            "description": "name of services to bind on each node sepetated by space",
            "default": "ICMP SNMP"
        },
        {
            "name": "exportSnmpConfig",
            "required": False,
            "description": "also export SNMP configuration for nodes",
            "default": "false"
        },
        {
            "name": "exportSnmpConfigRetries",
            "required": False,
            "description": "export SNMP configuration for nodes: set SNMP retries",
            "default": "1"
        },
        {
            "name": "exportSnmpConfigTimeout",
            "required": False,
            "description": "export SNMP configuration for nodes: set SNMP timeout",
            "default": "2000"
        }
    ]

    variables = [
        {
            "name": "nodelabel",
            "required": True,
            "description": "nodelabel for the OpenNMS node."
        },
        {
            "name": "ip",
            "required": True,
            "description": "ip address to add in OpenNMS"
        },
        {
            "name": "furtherIps",
            "required": False,
            "description": "further ip addresses to add to OpenNMS node. Format: IP1;IP2;IP3."
        },
        {
            "name": "asset_",
            "required": False,
            "description": "content for asset field e.g. - asset_city for adding information to the city field"
        },
        {
            "name": "category_",
            "required": False,
            "description": "use variable value of the field to define a category e.g. - category_1"
        },
        {
            "name": "snmp_community",
            "required": False,
            "description": "SNMP community of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true."
        },
        {
            "name": "snmp_version",
            "required": False,
            "description": "SNMP version of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true. \
                            Currently the exporter supports only v1/v2c"
        }
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


    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        # init destination vars
        self.__services = self._destination_parms.get("services").split()
        self.__snmp_export = False
        if self._destination_parms.get("exportSnmpConfig") in ['true', 'True']:
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


    def add_object(self, cmdb_object, template_data):
        # init error handling
        warning = False

        # get node variables
        node_foreignid = cmdb_object.object_information['object_id']
        node_label = self._export_vars\
                    .get("nodelabel", ExportVariable("nodelabel", "undefined"))\
                    .get_value(cmdb_object, template_data)
        node_location = self._export_vars\
                        .get("location", ExportVariable("location", "default"))\
                        .get_value(cmdb_object, template_data)

        # get interface information
        interfaces_in = []
        interfaces_in.append(self._export_vars\
                            .get("ip", ExportVariable("ip", "127.0.0.1"))\
                            .get_value(cmdb_object, template_data))
        interfaces_in.extend(self._export_vars\
                            .get("furtherIps", ExportVariable("furtherIps", "[]"))\
                            .get_value(cmdb_object, template_data).split(";"))

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
                categories.append(self._export_vars.get(export_var).get_value(cmdb_object, template_data))

        # get asset information
        assets = {}
        for export_var in self._export_vars:
            if export_var.startswith("asset_"):
                asset_name = export_var.replace("asset_", "", 1)
                asset_value = self.__check_asset(asset_name, self._export_vars\
                                                .get(export_var)\
                                                .get_value(cmdb_object, template_data))
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
            if category:
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
            snmp_ip = str(self._export_vars\
                         .get("ip", ExportVariable("ip", "127.0.0.1"))\
                         .get_value(cmdb_object, template_data))
            snmp_community = str(self._export_vars\
                                .get("snmp_community", ExportVariable("snmp_community", "public"))\
                                .get_value(cmdb_object, template_data))
            snmp_version = str(self._export_vars\
                               .get("snmp_version", ExportVariable("snmp_version", "v2c"))\
                               .get_value(cmdb_object, template_data))

            if self.__check_ip(snmp_ip):
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
        msg += f"{len(self.__obj_successful)} objects exported. "
        msg += f"The following objects were exported with warnings: {self.__obj_warning}"
        self.set_msg(msg)


    def __onms_check_connection(self):
        url = f"{self._destination_parms['resturl']}/info"
        try:
            response = requests.get(url,
                                    auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]),
                                    verify=False, timeout=self.__timeout)
            if response.status_code > 202:
                self.error(f"Error communicating to OpenNMS: HTTP/{str(response.status_code)}")
        except Exception:
            self.error("Can't connect to OpenNMS API")
        return True



    def __onms_update_requisition(self):
        rest_url = self._destination_parms["resturl"]
        url = f"{rest_url}/requisitions"
        data = ET.tostring(self.__xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.post(
                                url,
                                data=data,
                                headers=headers,
                                auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]),
                                verify=False,
                                timeout=self.__timeout)

            if response.status_code > 202:
                self.error(f"Error communicating to OpenNMS: HTTP/{str(response.status_code)}")
        except Exception:
            self.error("Can't connect to OpenNMS API")
        return True


    def __onms_sync_requisition(self):
        url = f"{self._destination_parms['resturl']}/requisitions/{self._destination_parms['requisition']}/import"
        try:
            response = requests.put(
                                url,
                                data="",
                                auth=(self._destination_parms["restuser"], self._destination_parms["restpassword"]),
                                verify=False,
                                timeout=self.__timeout)

            if response.status_code > 202:
                self.error(f"Error communicating to OpenNMS: HTTP/{str(response.status_code)}")
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
        url = f"{self._destination_parms['resturl']}/snmpConfig/{ip}"
        data = ET.tostring(snmp_config_xml, encoding="utf-8", method="xml")
        headers = {
            "Content-Type": "application/xml"
        }
        try:
            response = requests.put(url,
                                    data=data,
                                    headers=headers,
                                    auth=(self._destination_parms["restuser"],self._destination_parms["restpassword"]),
                                    verify=False,
                                    timeout=self.__timeout)
            if response.status_code > 204:
                self.error(f"Error communicating to OpenNMS: HTTP/{str(response.status_code)}")
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
    """TODO: document"""
    parameters = [
        {
            "name": "cpanelApiUrl",
            "required": True,
            "description": "cPanel API base URL",
            "default": "https://1.2.3.4:2083/json-api"
        },
        {
            "name": "cpanelApiUser",
            "required": True,
            "description": "cPanel username",
            "default": "admin"
        },
        {
            "name": "cpanelApiPassword",
            "required": True,
            "description": "cPanel password",
            "default": "admin"
        },
        {
            "name": "cpanelApiToken",
            "required": True,
            "description": "cPanel token",
            "default": ""
        },
        {
            "name": "domainName",
            "required": True,
            "description": "DNS Zone managed by cPanel for adding DNS A records",
            "default": "objects.datagerry.com"
        },
        {
            "name": "cpanelApiSslVerify",
            "required": False,
            "description": "disable SSL peer verification",
            "default": False
        }
    ]

    variables = [
        {
            "name": "hostname",
            "required": True,
            "description": "host part of the DNS A record. e.g. - test"
        },
        {
            "name": "ip",
            "required": True,
            "description": "ip address of the DNS A record. e.g. - 8.8.8.8"
        }
    ]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)

        self.__variables = export_vars

        # get parameters for cPanel access
        self.__cpanel_api_user = self._destination_parms.get("cpanelApiUser")
        self.__cpanel_api_password = self._destination_parms.get("cpanelApiPassword")
        self.__cpanel_api_token = self._destination_parms.get("cpanelApiToken")
        self.__domain_name = self._destination_parms.get("domainName")
        self.__cpanel_api_url = self._destination_parms.get("cpanelApiUrl")
        self.__cpanel_api_url += f"/cpanel?cpanel_jsonapi_user={self.__cpanel_api_user}"
        self.__cpanel_api_url += "&cpanel_jsonapi_apiversion=2&"

        if not (self.__cpanel_api_user and self.__cpanel_api_password and self.__domain_name and self.__cpanel_api_url):
            self.error("Parameters for ExternalSystem not set correctly")

        # SSL verify option
        self.__cpanel_api_ssl_verify = self._destination_parms.get("cpanelApiSslVerify")

        # get all existing DNS records from cPanel
        self.__existing_records = self.get_a_records(self.__domain_name)
        self.__created_records = {}


    def add_object(self, cmdb_object, template_data):
        # get variables from object
        hostname = self.format_hostname(str(self._export_vars\
                                            .get("hostname", ExportVariable("hostname", "default"))\
                                            .get_value(cmdb_object, template_data)))
        ip = self.format_ip(str(self._export_vars\
                                .get("ip", ExportVariable("ip", ""))\
                                .get_value(cmdb_object, template_data)))

        # ignore CmdbObject,
        if ip == "" or hostname == "":
            self.set_msg(f"Ignore CmdbObject ID:{cmdb_object.object_information['object_id']}. \
                           IP and/or hostname is invalid")

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
        url_parameters = f"cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=fetchzone&domain={cur_domain}&type=A"
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
                'Authorization': f'WHM {self.__cpanel_api_user}:{self.__cpanel_api_token}'
            }
            url = self.__cpanel_api_url + url
            response = requests.get(url,
                                    headers=headers,
                                    auth=(self.__cpanel_api_user, self.__cpanel_api_password),
                                    timeout=10)

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
        url_parameters += f"&domain={cur_domain}"
        url_parameters += f"&name={cur_hostname}"
        url_parameters += f"&type=A&address={cur_ip}"
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
        except Exception:
            return ""

        return ""


class ExternalSystemCsv(ExternalSystem):
    """TODO: document"""
    parameters = [
        {
            "name": "csv_filename",
            "required": False,
            "description": "name of the output CSV file. Default: stdout",
            "default": "/tmp/testfile.csv"
        },
        {
            "name": "csv_delimiter",
            "required": False,
            "description": "CSV delimiter. Default: ';'",
            "default": ";"
        },
        {
            "name": "csv_enclosure",
            "required": False,
            "description": "CSV enclosure. Default: '“'",
            "default": '”'
        }
    ]

    variables = [{}]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        self.__variables = export_vars

        # get parameters for cPanel access
        self.filename = self._destination_parms.get("csv_filename")
        self.delimiter = self._destination_parms.get("csv_delimiter")
        self.enclosure = self._destination_parms.get("csv_enclosure")
        self.header = []
        self.rows = []


    def prepare_export(self):
        pass


    def add_object(self, cmdb_object, template_data):
        row = {}
        for key in self.__variables:
            if key not in self.header:
                self.header.append(key)
            row.update({key: str(self._export_vars\
                                .get(key, ExportVariable(key, ""))\
                                .get_value(cmdb_object, template_data))})
        self.rows.append(row)


    def finish_export(self):
        import csv
        with open(self.filename, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    fieldnames=self.header,
                                    delimiter=self.delimiter,
                                    quotechar=self.enclosure)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)


class ExternalSystemAnsible(ExternalSystem):
    """TODO: document"""
    parameters = []

    variables = [
        {
            "name": "hostname",
            "required": True,
            "description": "hostname or IP that Ansible uses for connecting to the host. e.g. - test.example.com"
        },
        {
            "name": "group_",
            "required": True,
            "description": "Ansible group membership. e.g. - group_webservers"
        },
        {
            "name": "hostvar_",
            "required": False,
            "description": "host variables that should be given to Ansible. e.g. - hostvar_snmpread"
        }
    ]


    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        self.__variables = export_vars

        # initialize store for created ansible groups
        self.ansible_groups = {}

        # initialize store for hostvars
        self.ansible_hostvars = {}

        # initialize store for hostname
        self.host_list = []


    def add_object(self, cmdb_object, template_data):
        # get hostname for ansible inventory
        hostname = self._export_vars\
                    .get("hostname", ExportVariable("hostname", "default"))\
                    .get_value(cmdb_object, template_data)

        if hostname:
            self.host_list.append(hostname)

        # walk through all variables to get groups and hostvars
        groups = []
        hostvars = {}

        for v_name in self.__variables:
            # check if it is a "group_" variable
            matches = re.search(r'group_(.*)$', v_name)
            if matches:
                group_name = matches.group(1)
                group_value = self._export_vars\
                                .get(v_name, ExportVariable(v_name, ""))\
                                .get_value(cmdb_object, template_data)

                # check if the value is true
                if group_name != 'all' and group_value in ['true', 'True']:
                    # write to ansible group store
                    groups.append(group_name)

            # check if it is a "hostvar_" variable
            matches = re.search(r'hostvar_(.*)$', v_name)
            if matches:
                host_var_name = matches.group(1)
                host_var_value = self._export_vars\
                                    .get(v_name, ExportVariable(v_name, ""))\
                                    .get_value(cmdb_object, template_data)
                hostvars.update({host_var_name: host_var_value})

        # put all hosts into ansible group all
        groups.append('all')

        # write hostvars to ansible hostvars store
        self.ansible_hostvars.update({hostname: hostvars})

        # update ansible groups
        for group in groups:
            if group not in self.ansible_groups:
                self.ansible_groups[group] = {}
                self.ansible_groups[group]['hosts'] = []
            self.ansible_groups[group]['hosts'].append(hostname)


    def finish_export(self):
        # create JSON
        groups = self.ansible_groups
        groups.update({'_meta': {'hostvars': self.ansible_hostvars}})
        header = ExportdHeader(json.dumps(groups))
        return header


class ExternalSystemExecuteScript(ExternalSystem):
    """TODO: document"""
    parameters = [
        {
            "name": "script",
            "required": True,
            "description": "The script or binary to execute",
            "default": "/opt/scripts/export"
        },
        {
            "name": "timeout",
            "required": True,
            "description": "Timeout for executing the script in seconds",
            "default": "30"
        }
    ]

    variables = [{}]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        # init destination vars
        self.__script = self._destination_parms.get("script")
        self.__timeout = int(self._destination_parms.get("timeout"))
        self.__rows = []
        if not (self.__script and self.__timeout):
            self.error("missing parameters")


    def prepare_export(self):
        pass


    def add_object(self, cmdb_object, template_data):
        row = {}
        row["object_id"] = str(cmdb_object.object_information['object_id'])
        if self.event:
            row["event"] = self.event.get_param('event')
        row["variables"] = {}
        for key in self._export_vars:
            row["variables"][key] = str(self._export_vars\
                                        .get(key, ExportVariable(key, ""))\
                                        .get_value(cmdb_object, template_data))
        self.__rows.append(row)

    def finish_export(self):
        # create json data
        json_data = json.dumps(self.__rows)

        # check permission to execute script
        # try to open permission file
        script_path = os.path.dirname(self.__script)
        script_name = os.path.basename(self.__script)
        permission_filename = os.path.join(script_path, ".datagerry_exec.json")
        try:
            with open(permission_filename, "r", encoding='utf-8') as permission_file:
                permission_data = json.load(permission_file)
                if script_name not in permission_data["allowed_scripts"]:
                    self.error("You are not allowed to execute this script. \
                               Please check your .datagerry_exec.json file.")
        except OSError:
            self.error("You are not allowed to execute this script. Could not open .datagerry_exec.json file.")
        except KeyError:
            self.error("You are not allowed to execute this script. \
                       Please check structure of your .datagerry_exec.json file.")

        # execute script
        try:
            result = subprocess.run(self.__script,
                                    timeout=self.__timeout,
                                    input=json_data,
                                    encoding="utf-8",
                                    check=False)
            if result.returncode != 0:
                self.error("executed script returned an error")
        except FileNotFoundError:
            self.error("could not find script or binary")
        except subprocess.TimeoutExpired:
            self.error("timeout executing script or binary")


class ExternalSystemGenericRestCall(ExternalSystem):
    """TODO: document"""
    parameters = [
        {
            "name": "url",
            "required": True,
            "description": "URL for HTTP POST",
            "default": "https://localhost:8443/dg_export"
        },
        {
            "name": "timeout",
            "required": True,
            "description": "Timeout for executing the REST call in seconds",
            "default": "30"
        },
        {
            "name": "username",
            "required": False,
            "description": "Username for a HTTP basic authentication. If empty, no authentication will be done.",
            "default": ""
        },
        {
            "name": "password",
            "required": False,
            "description": "Password for a HTTP basic authentication.",
            "default": ""
        }
    ]

    variables = [{}]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        # init destination vars
        self.__url = self._destination_parms.get("url")
        self.__timeout = int(self._destination_parms.get("timeout"))
        self.__username = self._destination_parms.get("username")
        self.__password = self._destination_parms.get("password")
        self.__rows = []

        if not (self.__url and self.__timeout):
            self.error("missing parameters")


    def prepare_export(self):
        pass


    def add_object(self, cmdb_object, template_data):
        row = {}
        row["object_id"] = str(cmdb_object.object_information['object_id'])
        if self.event:
            row["event"] = self.event.get_param('event')
        row["variables"] = {}
        for key in self._export_vars:
            row["variables"][key] = str(self._export_vars\
                                        .get(key, ExportVariable(key, ""))\
                                        .get_value(cmdb_object, template_data))
        self.__rows.append(row)


    def finish_export(self):
        # create json data
        json_data = json.dumps(self.__rows)

        # execute REST call
        headers = {
            "Content-Type": "application/json"
        }

        auth = None
        if self.__username:
            auth = (self.__username, self.__password)
        try:
            response = requests.post(self.__url, data=json_data, headers=headers, auth=auth, verify=False,
                                     timeout=self.__timeout)
            if response.status_code > 202:
                self.error(f"Error communicating to REST endpoint: HTTP/{str(response.status_code)}")
        except requests.exceptions.ConnectionError:
            self.error("Can't connect to REST endpoint")
        except requests.exceptions.Timeout:
            self.error("Timeout connecting to REST endpoint")


class ExternalSystemGenericPullJson(ExternalSystem):
    """TODO: document"""
    parameters = []

    variables = [{}]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)
        self.__rows = []

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object, template_data):
        row = {}
        row["object_id"] = str(cmdb_object.object_information['object_id'])
        if self.event:
            row["event"] = self.event.get_param('event')
        row["variables"] = {}
        for key in self._export_vars:
            row["variables"][key] = str(self._export_vars\
                                        .get(key, ExportVariable(key, ""))\
                                        .get_value(cmdb_object, template_data))
        self.__rows.append(row)


    def finish_export(self):
        json_data = json.dumps(self.__rows)
        header = ExportdHeader(json_data)
        return header


class ExternalSystemMySQLDB(ExternalSystem):
    """TODO: document"""
    parameters = [
        {
            "name": "dbserver",
            "required": True,
            "description": "database server",
            "default": "localhost"
        },
        {
            "name": "database",
            "required": True,
            "description": "database name",
            "default": "db"
        },
        {
            "name": "username",
            "required": False,
            "description": "username for database server",
            "default": "user"
        },
        {
            "name": "password",
            "required": False,
            "description": "password for database server",
            "default": "password"
        }
    ]

    variables = [
        {
            "name": "table_<name>",
            "required": True,
            "description": "Sync data with database table <name>."
        }
    ]

    def __init__(self, destination_parms, export_vars, event=None):
        super().__init__(destination_parms, export_vars, event)


        # get table names for sync
        self.__tables = []
        self.__table_data = {}
        for export_var in self._export_vars:
            if export_var.startswith("table_"):
                table_name = export_var.replace("table_", "", 1)
                self.__tables.append(table_name)
                self.__table_data[table_name] = []


    def prepare_export(self):
        pass


    def add_object(self, cmdb_object, template_data):
        # add data for insert statement
        for table in self.__tables:
            varname = "table_" + table
            self.__table_data[table].append(str(self._export_vars\
                                                .get(varname, ExportVariable(varname, ""))\
                                                .get_value(cmdb_object, template_data)))


    def finish_export(self):
        # connect to database
        db_connection = pymysql.connect(host=self._destination_parms.get("dbserver"),
                                        user=self._destination_parms.get("username"),
                                        password=self._destination_parms.get("password"),
                                        db=self._destination_parms.get("database"),
                                        cursorclass=pymysql.cursors.DictCursor,
                                        autocommit=False)

        # handle all database changes within one transaction
        # if something goes wrong, a rollback will be done
        try:
            # beginn transaction
            db_connection.begin()

            # remove all data from existing tables
            for table in self.__tables:
                with db_connection.cursor() as cursor:
                    sql = f"DELETE FROM {table}"
                    cursor.execute(sql)

            # insert new data in all tables
            for table in self.__tables:
                for data in self.__table_data[table]:
                    with db_connection.cursor() as cursor:
                        sql = f"INSERT INTO {table} VALUES({data})"
                        cursor.execute(sql)

            # close transaction
            db_connection.commit()

        finally:
            db_connection.close()
