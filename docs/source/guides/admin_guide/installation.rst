############
Installation
############
This guide provides an overview of the installation and startup of DATAGERRY.
The project is developed in the platform-independent programming language Python (Python3) and is available
for different operating systems and architectures. Only the dependencies of the third-party programs
that are required for the CMDB are excluded.

Dependencies
************
Three external programs are required to run DATAGERRY.

1. Python
2. MongoDB
3. RabbitMQ

Python
======
Python is a universal, commonly interpreted higher level programming language.
Its purpose is to improve a readable, concise programming style.
See at the official documentation for details: `Our Documentation | Python.org <https://www.python.org/doc/>`_

**NOTE:** We are using Python 3.6.x or higher, which is not compatible with Python 2.x.

MongoDB
=======
MongoDB is a document-oriented NoSQL database. It is used to store content and the program uses necessary data.
See the official installation guide for details: `Install MongoDB Community Edition <https://docs.mongodb.com/manual/administration/install-community/>`_

RabbitMQ
========
RabbitMQ is an open source message broker software that implements the Advanced Message Queuing Protocol (AMQP).
See the official installation guide for details: `Downloading and Installing RabbitMQ <https://www.rabbitmq.com/download.html#installation-guides>`_

From source
***********
*Step 1:* To install from source files, first clone repository or download the zip release from github

.. code-block:: bash

   git clone https://github.com/NETHINKS/DATAGERRY.git

This should clone the complete repository with the default master branch.

*Step 2:* Install python requirements

.. code-block:: bash

   pip install -r requirements.txt

*Step 3:* Edit the configuration file
Default file is ``etc/cmdb.conf``. But you can change the chosen file with the ``-c`` parameter while starting.
The default configuration should look like this:

.. include:: ../../../../etc/cmdb.conf
    :literal:

With Docker
***********

.. todo:: Implement docker installation

Starting
********

The default start is

.. code-block:: bash

   python -m cmdb/ -s

Optional start parameters:

* ``--setup`` - have to be a unique parameter. Installs database collection and security keys.
* ``--keys`` - have to be a unique parameter. Generate security keys.
* ``-d`` or ``--debug`` - enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS
* ``-s`` or ``--start`` - starting cmdb core system - enables services.
* ``-c`` or ``--config`` - optional path to config file.
