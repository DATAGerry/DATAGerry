FROM centos:8
LABEL maintainer="adnan.smajic@becon.de"

# set locale
ARG build_locale=en_US

# install DATAGERRY
COPY files/DATAGERRY-*.rpm /tmp
RUN rpm -ivh /tmp/DATAGERRY-*.rpm \
    && yum -y install glibc-locale-source glibc-langpack-en \
    && localedef -c -i ${build_locale} -f UTF-8 ${build_locale}.utf-8

# set locale
ENV LANG ${build_locale}.utf8

# start DATAGERRY
CMD ["/usr/bin/datagerry", "-c", "/etc/datagerry/cmdb.conf", "-s"]
