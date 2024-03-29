*******
Exportd
*******

Concept
=======
Exportd is an interface for exporting objects to external systems like monitoring systems, ticket systems, backup
software or any kind of other system. Exports are organized in Jobs. A Job contains the following informations:

 * Sources
 * Destinations
 * Variables

A source defines the objects that should be exported to the external system. Multiple sources can be configured per 
Job. A source consists of multiple objects of a specific object type (e.g. router objects) that can be filtered by one or
multiple conditions (e.g. all router objects with field monitoring=true).

A destination is an external system, where you want to push DATAGERRY objects. One or multiple destinations can be
configured per Export Job. A destination consists of an ExternalSystem (e.g. ExternalSystemOpenNMS for an export of
objects to OpenNMS) and parameters, that depends on the ExternalSystem (e.g. resturl/restuser/restpassword for an export
to OpenNMS). DATAGERRY brings some ExternalSystems out of the box, in the near future, it will be possible to add
ExternalSystems with a plugin system.

Variables are a mapping of object data to data that are required for the external system. For example for an export of
objects to a DNS server (to add DNS-A records), hostname and ip are required. In variables a mapping between object
fields and the variable hostname can be configured.

Export Jobs can be triggered manually (by clicking on a button in the webui) or event based, if the configured sources
of a job were changed (e.g. a new object was added).

Export Jobs can be of type *Push* (default) or *Pull*. Push Jobs are a push to an external system, which runs in a
background process, while a *Pull* job is triggered by an external system via REST. The client directly gets the result
within that REST call.



Configuration
=============

Exportd Jobs can be configured in the WebUI under "Task Management" -> "Exportd Job Settings". Add a new Job or edit an
existing one. A wizzard will guide you through the configuration process:


Define Sources
--------------
One or multiple sources can be part of an Export Job. Select the Type of objects you want to export. Add one or multiple
conditions for limitating the export of objects.


Define Destinations
--------------------
Add one or multiple destinations to your Export Job. A destination consists of an ExternalSystem. Choose one out of the
box on the left side and move it to the center area. Depending on the ExternalSystem class, parameters can or must be
set (e.g. the URL of an external system). All parameter wil be preset in the WebUI and you can find a small description
by moving the mouse of the info icon.


Define Export Variables
-----------------------
Depending on the ExternalSystem, Variables must be defined. For example, an export to OpenNMS requires variables like
nodelabel or ip. To find, which variables are available, click on one of the "Variable Helpers". A Variable has a name
and a default value. You also can add other values for specific object types.

The value of a variable is a Jinja2 template. You can use static strings or get data from a specific object. The
following syntax is supported::

    # access the ID of the current object
    {{id}}
    
    # access the field "hostname" of the current object
    {{fields["hostname"]}}
    
    # dereference an object reference in field "location" (access the field "city" of the referenced object)
    # max 3 levels were dereferenced
    {{fields["location"]["fields"]["city"]}}

.. note::
    If you access object fields, use the name of the field instead of the label.



Configure Scheduling
--------------------
This step sets the settings for running exportd jobs.

.. csv-table:: Table 1: Execution settings
   :header: "Execution", "Description"
   :widths: 30 70
   :align: left

   "Run Exportd Job on Event", "It is also possible to run the job event based (this must be enabled in the configuration). That means, the job is triggered, if one of the sources objects has changed or a new object was added. All objects are transmitted that correspond to the previously defined conditions "
   "Transfer subset", "Transfer only the objects that have been changed. Excludes jobs that have been executed manually and jobs that are executed automatically after they have been created."

| When executing the following Exportd jobs, additional 'event' information is transmitted.

- External systems
    * ExternalSystemDummy
    * ExternalSystemExecuteScript
    * ExternalSystemGenericRestCall
    * ExternalSystemGenericPullJson

- Events
    * Run on Event
        * insert
        * update
        * delete
    * Run manual
        * manual
    * After creating Exportd Job
        * automatic

