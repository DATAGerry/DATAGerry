*************
Configuration
*************

Most of DATAGERRY's configuration is stored in MongoDB. There are a few parameters which cannot be stored at this place
(e.g. database connection to MongoDB itself). For this parameters, we provide an INI style configuration file, called
cmdb.conf. Please see the following example:

.. include:: ../../../etc/cmdb.conf
    :literal:

It is possible to overwrite settings in the configuration file with OS environment variables. Please see the following example:

.. code-block:: bash

   DATAGERRY_<section_name>_<option_name>
   DATAGERRY_Database_port=27018

This feature is especially useful, if you want to run DATAGERRY in Docker.
