*****
Setup
*****

Requirements
============
DATAGERRY has the following system requirements:

 * Linux Operating System
 * MongoDB 4.2+
 * RabbitMQ

There a several setup options for DATAGERRY, which are described in the sections below in detail:

 * Docker Images
 * RPM file (for RHEL/CentOS distributions)
 * tar.gz archive with setup script (for Debian/Ubuntu or other distributions)


Docker Image
============
The fastest way for getting started with DATAGERRY is using Docker. We provide a docker-compose file, which creates
three containers (DATAGERRY, MongoDB, RabbitMQ). All data were stored in MongoDB using Docker volumes on the Docker host
system.

To start, copy the follwing docker-compose.yml in a directory of your Docker host, and replace "undefined" with the version
of DATAGERRY, you want to use:

.. include:: ../../../contrib/docker/docker-compose.yml
    :literal:

Run docker-compose to start the application:

.. code-block:: console

    $ docker-compose up -d

To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin


RPM setup
=========

For Red Hat Enterprise Linux (RHEL) or RHEL based systems like CentOS or Oracle Linux, we provide a RPM file for
installing DATAGERRY.

The following RHEL/CentOS versions are supported and tested:

 * RHEL/CentOS 7
 * RHEL/CentOS 8


Before we can install DATAGERRY, we need to install the required dependencies MongoDB and Rabbit MQ.

Setup MongoDB
-------------

MongoDB 4.2+ is required as database for DATAGERRY.

.. note::
    The setup of MongoDB is described in detail on the MongoDB website: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/
    The following section is a quick install guide of MonogDB.

To setup MongoDB, place the follwing file under /etc/yum.repos.d/mongodb.repo:


.. code-block:: ini

    [MongoDB]
    name=MongoDB Repository
    baseurl=http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/$basearch/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc


After that, install the mongodb-org package and start the server with SystemD:

.. code-block:: console

    $ sudo yum install -y mongodb-org
    $ systemctl enable MongoDB
    $ systemctl start MongoDB


Setup RabbitMQ
--------------

RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

.. note::
    The setup of RabbitMQ is described in detail on the RabbitMQ website: https://www.rabbitmq.com/install-rpm.html
    The following section is a quick install guide of RabbitMQ

As RabbitMQ requires Erlang, we need to install Erlang first:

.. code-block:: console

    $ yum install -y erlang


For setting up RabbitMQ, we can use the RPM repository provided by Bintray. At first, add the RPM signing key:

.. code-block:: console

    $ rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc


After that, place the following file under /etc/yum.repos.d/rabbitmq.repo:

.. code-block:: ini

    [bintray-rabbitmq-server]
    name=bintray-rabbitmq-rpm
    baseurl=https://dl.bintray.com/rabbitmq/rpm/rabbitmq-server/v3.8.x/el/$releasever/
    gpgcheck=0
    repo_gpgcheck=0
    enabled=1

Now, RabbitMQ can be installed and started:

.. code-block:: console

    $ yum install rabbitmq
    $ systemctl enable rabbitmq-server
    $ systemctl start rabbitmq-server


Setup DATAGERRY
---------------

If all requirements were installed, we'll can install the downloaded DATAGERRY RPM file:

.. code-block:: console

    $ rpm -ivh DATAGERRY-<version>.x86_64.rpm


To change the parameters for connecting to MongoDB and RabbitMQ, edit the configuration file /etc/datagerry/cmdb.conf

Now, the database structure can be created:

.. code-block:: console

    $ datagerry -c /etc/datagerry/cmdb.conf --setup


After that, activate and start DATAGERRY with Systemd:

.. code-block:: console

    $ systemctl enable datagerry.service
    $ systemctl start datagerry.service


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin



tar.gz archive setup
====================
For all non rpm based Linux distributions, we provide a tar.gz archive with a setup shell script. Systemd is a
requirement for that setup. This should work on most distributions, and is tested with the following distributions:

 * Ubuntu 18.04


Before we can install DATAGERRY, we need to install the required dependencies MongoDB and Rabbit MQ.

Setup MongoDB
-------------

MongoDB 4.2+ is required as database for DATAGERRY.

Please follow the offical `MongoDB documentation <https://docs.mongodb.com/manual/administration/install-on-linux/>` to
setup MongoDB for your distribution.


Setup RabbitMQ
--------------

RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

Please follow the offical `RabbitMQ documentation <https://www.rabbitmq.com/download.html#installation-guides>` to
setup RabbitMQ for your distribution.


Setup DATAGERRY
---------------

Extract the provided tar.gz archive and execute the setup script as root:

.. code-block:: console

    $ tar -xzvf datagerry-<version>.tar.gz
    $ cd datagerry
    $ sudo ./setup.sh

To change the parameters for connecting to MongoDB and RabbitMQ, edit the configuration file /etc/datagerry/cmdb.conf

Now, the database structure can be created:

.. code-block:: console

    $ datagerry -c /etc/datagerry/cmdb.conf --setup


After that, activate and start DATAGERRY with Systemd:

.. code-block:: console

    $ systemctl start datagerry.service


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin

