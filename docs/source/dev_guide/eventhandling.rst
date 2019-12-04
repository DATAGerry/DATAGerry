Event Handling
==============
DATAGERRY uses an event based communication between its daemons. Each daemon can publish and 
subscribe events to a message broker. The message broker (currently, RabbitMQ is supported) 
will route events to the different daemons. 

Each daemon will open two AMQP connections to the message broker (one for sending, one for receiving
events). The connection handling will be done by
cmdb.event_management.event_manager.EventManagerAmqp.


structure of an event
---------------------
An event consists of a type and a set of key-value pairs as parameters.

example:
^^^^^^^^

type: 
  cmdb.core.object.added

parameters:
  id: id of the new created object


The set of key-value pairs depends on the event type.


event routing
-------------
Events are routed by type to the daemons. Each daemon can subscribe to a list of event type
definitions. In these definitions, wildcards can be used::

    # subscribe to a specific event type
    cmdb.core.object.added

    # subscribe to all event types starting with a specific string
    cmdb.core.#


list of event types
-------------------
The following event types are defined in DATAGERRY:

cmdb.core.object:
^^^^^^^^^^^^^^^^^^
These events will be created by the core system if CMDB objects will be added/updated/deleted. The
parameter "public_id" which includes the public ID of the specific object will be included.

* cmdb.core.object.added
* cmdb.core.object.updated
* cmdb.core.object.deleted


cmdb.core.objecttype:
^^^^^^^^^^^^^^^^^^^^^
These events will be created by the core system if CMDB object types will be added/updated/deleted. The
parameter "public_id" which includes the public ID of the specific object will be included.

* cmdb.core.objecttype.added
* cmdb.core.objecttype.updated
* cmdb.core.objecttype.deleted
