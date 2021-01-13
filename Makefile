# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# set environment variables
BUILDVAR_VERSION = undefined
BUILDVAR_VERSION_EXT = undefined
BUILDVAR_DOCKER_TAG = undefined
BIN_PYINSTALLER = pyinstaller
BIN_SPHINX = sphinx-build
BIN_PYTEST = pytest
BIN_PIP = pip
BIN_NPM = npm
BIN_RPMBUILD = rpmbuild
DIR_BUILD = $(CURDIR)/target
DIR_BIN_BUILD = ${DIR_BUILD}/bin
DIR_TEMP= ${DIR_BUILD}/temp
DIR_DOCS_SOURCE = docs/source
DIR_DOCS_BUILD = ${DIR_BUILD}/docs
DIR_DOCS_TARGET = cmdb/interface/docs/static
DIR_RPM_BUILD = ${DIR_BUILD}/rpm
DIR_TARGZ_BUILD = ${DIR_BUILD}/targz
DIR_DOCKER_BUILD = ${DIR_BUILD}/docker
DIR_WEB_SOURCE = app
DIR_WEB_BUILD = app/dist/DATAGERRYApp
DIR_WEB_TARGET = cmdb/interface/net_app/DATAGERRYApp

# set default goal
.DEFAULT_GOAL := all

# build whole application
.PHONY: all
all: bin rpm targz docker


# install Python requirements
.PHONY: requirements
requirements:
	${BIN_PIP} install -r requirements.txt


# substitue BUILD variables
.PHONY: buildvars
buildvars:
	sed -i 's/@@DG_BUILDVAR_VERSION@@/${BUILDVAR_VERSION_EXT}/g' cmdb/__init__.py
	sed -i 's/@@DG_BUILDVAR_VERSION@@/${BUILDVAR_VERSION_EXT}/g' docs/source/conf.py


# create documentation
.PHONY: docs
docs: requirements buildvars
	${BIN_SPHINX} -b html -a ${DIR_DOCS_SOURCE} ${DIR_DOCS_BUILD}
	cp -R ${DIR_DOCS_BUILD}/* ${DIR_DOCS_TARGET}


# create webapp
.PHONY: webapp
webapp:
	${BIN_NPM} install --prefix ${DIR_WEB_SOURCE}
	${BIN_NPM} run prod --prefix ${DIR_WEB_SOURCE}
	cp -R ${DIR_WEB_BUILD}/* ${DIR_WEB_TARGET}


# create onefile binary of DATAGERRY
.PHONY: bin
bin: requirements buildvars docs webapp
	${BIN_PYINSTALLER} --name datagerry --onefile \
		--distpath ${DIR_BIN_BUILD} \
		--workpath ${DIR_TEMP} \
		--hidden-import cmdb.updater.versions.updater_20200214 \
		--hidden-import cmdb.updater.versions.updater_20200226 \
		--hidden-import cmdb.updater.versions.updater_20200408 \
		--hidden-import cmdb.updater.versions.updater_20200512 \
		--hidden-import cmdb.exportd \
		--hidden-import cmdb.exportd.service \
		--hidden-import cmdb.exportd.externals \
		--hidden-import cmdb.exportd.externals.external_systems \
		--hidden-import cmdb.file_export \
		--hidden-import cmdb.file_export.file_exporter \
		--hidden-import cmdb.interface.gunicorn \
		--hidden-import gunicorn.glogging \
		--hidden-import gunicorn.workers.sync \
		--hidden-import reportlab.graphics.barcode.common \
		--hidden-import reportlab.graphics.barcode.code128 \
		--hidden-import reportlab.graphics.barcode.code93 \
		--hidden-import reportlab.graphics.barcode.code39 \
		--hidden-import reportlab.graphics.barcode.usps \
		--hidden-import reportlab.graphics.barcode.usps4s \
		--hidden-import reportlab.graphics.barcode.ecc200datamatrix \
		--add-data cmdb/interface/docs/static:cmdb/interface/docs/static \
		--add-data cmdb/interface/net_app/DATAGERRYApp:cmdb/interface/net_app/DATAGERRYApp \
		cmdb/__main__.py


# create RPM package
.PHONY: rpm
rpm: bin
	mkdir -p ${DIR_RPM_BUILD}
	mkdir -p ${DIR_RPM_BUILD}/SOURCES
	cp ${DIR_BIN_BUILD}/datagerry ${DIR_RPM_BUILD}/SOURCES
	cp contrib/systemd/datagerry.service ${DIR_RPM_BUILD}/SOURCES
	cp etc/cmdb.conf ${DIR_RPM_BUILD}/SOURCES
	cp contrib/tmpfiles.d/datagerry.conf ${DIR_RPM_BUILD}/SOURCES
	cp contrib/rpm/datagerry.spec ${DIR_RPM_BUILD}
	sed -i 's/@@DG_BUILDVAR_VERSION@@/$(subst -,_,${BUILDVAR_VERSION})/g' ${DIR_RPM_BUILD}/datagerry.spec
	${BIN_RPMBUILD} --define '_topdir ${DIR_RPM_BUILD}' -bb ${DIR_RPM_BUILD}/datagerry.spec


# create tar.gz package
.PHONY: targz
targz: bin
	mkdir -p ${DIR_TARGZ_BUILD}
	mkdir -p ${DIR_TARGZ_BUILD}/src/datagerry/
	mkdir -p ${DIR_TARGZ_BUILD}/src/datagerry/files
	cp ${DIR_BIN_BUILD}/datagerry ${DIR_TARGZ_BUILD}/src/datagerry/files
	cp contrib/systemd/datagerry.service ${DIR_TARGZ_BUILD}/src/datagerry/files
	cp contrib/tmpfiles.d/datagerry.conf ${DIR_TARGZ_BUILD}/src/datagerry/files
	cp etc/cmdb.conf ${DIR_TARGZ_BUILD}/src/datagerry/files
	cp LICENSE ${DIR_TARGZ_BUILD}/src/datagerry
	cp contrib/setup/setup.sh ${DIR_TARGZ_BUILD}/src/datagerry
	tar -czvf ${DIR_TARGZ_BUILD}/datagerry-${BUILDVAR_VERSION}.tar.gz -C ${DIR_TARGZ_BUILD}/src datagerry


# create Docker image
.PHONY: docker
docker: rpm
	mkdir -p ${DIR_DOCKER_BUILD}
	mkdir -p ${DIR_DOCKER_BUILD}/src
	mkdir -p ${DIR_DOCKER_BUILD}/src/files
	cp contrib/docker/Dockerfile ${DIR_DOCKER_BUILD}/src
	cp ${DIR_RPM_BUILD}/RPMS/x86_64/DATAGERRY-*.rpm ${DIR_DOCKER_BUILD}/src/files
	docker build -f ${DIR_DOCKER_BUILD}/src/Dockerfile -t nethinks/datagerry:${BUILDVAR_DOCKER_TAG} ${DIR_DOCKER_BUILD}/src


# execute tests
.PHONY: tests
tests: requirements
	${BIN_PYTEST} tests


# clean environment
.PHONY: clean
clean:
	rm -Rf ${DIR_BUILD}
	rm -Rf ${DIR_DOCS_TARGET}/*
	rm -Rf ${DIR_WEB_TARGET}/*
	rm -f datagerry.spec
