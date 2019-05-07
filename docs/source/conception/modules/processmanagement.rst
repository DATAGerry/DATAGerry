Process Management
==================
The dataGerry application consists of mulitple services. Each service is a Python process. The 
ProcessManager (cmdb.process_management.process_manager.ProcessManager) will start and stop 
all services in the correct order. 

A services needs to implement the AbstractCmdbService class
(cmdb.process_management.service.AbstractCmdbService). 


adding a new service
--------------------
To add a new service to dataGerry, write your own implementation of AbstractCmdbService and add 
a service definition to ProcessManager. 