| If the switch 'Run on Event' is set, all objects are transmitted that correspond to the previously defined conditions ( hostname == '.*host').

.. code-block:: json

    [
       {
          "object_id": "1",
          "event": "insert",
          "variables":{
             "hostname": "localhost",
          }
       },
       {
          "object_id": "5",
          "event": "insert",
          "variables":{
             "hostname": "datagerry-host",
          }
       },
    ]

| If the switch 'Transfer subset' is set, only the changed objects are transferred. The condition ( hostname == '.*host'). still applies.

.. code-block:: json

    [
       {
          "object_id": "7",
          "event": "insert",
          "variables":{
             "hostname": "customer-host",
          }
       }
    ]

ExternalSystems
===============

Currently the follwowing ExternalSystems are supported:

.. note::
    You can add your own ExternalSystems with a plugin system, that will be available soon.


.. csv-table:: Table 2: Supported external systems
    :header: "External system", "Description"
    :width: 100%
    :widths: 30 70
    :align: left

    "ExternalSystemAnsible", "Provides a dynamic inventory for Ansible"
    "ExternalSystemCpanelDns", "Creates DNS-A Records in cPanel"
    "ExternalSystemCsv", "Creates a CSV file on the filesystem"
    "ExternalSystemDummy", "A dummy for testing Exportd - will only print some debug output"
    "ExternalSystemExcuteScript", "Executes a script on the DATAGERRY machine"
    "ExternalSystemGenericPullJson", "Provides a JSON structure that can be pulled via the DATAGERRY REST API"
    "ExternalSystemGenericRestCall", "Sends a HTTP POST to an userdefined URL"
    "ExternalSystemMySQLDB", "Syncs CMDB objects to one or multiple MySQL/MariaDB database tables"
    "ExternalSystemOpenNMS", "Add nodes to the monitoring system OpenNMS with the OpenNMS REST API"


ExternalSystemAnsible
---------------------
This class will provide a dynamic inventory for `Ansible <https://ansible.com>`_. and needs to be configured as Pull
Job. The exporter walks through all CMDB objects that are configured as export source and creates Ansible groups. The
output is formatted as JSON and can be pulled with the DATAGERRY REST API.

We provide a little wrapper script in the contrib directory, that can be directly used by Ansible with the `inventory
script plugin <https://docs.ansible.com/ansible/latest/plugins/inventory/script.html>`_:

.. literalinclude:: ../../../contrib/ansible/ansible_dyn_inventory.sh


Download the script and change the config variables to met your DATAGERRY configuration. Start Ansible with the -i flag:

.. code-block:: console

    $ ansible -i ansible_dyn_inventory.sh [...]


This exporter class has no parameters, but needs some Export Variables to be set:

.. csv-table:: Table 3: ExternalSystemAnsible - Supported export variables
    :header: "Name", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "hostname", "True", "hostname or IP that Ansible uses for connecting to the host. e.g. - test.example.com"
    "group\_", "True", "Ansible group membership. e.g. - group\_webservers"
    "hostvar\_", "True", "host variables that should be given to Ansible. e.g. - hostvar\_snmpread"

For each CMDB object the export variable hostname has to be set which is used by Ansible to connect to a CMDB object.
Hosts are organized in Ansible groups. For adding a CMDB object to a specific group, the group\_ variables are used. The
variable name is group\_groupname and the value is True, if the CMDB object should be a member of the group.

Example::

    #variablename: group_webserver
    #value of the variable for object: True
    #behavior: the object is part of the Ansible group webserver.

.. note::
    Checkbox fields in object types are perfect for controlling the group memberships.

You can set host variables for Ansible using the hostvar\_ variables. The variable name is hostvar\_varname, which means,
you can access the value by using the name varname in Ansible.



ExternalSystemCpanelDns
-----------------------
This destination adds DNS A-records for CMDB objects to a given DNS zone in cPanel using the cPanel JSON API version 2.
Any existing A records in that zone, that does not exists as objects in DATAGERRY will be deleted. You can manage other
record types like CNAME or MX records manually in that zone and the exporter will not touch these records.

