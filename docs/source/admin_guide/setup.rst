*****
Setup
*****
This page contains a detailed overview on how to install DATAGERRY on different operating systems and plattforms.

| 

=======================================================================================================================

| 

Requirements
============
DATAGERRY has the following system requirements:

 * Linux Operating System
 * MongoDB 4.4+ (MongoDB 6.0 recommended)
 * RabbitMQ (except the deb-packages)

Although, DATAGERRY comes with an own webserver, we recomend Nginx as a reverse proxy for performance reasons.

There are several setup options for DATAGERRY, which are described in the sections below more in detail:

 * Docker Image
 * RPM file (for RHEL/CentOS distributions)
 * tar.gz archive with setup script (for Debian/Ubuntu or other distributions)
 * deb-package (for Debian)

If you want to have a fast and easy start, use our Docker Image and docker-compose file.

| 

=======================================================================================================================

| 

Setup via Docker Image
======================
The fastest way for getting started with DATAGERRY is using Docker. We provide a docker-compose file, which creates
four containers (DATAGERRY, MongoDB, RabbitMQ, Nginx). All data is stored in MongoDB using Docker volumes on the 
Docker host system.

To start, copy the following docker-compose.yml in a directory of your Docker host.

.. include:: ../../../contrib/docker/compose/ssl/docker-compose.yml
    :literal:

Create a subdirectory called *cert* with an SSL certificate (called cert.pem) and key (called key.pem). Your directory
structure should look like this:

.. code-block:: console

    ./docker-compose.yml
    ./cert/cert.pem
    ./cert/key.pem


If you don't need SSL and just want to have a quick start, use the follwing docker-compose.yml:

.. include:: ../../../contrib/docker/compose/nossl/docker-compose.yml
    :literal:

Now, run docker-compose to start the application:

.. code-block:: console

    $ docker-compose up -d

To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<host> or https://<host>
    user: admin
    password: admin


We provide Docker images for every version of DATAGERRY in `Docker Hub <https://hub.docker.com/r/becongmbh/datagerry>`_.
You can use one of the following Docker tags:

latest
    The latest tag is a symlink to the latest stable version of DATAGERRY. It is nice for a quickstart but will also do
    an automatic upgrade to the next major release if one is available. For production, we recommend the <release> tag
    below.

<release> (e.g. 2.0.0)
    Every release has its own tag. So, if you want to use a specific version (or prevent your environment from automatic
    upgrades) just use a specific version as a Docker tag.


To use a specific Docker tag, just replace the following line of the docker-compose.yml:

.. code-block:: console

    # replace this line
    image: becongmbh/datagerry:latest

    # by the following:
    image: becongmbh/datagerry:<tagname>
    # example:
    image: becongmbh/datagerry:2.0.0

| 

=======================================================================================================================

| 

Setup via RPM 
=============

For Red Hat Enterprise Linux (RHEL) or RHEL based systems like CentOS or Oracle Linux, we provide a RPM file for
installing DATAGERRY.

The following RHEL/CentOS versions are supported and tested:

 * RHEL/CentOS 8


Before you can install DATAGERRY, you need to install the required dependencies MongoDB and Rabbit MQ.

=======================================================================================================================

Setup MongoDB
-------------

MongoDB 4.4+ is required as database for DATAGERRY.

.. note::
    The setup of MongoDB is described in detail on the `MongoDB website https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/`
    The following section is a quick install guide of MonogDB.

To setup MongoDB, place the follwing file under /etc/yum.repos.d/mongodb.repo:


.. code-block:: ini

    [MongoDB]
    name=MongoDB Repository
    baseurl=http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.4/$basearch/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc


After that, install the mongodb-org package and start the server with SystemD:

.. code-block:: console

    $ sudo yum install -y mongodb-org
    $ sudo systemctl enable mongod
    $ sudo systemctl start mongod

=======================================================================================================================

Setup RabbitMQ
--------------

RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

.. note::
    The setup of RabbitMQ is described in detail on the RabbitMQ website: https://www.rabbitmq.com/install-rpm.html
    The following section is a quick install guide of RabbitMQ


For setting up RabbitMQ, we can use the RPM repository provided by Bintray. Place the following file under 
/etc/yum.repos.d/rabbitmq.repo:

