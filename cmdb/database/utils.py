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
import uuid
import logging
import calendar
import datetime
from bson.dbref import DBRef
from bson.max_key import MaxKey
from bson.min_key import MinKey
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from bson.tz_util import utc

from cmdb.framework.rendering.render_result import RenderResult
from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
from cmdb.media_library.media_file_base import MediaFileManagementBase
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.settings.date.date_settings import DateSettingsDAO
from cmdb.search.search_result import SearchResult, SearchResultMap
from cmdb.docapi.docapi_template.docapi_template_base import TemplateManagementBase
from cmdb.user_management.models.right import BaseRight
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

RE_TYPE = type(re.compile("re.Pattern"))

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
            return datetime.datetime.fromtimestamp(float(dct["$date"]) / 1000.0, utc)
        except ValueError:
            return datetime.datetime.fromisoformat(dct['$date'][:-1]).astimezone(utc)

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

    if "$uuid" in dct:
        return uuid.UUID(dct["$uuid"])

    return dct

#pylint: disable=too-many-return-statements
def default(obj):
    """Helper function for converting bson to json
    Args:
        obj: bson data

    Returns:
        json format
    """
    if isinstance(obj, (CmdbDAO,
                        RenderResult,
                        TemplateManagementBase,
                        AuthSettingsDAO,
                        MediaFileManagementBase,
                        AuthProviderConfig,
                        BaseRight,
                        DateSettingsDAO)):
        return obj.__dict__

    if isinstance(obj, (SearchResult,SearchResultMap)):
        return obj.to_json()

    if isinstance(obj, bytes):
        return obj.decode("utf-8")

    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}

    if isinstance(obj, DBRef):
        return obj.as_doc()

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()

        millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
        return {"$date": millis}

    if isinstance(obj, RE_TYPE):
        flags = ""
        if obj.flags & re.IGNORECASE:
            flags += "i"
        if obj.flags & re.MULTILINE:
            flags += "m"
        return {"$regex": obj.pattern, "$options": flags}

    if isinstance(obj, MinKey):
        return {"$minKey": 1}

    if isinstance(obj, MaxKey):
        return {"$maxKey": 1}

    if isinstance(obj, dict):
        return obj

    if isinstance(obj, Timestamp):
        return {"t": obj.time, "i": obj.inc}

    if isinstance(obj, uuid.UUID):
        return {"$uuid": obj.hex}

    try:
        return obj.__dict__
    except Exception as err:
        raise TypeError(f"{obj} not JSON serializable - Type: {type(obj)}. Error: {err}") from err