To use this exporter, you need a valid cPanel account with username and password and a DNS zone, you can manage.
The exporter will not create a DNS zone for you. So the DNS zone should already exist, if you want to use this exporter.

The exporter class has the following parameters:

.. csv-table:: Table 4: ExternalSystemCpanelDns - Supported export parameters
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "cpanelApiUrl", "True", "cPanel API base URL"
    "cpanelApiUser", "True", "cPanel username"
    "cpanelApiPassword", "True", "cPanel password"
    "cpanelApiToken", "True", "cPanel API token"
    "domainName", "True", "DNS Zone managed by cPanel for adding DNS A records"
    "cpanelApiSslVerify", "False", "disable SSL peer verification"


The following variables needs to be set:

.. csv-table:: Table 5: ExternalSystemCpanelDns - Supported export variables
    :header: "Name", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "hostname", "True", "host part of the DNS A record. e.g. - test"
    "ip", "True", "host part of the DNS A record. e.g. - test"


ExternalSystemCsv
-----------------
This class will create a CSV file on the filesystem. 

The exporter class has the following parameters:

.. csv-table:: Table 6: ExternalSystemCsv - Supported export variables
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "csv_filename", "False", "name of the output CSV file. Default: stdout"
    "csv_delimiter", "False", "CSV delimiter. Default: ';'"
    "csv_enclosure", "False", "CSV enclosure."


Each export variable will define a row in the CSV file. The header of the row is the export variable name.



ExternalSystemExecuteScript
---------------------------
This class will execute an external script or binary on the DATAGERRY machine. A JSON structure with object IDs and
export variables will be passed to the external script/binary via stdin. 

The exporter class has the following parameters:

.. csv-table:: Table 7: ExternalSystemExecuteScript - Supported export parameters
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "script", "True", "full path to the script that should be executed"
    "timeout", "True", "timeout for executing the script"


You can define any export variables. All defined export variables will be sent to the executed script/binary via stdin
within a JSON structure. Please see the following section for an example JSON structure:

.. code-block:: json

    [
        {
            "object_id": 1234,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        },
        {
            "object_id": 1235,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        }
    ]


As executing a script or binary on the machine can be a bit of a security concern, we added some extra security feature
for this exporter class. DATAGERRY will look for a file named *.datagerry_exec.json* inside the directory for the script
that should be executed. In that file, every script or binary that should be executed by DATAGERRY needs to be listed.
Please see the following example file:

.. code-block:: json

    {
        "allowed_scripts": ["test2.py"]
    }


DATAGERRY will not execute scripts, that are not listed in a *.datagerry_exec.json* file.



ExternalSystemGenericPullJson
-----------------------------
This class will provide a JSON structure with object IDs and export variables that can be requested by a user via the 
DATAGERRY REST API. It needs to be configured as Pull job. The get the JSON structure, have a look at the following
curl example:

.. code-block:: console

    #!/bin/bash

    # config variables
    DATAGERRY_EXPORT_TASK=taskname
    DATAGERRY_REST_URL=http://127.0.0.1:4000/rest
    DATAGERRY_REST_USER=admin
    DATAGERRY_REST_PASSWORD=admin

    curl \
        -X GET \
        -u "${DATAGERRY_REST_USER}:${DATAGERRY_REST_PASSWORD}" \
        --silent \
        ${DATAGERRY_REST_URL}/exportdjob/pull/${DATAGERRY_EXPORT_TASK}

The exporter class has no parameters.

You can define any export variables. All defined export variables will be included in the JSON structure that will be 
sent as HTTP response. Please see the following section for an example JSON structure:

.. code-block:: json

    [
        {
            "object_id": 1234,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        },
        {
            "object_id": 1235,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        }
    ]



ExternalSystemGenericRestCall
-----------------------------
This class will send an HTTP POST request to an user-defined URL. A JSON structure with object IDs and export variables 
will be sent as data within the HTTP request. 

