Logging
=======
Logging is done by the Python logging module. Each process of the application (e.g. webapp, exportd, ...) 
initializes the logging with a configuration. This configuration is defined in the cmdb.utils.logger
module.

By default, each process will write the logs to one file as it is not safe, to write to a single
logfile from multiple processes.

To add logs within the application, use the following code snippet::

    import logging
    logger = logging.getLogger(__name__)
    logger.error("error message")


To get a logger, use the logging.getLogger() function with the name of the current module as
parameter. In the logging configuration, the output for the specific module or for parent packages
can be defined.


Log Levels
----------
The loglevel is configured in cmdb/__init__.py with the variable __MODE__. It can be overwritten by
startup parameters. For the main process (handling the startup), *INFO* is the minimum loglevel. All
other processes uses the defined loglevel in __MODE__.


Log Output
----------
At the moment, there is a console output and an output to logfiles (one logfile per process). The
files were placed in the *logs* directory and were rotated after 10MB of log content. 4 backup files
are stored for each logfile.


Changing the Log Configuration
------------------------------
The log configuration is done in the module cmdb.utils.logger. Change this module to change the log
configuration.

