**************************
Objects and Object Types
**************************

Managing Categories
===================

Object Types are organized in Categories. Categories can be managed under Framework -> Categories. Each Object Type is
assigned to one Category. Categories can be organized hierarchically, just define a parent Category. The tree of
Categories and their assigned Object Types are displayed on the sidebar on the left side of DATAGERRY.

.. image:: img/objects_categories_sidebar.png
    :width: 100


Managing Object Types
=====================

To manage Object Types select Framework -> Types in the menu bar:

.. image:: img/objects_menu_types.png
    :width: 200

A list with defined object types will be shown.


Adding/Editing an Object Type
-----------------------------
In the Object Type list click on "Add" to add a new type, or click on the "Edit" icon to edit an existing type. A
wizzard will guide you through the process.

At first, some basic information about the type will be asked:

.. image:: img/objects_type_basic.png
    :width: 600

Choose a label and icon for the Object Type, that will be shown in the frontend. The name of the Object Type will be 
created automatically and cannot be changed and is only for internal use. Each Type is connected with a category. With
the exception of name, each setting on this page can be changed at any time.


As a next step, the object fields can be defined:

.. image:: img/objects_type_fields.png
    :width: 600

Fields are organized in "Sections". To add a new section or field, choose an element from the left side box and move it
to the center with drag and drop. At first, add a section (you find it under "Structure Controls"), after that, choose
one or more fields. Each field or section has a name and label. A name will be created automatically and cannot be
changed manually, while a label can be changed at any time. Depending on the field type, several options can be set.
Currently we support the following field types:

.. csv-table::
    :header: "type", "description"
    :align: left

    "Text", "A text field. Content validation with regular expression is possible"
    "Password", "A password field with integrated password generator and hiding of content"
    "Textarea", "Textbox with multiple lines"
    "Checkbox", "A boolean checkbox"
    "Radio", "Selection between multiple options"
    "Select", "Selection between multiple options with a dropdown menu"
    "Date", "A datepicker"
    "Reference", "Reference to another object of a specific type. E.g. connection between a router and a location object"

With the yellow preview button, an example of an object with the current configuration will be shown.


On the next page on the configuration dialog, meta informations can be set:

.. image:: img/objects_type_meta.png
    :width: 600

Each object has summary fields. These fields summarize the object and are shown by default in object lists. On a router,
this could be a management ip and a hostname. The summary fields can be set under "Summary".
Also, external links can be set, which are shown on the object page to add a quick link to the webUI of another system.
An External Link has a name, a label, an icon and the link (URL) itself. In the link, use curved brackets to access
values of an object field.


Changing an existing Object Type
--------------------------------
Existing Object Types can be changed at any time, just edit the Object Type and add or remove fields or other details.
The Object Type definition will be applied to all existing objects, so if you remove a field, it will not be shown in
DATAGERRY anymore. The removed field still exists in the database and if you add the field again, you can access the old
content. To cleanup the database and sync Object Type definition with the database, click on the "Cleanup" button in the
object type list.


Importing/Exporting Object Types
--------------------------------
Object Types can be exported in JSON format. In the Object Types list, click on the yellow "Export" button to get a file
in JSON format. By default, all Object Types will be exported. If you only want to export specific types, select items
in the list and click on the "Export" button.

Object Types can also be imported from a JSON file. In the menu, choose "Type Import/Export" -> "Import Type" and upload
a JSON file with type definitions. During the import, you can choose, which types from the JSON file should be imported.


Managing Objects
================
You can access Objects in DATAGERRY in several ways:

 * using the Category tree on the left side
 * using the search bar at the top

When using the Category tree, you can choose an Object Type (e.g. router) and get a list with all objects of that type.
By default, only summary fields of an object are shown in the table, with the yellow settings button, additional fields
can be faded in.



Active und Inactive Objects
---------------------------
Objects in DATAGERRY can be active or inactive. Inactive Objects are hidden in the WebUI and were not exported to
external systems with Exportd. By default, all new created Objects in DATAGERRY are active. You can set an Object to 
inactive by hitting the small switch on the Object view page.

If you want to see inactive Objects in the WebUI, ckick on the switch under the navigation bar.

.. image:: img/objects_active_switch.png
    :width: 200


Exporting Objects
-----------------
Objects can be exported in several formats. Currently we support:

 * CSV
 * Microsoft Excel (xlsx)
 * JSON
 * XML

To export objects, click on the "Export" button in an Object list and choose the export format. Only Objects of a single
type can be exported (so you won't find the Export button in a list with Objects of multiple types).

An export is also possible in the menu, choose "Object Import/Export" -> "Export Objects".


Importing Objects
-----------------
To import Objects, choose "Objects Import/Export" -> "Import Objects" from the menu. Currently we support the import of
the following file formats:

 * CSV
 * JSON

To start an import, upload a file and choose the file format. Depending on the format, you have to make some settings
before an import can start.

CSV Import
^^^^^^^^^^
During an import from a CSV file, a mapping of rows to object fields must be defined with a drag and drop assistent.
If the CSV file contains a header that matches the name of object fields, the mapping will be predefined in the WebUI.
Also object references can be resolved with "Foreign Keys". For example, router objects with a field "location" should
be imported. There are Location objects in DATAGERRY with a field "name", that contains an unique name of a Location
(e.g. FRA1). The CSV file with router Objects contains the unique location name. If you choose "foreign key:
location:name" in the mapping wizzard, a reference to the correct Location object will be set during the import.


JSON
^^^^
DATAGERRY can import Objects from a JSON file. The JSON format correspond to the format that was created when exporting
Objects.
