##########
Interfaces
##########

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

Routes
******
The url structure of the software is subdivided by several routes.
These have their own prefix and can contain subroutes. Each route is subdivided into its area of application.

Static Routes
=============
+-----------+-----------------------------+-------------+-----------+------------+----------------+
| URL       | Route                       | Description | Arguments | Parameters | Required Right |
+===========+=============================+=============+===========+============+================+
| /licence/ | static_pages.licence_page   |             | -         | -          | -              |
+-----------+-----------------------------+-------------+-----------+------------+----------------+
| /contact/ | static_pages.contact_page   |             | -         | -          | -              |
+-----------+-----------------------------+-------------+-----------+------------+----------------+
| /faq/     | static_pages.faq_page       |             | -         | -          | -              |
+-----------+-----------------------------+-------------+-----------+------------+----------------+

Authentication Routes
=====================
+-------------------+--------------------------------------+-------------+---------------------------+------------+----------------+
| URL               | Route                                | Description | Arguments                 | Parameters | Required Right |
+===================+======================================+=============+===========================+============+================+
| /login/           | auth_pages.login_page                | -           | username, password        | -          | -              |
+-------------------+--------------------------------------+-------------+---------------------------+------------+----------------+
| /logout/          | auth_pages.logout_page               | -           | -                         | -          | -              |
+-------------------+--------------------------------------+-------------+---------------------------+------------+----------------+
| /register/        | static_pages.register_page           | -           | username, password, email | -          | -              |
+-------------------+--------------------------------------+-------------+---------------------------+------------+----------------+
| /forgot-password/ | static_pages.forgot_password_page    | -           | username                  | -          | -              |
+-------------------+--------------------------------------+-------------+---------------------------+------------+----------------+

Object Routes
=============
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| URL                              | Route                               | Description | Arguments  | Parameters  | Required Right               |
+==================================+=====================================+=============+============+=============+==============================+
| /object/                         | object_pages.list_page              |             |            | limit, sort | base.framework.*             |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| /object/newest/                  | object_pages.newest_objects_page    |             |            | limit       | base.framework.object.view   |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| /object/latest/                  | object_pages.latest_objects_page    |             |            | limit       | base.framework.object.view   |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| /object/[int:public_id]/         | object_pages.view_page              |             | public_id  |             | base.framework.object.view   |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| /object/[int:public_id]/edit/    | object_pages.edit_page              |             | public_id  |             | base.framework.object.edit   |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+
| /object/[int:public_id]/delete/  | object_pages.delete_page            |             | public_id  |             | base.framework.object.delete |
+----------------------------------+-------------------------------------+-------------+------------+-------------+------------------------------+

