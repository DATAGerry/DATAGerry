#########
Interface
#########

The interfaces are used for communication with the CMDB functions.
Basically, there are three different defined interfaces. A distinction is made between usage,
configuration and automation. Normal end-user access is via the web interface.
Automated applications can use the REST-API or the Exporter Daemon.
Configurations should be done either via the web interface or the command-line interface.


Web-Interface
*************
The web interface should be accessible via the port specified in the configuration file.
Host setup ``0.0.0.0`` means that the web server is reachable outside of the localhost.
We strongly recommend to run the cmdb application server BEHIND a web server - e.g. apache, nginx, caddy.
Default port is ``4000``.

.. literalinclude:: ../../../etc/cmdb.conf
    :lines: 9-11

Permalink-Structure
===================

=========  =====  ===========
Blueprint  Link   Description
=========  =====  ===========
False      False  False
True       False  False
False      True   False
True       True   True
=========  =====  ===========