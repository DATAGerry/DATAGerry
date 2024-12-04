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
 * MongoDB 6.0 (MongoDB 4.4+ should stille be compatible)
 * RabbitMQ (except the deb-packages)

Although DATAGERRY includes its own web server, we recommend using Nginx as a reverse proxy to enhance performance.

Below, you will find detailed descriptions of several setup options for DATAGERRY:

 * **Docker Image** (Simplified deployment using containerization)
 * **RPM File** (for RHEL/CentOS distributions)
 * **tar.gz Archive with Setup Script** (Compatible with Debian/Ubuntu and other distributions, providing flexibility in setup)
 * **Deb Package** (Specifically designed for Debian systems, ensuring smooth installation)

For a quick and easy setup, use our Docker Image along with the docker-compose file.

| 

=======================================================================================================================

| 

Configuration
=============

Most of DATAGERRY's configuration is stored in MongoDB. However, a few parameters, such as
the database connection to MongoDB itself, cannot be stored there. For these parameters,
we provide an INI-style configuration file called cmdb.conf. Please see the following example:

.. include:: ../../../etc/cmdb.conf
    :literal:

It is possible to overwride settings in the configuration file with OS environment variables.
Please see the following example:

.. code-block:: bash

   DATAGERRY_<section_name>_<option_name>
   DATAGERRY_Database_port=27018

This feature is especially useful, if you want to run DATAGERRY in Docker.


| 

=======================================================================================================================

| 

Setup via Docker Image
======================
The quickest way to get started with DATAGERRY is by using Docker. We provide a docker-compose file
that creates four containers: DATAGERRY, MongoDB, RabbitMQ, and Nginx. All data is stored in MongoDB
using Docker volumes on the host system.

To begin, copy the following docker-compose.yml file into a directory on your Docker host.

.. include:: ../../../contrib/docker/compose/ssl/docker-compose.yml
    :literal:

Create a subdirectory called *cert* with an SSL certificate (called cert.pem) and key (called key.pem). Your directory
structure should look like this:

.. code-block:: console

    ./docker-compose.yml
    ./cert/cert.pem
    ./cert/key.pem


If you don't need SSL and just want to have a quick start, use the follwing docker-compose.yml file:

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

For Red Hat Enterprise Linux (RHEL) and RHEL-based systems such as CentOS or Oracle Linux,
we offer an RPM file for installing DATAGERRY.

Link to RPM Package: `BuildKite <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-rpm>`_

The following RHEL/CentOS versions are supported and tested:

 * **RHEL/CentOS 9**

Before installing DATAGERRY, ensure you have installed the necessary dependencies MongoDB and RabbitMQ.

=======================================================================================================================

Setup MongoDB
-------------

DATAGERRY requires MongoDB version 6 as its database (4.4+ should still be compatible).

.. note::
    Detailed instructions for setting up MongoDB 6.0 can be found on the
    `MongoDB Website <https://www.mongodb.com/docs/v6.0/tutorial/install-mongodb-on-red-hat/>`_


=======================================================================================================================

Setup RabbitMQ
--------------

RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

.. note::
    The setup of RabbitMQ is described in detail on the `RabbitMQ Website <https://www.rabbitmq.com/install-rpm.html>`_
    The following section is a quick install guide of RabbitMQ

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

    http://<host>:4000
    user: admin
    password: admin


.. note::
    If you can't access the webfrontend of DATAGERRY, check the firewall settings of your server. Port 4000 should ba
    accessible.

| 

=======================================================================================================================

| 

Setup via tar.gz/zip archive
============================
For all non rpm based Linux distributions, we provide a tar.gz archive with a setup shell script. Systemd is a
requirement for that setup. This should work on most distributions, and is tested with the following distributions:

 * Ubuntu 20.04
 * Ubuntu 22.04


Before installing DATAGERRY, ensure you have installed the necessary dependencies MongoDB and RabbitMQ.

=======================================================================================================================

Setup MongoDB
-------------
MongoDB 6.0 (4.4+ should still be compatible) is required as database for DATAGERRY.

Please follow the offical `MongoDB documentation <https://www.mongodb.com/docs/v6.0/administration/install-on-linux/>`_
to setup MongoDB for your distribution.

=======================================================================================================================

Setup RabbitMQ
--------------
RabbitMQ 3.8+ is used as messaging bus between the processes of DATAGERRY.

Please follow the offical `RabbitMQ documentation <https://www.rabbitmq.com/docs/install-debian>`_ to
setup RabbitMQ for your distribution.

=======================================================================================================================

Setup DATAGERRY
---------------
Link to zip Package: `BuildKite <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-zip>`_

Extract the provided zip archive and execute the setup script as root:

.. code-block:: console

    $ unzip datagerry-<version>.zip
    $ cd datagerry
    $ sudo ./setup.sh

**OR**

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

    http://<host>:4000
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

Link to deb Package: `BuildKite <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-deb>`_

.. code-block:: console

    apt install ./<deb-package-filename>


To access the DATAGERRY frontend, use the following parameters:

.. code-block:: console

    http://<host>:4000
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

This will set Nginx to listen on port 80 (HTTP) and 443 (HTTPS) and create a redirect from HTTP to HTTPS. If someone access 
*https://<host>/*, Nginx will contact *http://127.0.0.1:4000*, where DATAGERRY is listening.

| 

=======================================================================================================================

| 

Updating DATAGERRY
==================
To update DATAGERRY to a new version, simply install the new version and start DATAGERRY. During the initial startup,
DATAGERRY will detect the version of the existing database and apply any necessary updates. This process may take a
few seconds or minutes. Once complete, the application will start automatically. 
