# dataGerry - OpenSource Enterprise CMDB
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
BIN_PYINSTALLER = /usr/bin/pyinstaller
BIN_SPHINX = /usr/bin/sphinx-build
BIN_PYTEST = /usr/bin/pytest
BIN_PIP = /usr/bin/pip
DIR_BUILD = ./target
DIR_BIN_BUILD = ${DIR_BUILD}/bin
DIR_TEMP= ${DIR_BUILD}/temp
DIR_DOCS_SOURCE = docs/source
DIR_DOCS_BUILD = ${DIR_BUILD}/docs
DIR_DOCS_TARGET = cmdb/interface/net_app/docs

# set default goal
.DEFAULT_GOAL := bin


# install Python requirements
.PHONY: requirements
requirements:
	${BIN_PIP} install -r requirements.txt


# create documentation
.PHONY: docs
docs: requirements
	${BIN_SPHINX} -b html -a ${DIR_DOCS_SOURCE} ${DIR_DOCS_BUILD}
	cp -R ${DIR_DOCS_BUILD}/* ${DIR_DOCS_TARGET}


# create onefile binary of dataGerry
.PHONY: bin
bin: requirements docs
	${BIN_PYINSTALLER} --name datagerry --onefile \
		--distpath ${DIR_BIN_BUILD} \
		--workpath ${DIR_TEMP} \
		--hidden-import cmdb.exportd \
		--hidden-import cmdb.exportd.service \
		--hidden-import cmdb.interface.gunicorn \
		--hidden-import gunicorn.glogging \
		--hidden-import gunicorn.workers.sync \
		--add-data cmdb/interface/net_app/docs:cmdb/interface/net_app/docs \
		--add-data cmdb/interface/net_app/dataGerryApp:cmdb/interface/net_app/dataGerryApp \
		cmdb/__main__.py


# execute tests
.PHONY: tests
tests: requirements
	${BIN_PYTEST} tests


# clean environment
.PHONY: clean
clean:
	rm -Rf ${DIR_BUILD}
	rm -Rf ${DIR_DOCS_TARGET}/*
	rm datagerry.spec
