# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
List of useful functions for the database
"""
import re
import logging
import calendar
import datetime
from datetime import datetime
from bson.dbref import DBRef
from bson.max_key import MaxKey
from bson.min_key import MinKey
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from bson.tz_util import utc

try:
    import uuid

    USE_UUID = True
except ImportError:
    USE_UUID = False
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

_RE_TYPE = type(re.compile("foo"))

ASCENDING = 1
DESCENDING = -1

# -------------------------------------------------------------------------------------------------------------------- #

def object_hook(dct: dict):
    """Helper function for converting json to mongo bson
    Args:
        dct: json data

    Returns:
        bson json format
    """
    if "$oid" in dct:
        return ObjectId(str(dct["$oid"]))

    if "$ref" in dct:
        return DBRef(dct["$ref"], dct["$id"], dct.get("$db", None))

    if "$date" in dct:
        try:
            # if timestamp
            return datetime.fromtimestamp(float(dct["$date"]) / 1000.0, utc)
        except ValueError:
            return datetime.fromisoformat(dct['$date'][:-1]).astimezone(utc)

    if "$regex" in dct:
        flags = 0
        if "i" in dct["$options"]:
            flags |= re.IGNORECASE
        if "m" in dct["$options"]:
            flags |= re.MULTILINE
        return re.compile(dct["$regex"], flags)

    if "$minKey" in dct:
        return MinKey()

    if "$maxKey" in dct:
        return MaxKey()

    if USE_UUID and "$uuid" in dct:
        return uuid.UUID(dct["$uuid"])
    return dct


def default(obj):
    """Helper function for converting bson to json
    Args:
        obj: bson data

    Returns:
        json format
    """
    from cmdb.framework.cmdb_render import RenderResult

    from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
    if isinstance(obj, CmdbDAO):
        return obj.__dict__

    if isinstance(obj, RenderResult):
        return obj.__dict__

    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}

    if isinstance(obj, DBRef):
        return obj.as_doc()

    if isinstance(obj, datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(calendar.timegm(obj.timetuple()) * 1000 +
                     obj.microsecond / 1000)
        return {"$date": millis}

    if isinstance(obj, _RE_TYPE):
        flags = ""
        if obj.flags & re.IGNORECASE:
            flags += "i"
        if obj.flags & re.MULTILINE:
            flags += "m"
        return {
            "$regex": obj.pattern,
            "$options": flags
        }

    if isinstance(obj, MinKey):
        return {"$minKey": 1}

    if isinstance(obj, MaxKey):
        return {"$maxKey": 1}

    if isinstance(obj, dict):
        return obj

    if isinstance(obj, Timestamp):
        return {"t": obj.time, "i": obj.inc}

    if USE_UUID and isinstance(obj, uuid.UUID):
        return {"$uuid": obj.hex}

    raise TypeError(f"{obj} is not JSON serializable")
