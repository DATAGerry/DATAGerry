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


import logging
import pkgutil
import inspect

from . import versions
from cmdb.utils.helpers import process_bar

LOGGER = logging.getLogger(__name__)


class UpdateSettings:
    """Update data object"""

    __DOCUMENT_IDENTIFIER = 'updater'

    def __init__(self, version: int, *args, **kwargs):
        self._id: str = UpdateSettings.__DOCUMENT_IDENTIFIER
        self.version = version

    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id

    def get_version(self) -> int:
        """Get the current version"""
        return self.version

    def run_updates(self, version):
        package = versions
        files = []
        for finder, modname, ispkg in pkgutil.iter_modules(package.__path__):
            files.append({'finder': finder, 'modname': modname, 'version': modname.replace('updater_', '')})

        for num, file in enumerate(sorted(files)):
            current_version = int(file['version'])
            if current_version > version:
                process_bar('Process', len(files), num + 1)
                module = file['finder'].find_module(file['modname']).load_module(file['modname'])
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and name in 'Update%s' % current_version:
                       obj().start_update()