.. code-block:: ini

    [bintray-rabbitmq-server]
    name=bintray-rabbitmq-rpm
    baseurl=https://dl.bintray.com/rabbitmq/rpm/rabbitmq-server/v3.8.x/el/$releasever/
    gpgcheck=1
    gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
    enabled=1

    [bintraybintray-rabbitmq-erlang-rpm]
    name=bintray-rabbitmq-erlang-rpm
    baseurl=https://dl.bintray.com/rabbitmq-erlang/rpm/erlang/22/el/$releasever/
    gpgcheck=0
    repo_gpgcheck=0
    enabled=1

Now, RabbitMQ can be installed and started:

.. code-block:: console

    $ sudo yum install -y rabbitmq-server
    $ sudo systemctl enable rabbitmq-server
    $ sudo systemctl start rabbitmq-server

=======================================================================================================================

Setup DATAGERRY
---------------

If all requirements were installed, you can install the downloaded DATAGERRY RPM file:

.. code-block:: console

    $ sudo rpm -ivh DATAGERRY-<version>.x86_64.rpm


To change the parameters for connecting to MongoDB and RabbitMQ, edit the configuration file
**/etc/datagerry/cmdb.conf**

After that, activate and start DATAGERRY with Systemd:

.. code-block:: console

    $ sudo systemctl enable datagerry.service
    $ sudo systemctl start datagerry.service


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin


.. note::
    If you can't access the webfrontend of DATAGERRY, check the firewall settings of your server. Port 4000 should ba
    accessible.

| 

=======================================================================================================================

| 

Setup via tar.gz archive
========================
For all non rpm based Linux distributions, we provide a tar.gz archive with a setup shell script. Systemd is a
requirement for that setup. This should work on most distributions, and is tested with the following distributions:

 * Ubuntu 20.04
 * Ubuntu 22.04


Before we can install DATAGERRY, we need to install the required dependencies MongoDB and Rabbit MQ.

=======================================================================================================================

Setup MongoDB
-------------
MongoDB 4.4+ (6.0 recommended) is required as database for DATAGERRY.

Please follow the offical `MongoDB documentation <https://docs.mongodb.com/manual/administration/install-on-linux/>`_
to setup MongoDB for your distribution.

=======================================================================================================================

Setup RabbitMQ
--------------
RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

Please follow the offical `RabbitMQ documentation <https://www.rabbitmq.com/download.html#installation-guides>`_ to
setup RabbitMQ for your distribution.

=======================================================================================================================

Setup DATAGERRY
---------------
Extract the provided tar.gz archive and execute the setup script as root:

.. code-block:: console

    $ tar -xzvf datagerry-<version>.tar.gz
    $ cd datagerry
    $ sudo ./setup.sh

To change the parameters for connecting to MongoDB and RabbitMQ, edit the configuration file
**/etc/datagerry/cmdb.conf**

After that, activate and start DATAGERRY with Systemd:

.. code-block:: console

    $ sudo systemctl enable datagerry.service
    $ sudo systemctl start datagerry.service


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin

.. note::
    If you can't access the webfrontend of DATAGERRY, check the firewall settings of your server. Port 4000 should be
    accessible.

| 

=======================================================================================================================

| 

Setup via deb-package
=====================
The deb-package already contains RabbitMQ and you just need to install MongoDB. Follow the offical instructions from
the `MongoDB-Homepage <https://www.mongodb.com/docs/v6.0/tutorial/install-mongodb-on-debian/>`_.

The next step is to download the deb-package and install it via the following command (execute the command in the
folder where the deb-package is).

.. code-block:: console

    apt install ./<deb-package-filename>


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<<host>:4000
    user: admin
    password: admin

| 

=======================================================================================================================

| 

Setting up Nginx as reverse proxy
=================================
We recomend to run Nginx as reverse proxy for DATAGERRY. After installing Nginx for your platform, you can adapt the 
following example configuration for Nginx (nginx.conf):

.. include:: ../../../contrib/nginx/nginx.conf
    :literal:

This will Nginx listen on port 80 (HTTP) and 443 (HTTPS) and create a redirect from HTTP to HTTPS. If someone access 
*https://<host>/*, Nginx will contact *http://127.0.0.1:4000*, where DATAGERRY is listening.

| 

=======================================================================================================================

| 

Update DATAGERRY
================
To update DATAGERRY to a new version, simply install the new version and start DATAGERRY. During the first start,
DATAGERRY will detect the version of the existing database and apply required updates. This may take a few seconds or
minutes. After that, the application will be started. 
