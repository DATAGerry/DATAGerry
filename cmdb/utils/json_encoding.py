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
"""TODO: document"""
import calendar
import datetime
import re

from bson.dbref import DBRef
from bson.max_key import MaxKey
from bson.min_key import MinKey
from bson.objectid import ObjectId
from bson.timestamp import Timestamp

from cmdb.framework.rendering.render_result import RenderResult
from cmdb.importer.importer_response import ImportMessage, BaseImporterResponse
from cmdb.search.search_result import SearchResult, SearchResultMap
from cmdb.security.auth import AuthSettingsDAO, AuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.settings.date.date_settings import DateSettingsDAO

# TODO: try just import and remove handling if not uuid
try:
    import uuid

    USE_UUID = True
except ImportError:
    USE_UUID = False
# -------------------------------------------------------------------------------------------------------------------- #

_RE_TYPE = type(re.compile("foo"))


def default(obj):
    """Helper function for converting cmdb objects to json"""
    from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
    from cmdb.user_management.models.right import BaseRight
    from cmdb.exportd.exportd_job.exportd_job_base import JobManagementBase
    from cmdb.media_library.media_file_base import MediaFileManagementBase
    from cmdb.docapi.docapi_template.docapi_template_base import TemplateManagementBase

    if isinstance(obj, (CmdbDAO,
                        JobManagementBase,
                        MediaFileManagementBase,
                        TemplateManagementBase,
                        BaseRight,
                        RenderResult,
                        BaseImporterResponse,
                        ImportMessage,
                        AuthSettingsDAO,
                        AuthenticationProvider,
                        AuthProviderConfig,
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
        millis = int(calendar.timegm(obj.timetuple()) * 1000 +
                     obj.microsecond / 1000)
        return {"$date": millis}

    if isinstance(obj, _RE_TYPE):
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

    if USE_UUID and isinstance(obj, uuid.UUID):
        return {"$uuid": obj.hex}

    raise TypeError(f"{obj} is not JSON serializable - type: {type(obj)}")
