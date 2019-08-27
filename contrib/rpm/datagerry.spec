Name:       DATAGERRY
Version:	1.0.0
Release:	1%{?dist}
Summary:	DATAGERRY is an enterprise-grade OpenSource CMDB, which completely leaves the definition of object types to the user.

Group:		Applications/Databases
License:	AGPLv3
URL:		https://www.datagerry.org
Vendor:     NETHINKS GmbH
Source0:	https://github.com/NETHINKS/DATAGERRY

%description
A CMDB is a database which includes all informations about objects 
(i.e. servers, routers, locations, maintenance contracts), that are 
required for operating an IT infrastructure. Also the relationships 
between objects are stored (i.e. server a is placed on location b). 
Available solutions tend to be shipped with predefined object types, 
that often can only be customized with big efforts.

DATAGERRY is an enterprise-grade OpenSource CMDB, where object types
can be completely defined by the user and can be adapted at runtime. 
The stored data can be used in different ways, i.e. for automated 
export to external systems, an intelligent search within the data, 
or a reporting. All functions are implemented with the generic and 
the custom definition of object types in mind. With a plugin system, 
DATAGERRY can be extended easily - also by experienced users.


%pre
/usr/bin/getent group datagerry || /usr/sbin/groupadd -r datagerry
/usr/bin/getent passwd datagerry || /usr/sbin/useradd -r -d /home/datagerry -s /sbin/nologin -g datagerry datagerry


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/datagerry
install %{_sourcedir}/datagerry %{buildroot}%{_bindir}/datagerry
install %{_sourcedir}/datagerry.service %{buildroot}%{_unitdir}/datagerry.service
install -D %{_sourcedir}/cmdb.conf %{buildroot}%{_sysconfdir}/datagerry/cmdb.conf


%files
%{_bindir}/datagerry
%{_unitdir}/datagerry.service
%{_sysconfdir}/datagerry/cmdb.conf
