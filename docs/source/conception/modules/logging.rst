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
