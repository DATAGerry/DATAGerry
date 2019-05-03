##########
Conception
##########
All requirements listed refer to version 1.0 unless otherwise specified. The name CMDB
(Configuration Management Database) is used in the following as project name until a name
has been chosen for the software.


Preamble
********
A Configuration Management Database (CMDB) is a database that is used to access and manage Configuration Items.
In IT management, the term Configuration Item (CI) is used to describe all IT resources. The term Configuration is
misleading in that it refers to the inventory and mutual dependencies of the managed objects. Many companies use
different databases next to each other for problem, change, asset and process data. This is where the CMDB concept
comes in. The goal is to combine all information from the above-mentioned databases in one place and to make access
to this data easier and more transparent.

Requirements
************
From the functional extent, all functions implemented in the yourCMDB are to be adopted. The core system should provide
2 basic functions. Under point 1, the object system will provide all relevant operations for the management of the
object instances. This also contains the storage of all application and object specific data and their access. The
provision system which is treated for the manual and automated provision and synchronization of the object data
becomes point 2.

Technical requirements
======================
The data storage is based on the approach of a document-oriented NoSQL database. Implemented here is a connection using
MongoDB. Technically you should however must not be attached to a fixed database engine. The internal connection
manager has to be set to the the respective target engine will be adapted. The software is is developed using Python 3.
Current standard is Python Version 3.7.0 (as of 06.09.2018). Minimum requirement is Python Version 3.4.9. A backward
compatibility of the Python Versions are decided depending on the release. However we strive to achieve the greatest
possible compatibility by means of of our versioning (Semantic Versioning 2.0.0).

Modules
*******
.. toctree::
    modules/core
    modules/logging
    modules/processmanagement
    modules/eventhandling
    modules/interface