*****
Setup
*****
.. contents:: Table of Contents
    :local:
|

Installing on Debian
====================
Instructions for installing DATAGERRY on a Debian system

Installing the dependencies
---------------------------
MongoDB
^^^^^^^

| **Installing MongoDB:**
.. code-block:: console

    $ sudo apt install -y MongoDB

| **Enable MongoDB on startup:**
.. code-block:: console

    $ systemctl enable MongoDB

| **Start MongoDB:**
.. code-block:: console

    $ systemctl start MongoDB

| **Check the status of MongoDB:**
.. code-block:: console

    $ systemctl status MongoDB

RabbitMQ and Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^
| **Installing Erlang:**
| Erlang is a programming language that is required for the installation of RabbitMQ
.. code-block:: console

    $ wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
    $ sudo dpkg -I erlang-solutions_1.0_all.deb
    $ sudo apt-get update
    $ sudo apt-get install erlang

| **Installing RabbitMQ:**
| Enable RabbitMQ repository:
.. code-block:: console

    $ echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
    $ wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add –

| Update Cache and install RabbitMQ:
.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install -y rabbitmq-server

| **Enable RabbitMQ on startup:**
.. code-block:: console

    $ systemctl enable rabbitmq-server

| **Start RabbitMQ:**
.. code-block:: console

    $ systemctl start rabbitmq-server

| **Check the status of RabbitMQ:**
.. code-block:: console

    $ systemctl status rabbitmq-server

Installing DATAGERRY
--------------------
| **Create a directory and download the DATAGERRY binary:**
.. code-block:: console

    $ wget http://files.datagerry.com/master/targz/datagerry-master.tar.gz

| **Extract the archive:**
.. code-block:: console

    $ tar -xzvf datagerry-development.tar.gz

| **Execute the setup script:**
.. code-block:: console

    $ cd datagerry
    $ bash setup.sh

| **Set the firewall rules:**
.. code-block:: console

    $ ufw allow 4000

| **Check if DATAGERRY is running:**
.. code-block:: console

    $ systemctl status datagerry.service
|

Installing on RHEL
==================
Instructions for installing DATAGERRY one a RHEL system

Installing the dependencies
---------------------------
MongoDB
^^^^^^^
| **Installing MongoDB:**
| Create a repository file with the following input:
.. code-block:: console

    $ vi /etc/yum.repos.d/mongodb.repo

| [MongoDB]
| name=MongoDB Repository
| baseurl=http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/$basearch/
| gpgcheck=1
| enabled=1
| gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
.. code-block:: console

    $ sudo yum install -y mongodb-org

| **Enable MongoDB on startup:**
.. code-block:: console

    $ systemctl enable MongoDB

| **Start MongoDB:**
.. code-block:: console

    $ systemctl start MongoDB

| **Check the status of MongoDB:**
.. code-block:: console

    $ systemctl status MongoDB

RabbitMQ and Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^
| **Installing Erlang:**
| Erlang is a programming language that is required for the installation of RabbitMQ
.. code-block:: console

    $ yum install -y erlang

| **Installing RabbitMQ:**
| Import the rpm-key:
.. code-block:: console

    $ rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc

| Enable RabbitMQ repository:
.. code-block:: console

    $ vi /etc/yum.repos.d/rabbitmq.repo

| [bintray-rabbitmq-server]
| name=bintray-rabbitmq-rpm
| baseurl=https://dl.bintray.com/rabbitmq/rpm/rabbitmq-server/v3.8.x/el/$releasever/
| gpgcheck=0
| repo_gpgcheck=0
| enabled=1  |

| **Enable RabbitMQ on startup:**
.. code-block:: console

    $ systemctl enable rabbitmq-server

| **Start RabbitMQ:**
.. code-block:: console

    $ systemctl start rabbitmq-server

| **Check the status of RabbitMQ:**
.. code-block:: console

    $ systemctl status rabbitmq-server

Installing DATAGERRY
---------------------
| There are two options for RHEL available with a *.tar.gz archive or a rpm-package.

DATAGERRY from archive
^^^^^^^^^^^^^^^^^^^^^^
| **Create a directory and download the DATAGERRY archive:**
.. code-block:: console

    $ wget http://files.datagerry.com/master/targz/datagerry-master.tar.gz

| **Extract the archive:**
.. code-block:: console

    $ tar -xzvf datagerry-development.tar.gz

| **Execute the setup script:**
.. code-block:: console

    $ cd datagerry
    $ bash setup.sh

| **Set the firewall rules:**
.. code-block:: console

    $ firewall-cmd --permanent --zone=public --add-port=4000/tcp
    $ firewall-cmd --reload

| **Deactivate SELinux:**
.. code-block:: console

    $ vi /etc/selinux/config
| Set SELINUX=enforcing to SELINUX=disabled and restart the system

| **Check if DATAGERRY is running:**
.. code-block:: console

    $ systemctl status datagerry.service

DATAGERRY rpm-package
^^^^^^^^^^^^^^^^^^^^^
| **Install the rpm:**
.. code-block:: console

    $ rpm -ivh DATAGERRY_RPM_PACKAGE.rpm

| **Set the firewall rules:**
.. code-block:: console

    $ firewall-cmd --permanent --zone=public --add-port=4000/tcp
    $ firewall-cmd --reload

| **Deactivate SELinux:**
.. code-block:: console

    $ vi /etc/selinux/config
| Set SELINUX=enforcing to SELINUX=disabled and restart the system

| **Check if DATAGERRY is running:**
.. code-block:: console

    $ systemctl status datagerry.service


Configuration
=============

DATAGERRRY has a small INI style configuration file, called cmdb.conf, which defines some basic configuration options (e.g. database connection,
etc). Please see the following example:

.. include:: ../../../etc/cmdb.conf
    :literal:

It is possible to overwrite settings in the configuration file with OS environment variables. Please see the following example:

.. code-block:: bash

   DATAGERRY_<section_name>_<option_name>
   DATAGERRY_Database_port=27018
