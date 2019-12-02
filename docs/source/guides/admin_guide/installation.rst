###########################
Install guide for DATAGERRY
###########################
* Installing on Debian 
* Installing on RHEL
|

Installing on Debian
********************
Instructions for installing DATAGERRY one a Debian system

- **1. Installing the dependencies**
    - **1.1. MongoDB**
        - **1.1.1 Installing MongoDB**
            | sudo apt install -y MongoDB
        - **1.1.2 Enable MongoDB on startup**
            | systemctl enable MongoDB
        - **1.1.3 Start MongoDB**
            | systemctl start MongoDB
        - **1.1.4 Check the status of MongoDB**
            | systemctl status MongoDB
    - **1.2 RabbitMQ and Dependencies**
        - **1.2.1 Installing Erlang**
            | Erlang is a programming language that is required for the installation of RabbitMQ
            | wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
            | sudo dpkg -I erlang-solutions_1.0_all.deb
            | sudo apt-get update
            | sudo apt-get install erlang
        - **1.2.2 Installing RabbitMQ**
            | Enable RabbitMQ repository:
            | echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
            | wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add –
            
            | Update Cache an install RabbitMQ:
            | sudo apt-get update
            | sudo apt-get install -y rabbitmq-server

            | systemctl enable rabbitmq-server
            | systemctl start rabbitmq-server
            | systemctl status rabbitmq-server

- **2. Installing DATAGERRY**
    | Actually there is only the binary file for Debian systems available at the momement.
    | We recommend to create a directory under /opt and move the datagerry files in this directory.

    - **2.1 Create a directory and download the DATAGERRY binary**
        cd /opt
        mkdir cmdb (just an example and you can name the directory like you want)
        wget http://files.datagerry.com/master/bin/

    - **2.2 Make datagerry binary executable**
        chmod +x datagerry

    - **2.3 Create the configuration file**
        vi cmdb.conf

        | [Database]
        | host = 127.0.0.1 
        | port = 27017    
        | database_name = cmdb
        | ;username = username
        | ;password = password

        | [WebServer]
        | host = 0.0.0.0 
        | port = 4000 
        | [Token]
        | expire = 1440

        | [MessageQueueing]
        | host = 127.0.0.1
        | port = 5672
        | username = guest
        | password = guest
        | exchange = datagerry.eventbus
        | connection_attempts = 2
        | retry_delay = 6
        | use_tls = False
    - **2.4 Set the firewall rules**
        ufw allow 4000
    - **2.5 DATAGERRY commands**
        Initialize the database:
        | PATH_TO_DATAGERRY/datagerry --setup -c /PATH/TO/cmdb.conf
        | Create Admin user:
        | PATH_TO_DATAGERRY /datagerry --keys -c /PATH/TO/cmdb.conf
        | Start DATAGERRY:
        | PATH_TO_DATAGERRY /datagerry -s -c /PATH/TO/cmdb.conf
    - **2.6 Create a systemd.service for autostart**
        vi /usr/lib/systemd/system/datagerry.service

        | [Unit]
        | Description=DATAGERRY - Enterprise grade OpenSource CMDB
        | Wants=rabbitmq-server.service mongod.service
        | Requires=network.target
        | After=rabbitmq-server.service mongod.service network.target

        | [Service]
        | User=datagerry
        | Group=datagerry
        | Type=simple
        | ExecStart=/opt/cmdb/datagerry -c /opt/cmdb/cmdb.conf -s
        | KillMode=process
        | Restart=on-failure

        | [Install]
        | WantedBy=multi-user.target
        | Alias=datagerry.service

        | systemctl enable datagerry.service
        | systemctl start datagerry.service
        | systemctl status datagerry.service
|

Installing on RHEL
******************
***************************
Install guide for DATAGERRY
***************************
.. contents:: Table of Contents
    :local:

Installing on Debian
====================
Instructions for installing DATAGERRY one a Debian system

Installing the dependencies
---------------------------
MongoDB
^^^^^^^

Installing MongoDB
""""""""""""""""""
sudo apt install -y MongoDB