The exporter class has the following parameters:

.. csv-table:: Table 8: ExternalSystemGenericRestCall - Supported export parameters
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "url", "True", "URL for HTTP POST request"
    "timeout", "True", "timeout for executing the REST call in seconds"
    "username", "False", "Username for a HTTP basic authentication. If empty, no authentication will be done."
    "password", "False", "Password for a HTTP basic authentication."


You can define any export variables. All defined export variables will be sent as JSON structure within the HTTP
request. Please see the following section for an example JSON structure:

.. code-block:: json

    [
        {
            "object_id": 1234,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        },
        {
            "object_id": 1235,
            "variables": 
                {
                    "var1": "value1",
                    "var2": "value2"
                }
        }
    ]


ExternalSystemMySQLDB
---------------------
This exporter synchronizes DATAGERRY objects to one or multiple database tables in a MySQL/MariaDB database. The
synchronization is done within one database transaction. At first, the content of the configured tables will be deleted.
After that, the new data will be inserted. If anything goes wrong (e.g. a table does not exist, there is an error in SQL
syntax, etc.), a rollback will be done.

The exporter class has the following parameters:

.. csv-table:: Table 9: ExternalSystemMySQLDB - Supported export parameters
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "dbserver", "True", "Hostname or IP of the database server"
    "database", "True", "database name"
    "username", "True", "username for database connection"
    "password", "True", "password for database connection"


The following export variables can be defined:

.. csv-table:: Table 10: ExternalSystemMySQLDB - Supported export variables
    :header: "Name", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "table\_<name>", "True", "adding CMDB data to database table with name <name>. As value, comma seperated field values (in SQL INSERT syntax) should be defined"


The exporter can synchronize objects to one or multiple database tables. Please see an example of the export variable syntax below::

    #variable name: table_users
    #variable value: "{{id}}", "{{fields['username']}}", NULL, NULL

    #variable name: table_groups
    #variable value: "{{id}}", "{{fields['username']}}"



ExternalSystemOpenNMS
---------------------
This class will create/update/delete nodes in the monitoring system OpenNMS. DATAGERRY objects were exported to one
OpenNMS provisioning requisition using the OpenNMS REST API. Foreach exported object, ip, hostname, asset informations
and surveillance categories can be set. Optionallly an export of SNMP communities (at the moment SNMPv1 and SNMPv2c are
supported) can be done.


The exporter class has the following parameters:

.. csv-table:: Table 11: ExternalSystemOpenNMS - Supported export parameters
    :header: "Parameter", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "resturl", "True", "OpenNMS REST URL"
    "restuser", "True", "OpenNMS REST user"
    "restpassword", "True", "OpenNMS REST password"
    "requisition", "True", "OpenNMS requisition to use"
    "services", "False", "name of services to bind on each node sepetated by space"
    "exportSnmpConfig", "False", "also export SNMP configuration for nodes"
    "exportSnmpConfigRetries", "False", "export SNMP configuration for nodes: set SNMP retries"
    "exportSnmpConfigTimeout", "False", "export SNMP configuration for nodes: set SNMP timeout"


The following export variables can be defined:

.. csv-table:: Table 12: ExternalSystemOpenNMS - Supported export variables
    :header: "Name", "Required", "Description"
    :width: 100%
    :widths: 30 20 50
    :align: left

    "nodelabel", "True", "nodelabel for the OpenNMS node"
    "ip", "True", "ip address to add in OpenNMS"
    "furtherIps", "True", "further ip addresses to add to OpenNMS node. Format: IP1;IP2;IP3."
    "asset\_", "True", "content for asset field e.g. - asset\_city for adding information to the city field"
    "category\_", "True", "use variable value of the field to define a category e.g. - category\_1"
    "snmp\_community", "True", "SNMP community of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true."
    "snmp\_version", "True", "SNMP version of a node. This will be set in OpenNMS, if exportSnmpConfig is set to true. Currently the exporter supports only v1/v2c"

