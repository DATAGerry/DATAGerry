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

"""
Different wrapper functions for interface module
"""
import logging
from functools import wraps

from flask import request, abort

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def deprecated(f):
    @wraps(f)
    def _deprecated(*args, **kwargs):
        LOGGER.debug(f'{f} is likely to be deprecated soon!')
        return f(*args, **kwargs)

    return _deprecated


def json_required(f):
    @wraps(f)
    def _json_required(*args, **kwargs):
        if not request or not request.json:
            LOGGER.warning("Not json | {}".format(request))
            return abort(400)
        return f(*args, **kwargs)

    return _json_required


def timing(msg=None):
    """
    Time wrap function - Measures time of function duration
    Args:
        msg: output message

    Returns:
        wrap function
    """

    def _timing(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            import logging
            import time
            time1 = time.time()
            ret = f(*args, **kwargs)
            time2 = time.time()
            logging.getLogger(__name__).debug(f'{msg} took {(time2 - time1) * 1000.0} MS')
            return ret

        return wrap

    return _timing