Enable MongoDB on startup
"""""""""""""""""""""""""
systemctl enable MongoDB
Start MongoDB
"""""""""""""
systemctl start MongoDB
Check the status of MongoDB
"""""""""""""""""""""""""""
systemctl status MongoDB


RabbitMQ and Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^
Installing Erlang
"""""""""""""""""
| Erlang is a programming language that is required for the installation of RabbitMQ
| wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
| sudo dpkg -I erlang-solutions_1.0_all.deb
| sudo apt-get update
| sudo apt-get install erlang

Installing RabbitMQ
"""""""""""""""""""
Enable RabbitMQ repository:

| echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
| wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add –

| Update Cache an install RabbitMQ:
| sudo apt-get update
| sudo apt-get install -y rabbitmq-server

| systemctl enable rabbitmq-server
| systemctl start rabbitmq-server
| systemctl status rabbitmq-server



Installing DATAGERRY
--------------------
| Actually there is only the binary file for Debian systems available at the momement.
| We recommend to create a directory under /opt and move the datagerry files in this directory.

Create a directory and download the DATAGERRY binary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| cd /opt
| mkdir cmdb (just an example and you can name the directory like you want)
| wget http://files.datagerry.com/master/bin/

Make datagerry binary executable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
chmod +x datagerry

Create the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vi cmdb.conf

| [Database]
| host = 127.0.0.1 
| port = 27017    
| database_name = cmdb
| ;username = username
| ;password = password

| [WebServer]
| host = 0.0.0.0 
| port = 4000 
| [Token]
| expire = 1440

| [MessageQueueing]
| host = 127.0.0.1
| port = 5672
| username = guest
| password = guest
| exchange = datagerry.eventbus
| connection_attempts = 2
| retry_delay = 6
| use_tls = False

Set the firewall rules
^^^^^^^^^^^^^^^^^^^^^^
ufw allow 4000

DATAGERRY commands
^^^^^^^^^^^^^^^^^^
Initialize the database:
| PATH_TO_DATAGERRY/datagerry --setup -c /PATH/TO/cmdb.conf
| Create Admin user:
| PATH_TO_DATAGERRY /datagerry --keys -c /PATH/TO/cmdb.conf
| Start DATAGERRY:
| PATH_TO_DATAGERRY /datagerry -s -c /PATH/TO/cmdb.conf

Create a systemd.service for autostart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vi /usr/lib/systemd/system/datagerry.service

| [Unit]
| Description=DATAGERRY - Enterprise grade OpenSource CMDB
| Wants=rabbitmq-server.service mongod.service
| Requires=network.target
| After=rabbitmq-server.service mongod.service network.target

| [Service]
| User=datagerry
| Group=datagerry
| Type=simple
| ExecStart=/opt/cmdb/datagerry -c /opt/cmdb/cmdb.conf -s
| KillMode=process
| Restart=on-failure

| [Install]
| WantedBy=multi-user.target
| Alias=datagerry.service

| systemctl enable datagerry.service
| systemctl start datagerry.service
| systemctl status datagerry.service

Installing on RHEL
==================
Instructions for installing DATAGERRY one a RHEL system

Installing the dependencies
---------------------------
MongoDB
^^^^^^^
Installing MongoDB
""""""""""""""""""
| vi /etc/yum.repos.d/mongodb.repo

| [MongoDB]
| name=MongoDB Repository
| baseurl=http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/$basearch/
| gpgcheck=1
| enabled=1
| gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc

| sudo yum install -y mongodb-org

Enable MongoDB on startup
"""""""""""""""""""""""""
systemctl enable MongoDB

Start MongoDB
"""""""""""""
systemctl start MongoDB

Check the status of MongoDB
"""""""""""""""""""""""""""
systemctl status MongoDB

RabbitMQ and Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^
Installing Erlang
"""""""""""""""""
| Erlang is a programming language that is required for the installation of RabbitMQ
| yum install -y erlang

Installing RabbitMQ
"""""""""""""""""""
Import the rpm-key:

| rpm --import https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc

