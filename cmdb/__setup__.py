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

import logging

LOGGER = logging.getLogger(__name__)


def initial_setup_routine():
    # check if settings are loaded
    from cmdb.utils.system_reader import SystemConfigReader
    system_config_reader_status = SystemConfigReader().status()
    if system_config_reader_status is not True:
        raise RuntimeError(
            f'The system configuration files were loaded incorrectly or nothing has been loaded at all. - \
            system config reader status: {system_config_reader_status}')

    # connect to database
    pass
    # check if database already initialized
    pass
    # generate collections
    pass
    # set unique indexes
    pass
    # generate key
    pass
