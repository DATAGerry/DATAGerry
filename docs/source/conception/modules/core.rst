Core
====
The object system should represent the actual main function of the software system. In addition to the core system,
which releases the collected data for use, the object system is responsible for collecting, storing, managing,
updating, analyzing and presenting the data input. It is divided into: Objects, Types, Categories, Collections
and Statuses

Objects
-------
Objects are the data representation or represent instances of the types. They hold the final information.
They consist of various meta data and field data, which are dependent on their corresponding types.
The field values are not necessarily dependent on the predefined definitions within the types.
However, they cannot be used without the respective assignments within the CMDB.

Object Linking
^^^^^^^^^^^^^^
Objects should be linked to each other to form chains of any length.
This should enable relationships between different objects.

Object referencing
^^^^^^^^^^^^^^^^^^
Within the objects, other object instances can be used as field values.

Object Logs
^^^^^^^^^^^
When data is changed within an object, the last state of the object is to be saved.
These are provided with the respective action, the user who made the changes and an optional comment.
This makes it possible to retrieve any former state of the object.

Types
-----
