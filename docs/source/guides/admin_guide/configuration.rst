#############
Configuration
#############

DATAGERRRY has a small INI style configuration file, called cmdb.conf, which defines some basic configuration options (e.g. database connection,
etc). Please see the following example:

.. include:: ../../../../etc/cmdb.conf

It is possible to overwrite settings in the configuration file with OS environment variables. Please see the following example:

.. code-block:: bash

   DATAGERRY_<section_name>_<option_name>
   DATAGERRY_Database_port=27018