| Enable RabbitMQ repository:
| vi /etc/yum.repos.d/rabbitmq.repo

| [bintray-rabbitmq-server]
| name=bintray-rabbitmq-rpm
| baseurl=https://dl.bintray.com/rabbitmq/rpm/rabbitmq-server/v3.8.x/el/$releasever/
| gpgcheck=0
| repo_gpgcheck=0
| enabled=1  |

| systemctl enable rabbitmq-server
| systemctl start rabbitmq-server
| systemctl status rabbitmq-server
|

Installing DATAGERRY
--------------------
There are two options for RHEL available with a binary file or a rpm-package.

DATAGERRY binary
^^^^^^^^^^^^^^^^
Create a directory and download the DATAGERRY binary
""""""""""""""""""""""""""""""""""""""""""""""""""""
| cd /opt
| mkdir cmdb (just an example and you can name the directory like you want)
wget http://files.datagerry.com/master/bin/

Make datagerry binary executable
""""""""""""""""""""""""""""""""
chmod +x datagerry
    
Create the configuration file
"""""""""""""""""""""""""""""
vi cmdb.conf

| [Database]
| host = 127.0.0.1 
| port = 27017    
| database_name = cmdb
| ;username = username
| ;password = password

| [WebServer]
| host = 0.0.0.0 
| port = 4000 
| [Token]
| expire = 1440

| [MessageQueueing]
| host = 127.0.0.1
| port = 5672
| username = guest
| password = guest
| exchange = datagerry.eventbus
| connection_attempts = 2
| retry_delay = 6
| use_tls = False

Set the firewall rules
""""""""""""""""""""""
| firewall-cmd --permanent --zone=public --add-port=4000/tcp
| firewall-cmd --reload

Deactivate SELinux
""""""""""""""""""
| vi /etc/selinux/config
| Set SELINUX=enforcing to SELINUX=disabled and restart the system

DATAGERRY commands
""""""""""""""""""
| Initialize the database:
| PATH_TO_DATAGERRY/datagerry --setup -c /PATH/TO/cmdb.conf

| Create Admin user:
| PATH_TO_DATAGERRY /datagerry --keys -c /PATH/TO/cmdb.conf

| Start DATAGERRY:
| PATH_TO_DATAGERRY /datagerry -s -c /PATH/TO/cmdb.conf
    
Create a systemd.service for autostart
""""""""""""""""""""""""""""""""""""""
| vi /usr/lib/systemd/system/datagerry.service

| [Unit]
| Description=DATAGERRY - Enterprise grade OpenSource CMDB
| Wants=rabbitmq-server.service mongod.service
| Requires=network.target
| After=rabbitmq-server.service mongod.service network.target

| [Service]
| User=datagerry
| Group=datagerry
| Type=simple
| ExecStart=/opt/cmdb/datagerry -c /opt/cmdb/cmdb.conf -s
| KillMode=process
| Restart=on-failure

| [Install]
| WantedBy=multi-user.target
| Alias=datagerry.service
|
| systemctl enable datagerry.service
| systemctl start datagerry.service
| systemctl status datagerry.service
    
DATAGERRY rpm-package
^^^^^^^^^^^^^^^^^^^^^
Install the rpm
"""""""""""""""
rpm -i DATAGERRY_RPM_PACKAGE.rpm

Set the firewall rules
""""""""""""""""""""""
| firewall-cmd --permanent --zone=public --add-port=4000/tcp
| firewall-cmd --reload

Deactivate SELinux
""""""""""""""""""
| vi /etc/selinux/config
| Set SELINUX=enforcing to SELINUX=disabled and restart the system

DATAGERRY commands
""""""""""""""""""
| Initialize the database:
| PATH_TO_DATAGERRY/datagerry --setup -c /PATH/TO/cmdb.conf

| Create Admin user:
| PATH_TO_DATAGERRY /datagerry --keys -c /PATH/TO/cmdb.conf

| Start DATAGERRY:
| PATH_TO_DATAGERRY /datagerry -s -c /PATH/TO/cmdb.conf
    