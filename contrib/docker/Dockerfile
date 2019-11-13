FROM centos:8
LABEL maintainer="monitoring@nethinks.com"

# install DATAGERRY
COPY files/DATAGERRY-*.rpm /tmp
RUN rpm -ivh /tmp/DATAGERRY-*.rpm

# start DATAGERRY
CMD ["/usr/bin/datagerry", "-c", "/etc/datagerry/cmdb.conf", "--setup", "-s"]
