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
ExportJob can be triggered manually by clicking "Run Now" on the Export Job List. It is also possible to run the job
event based (this must be enabled in the configuration). That means, the job is triggered, if one of the sources'
objects has changed or a new object was added.


ExternalSystems
===============

Currently the follwowing ExternalSystems are supported:

.. note::
    You can add your own ExternalSystems with a plugin system, that will be available soon.


.. csv-table:: 
    :header: "ExternalSystem", "description"
    :align: left

    "ExternalSystemOpenNMS", "Add nodes to the monitoring system OpenNMS with the OpenNMS REST API"
    "ExternalSystemDummy", "A dummy for testing Exportd - will only print some debug output"

