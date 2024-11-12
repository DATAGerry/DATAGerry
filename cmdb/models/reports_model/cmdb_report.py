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
This module contains the implementation of CmdbReport, which is representing
a report in Datagarry
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  CmdbReport - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbReport(CmdbDAO):
    """
    TODO: document

    Attributes:
        COLLECTION (str):    Name of the database collection
        MODEL (Model):              Name of the DAO
        DEFAULT_VERSION (str):      The default "starting" version number
        SCHEMA (dict):              The validation schema for this DAO
        INDEX_KEYS (list):          List of index keys for the database
    """
    COLLECTION = 'framework.reports'
    MODEL = 'Report'
    DEFAULT_VERSION: str = '1.0.0'
    REQUIRED_INIT_KEYS = [
        'report_category_id',
        'name',
        'predefined',
        'type_id',
        'selected_fields',
        'conditions',
        'report_query',
    ]

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'report_category_id': {
            'type': 'integer',
            'required': True,
        },
        'name': {
            'type': 'string',
            'required': True,
        },
        'type_id': {
            'type': 'integer',
            'required': True,
        },
        'selected_fields': {
            'type': 'list',
            'required': True,
        },
        'conditions': {
            'type': 'list',
        },
        'report_query': {
            'type': 'list',
        },
        'predefined': {
            'type': 'boolean',
            'default': False
        },
    }

# ---------------------------------------------------- CONSTRUCTOR --------------------------------------------------- #

    def __init__(
            self,
            report_category_id: int,
            name: str,
            type_id: int,
            selected_fields: list,
            conditions: list,
            report_query: list,
            predefined: bool = False,
            **kwargs):
        """TODO: document"""
        self.report_category_id = report_category_id
        self.name = name
        self.type_id = type_id
        self.selected_fields = selected_fields
        self.conditions = conditions
        self.report_query = report_query
        self.predefined = predefined

        super().__init__(**kwargs)

# --------------------------------------------------- CLASS METHODS -------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbReport":
        """
        Convert data to instance of CmdbReport
        """
        return cls(
            public_id=data.get('public_id'),
            report_category_id=data.get('report_category_id'),
            name=data.get('name'),
            type_id=data.get('type_id'),
            selected_fields=data.get('selected_fields'),
            conditions=data.get('conditions'),
            report_query=data.get('report_query'),
            predefined=data.get('predefined'),
        )


    @classmethod
    def to_json(cls, instance: "CmdbReport") -> dict:
        """Convert a CmdbReport instance to json conform data"""
        return {
            'public_id': instance.get_public_id(),
            'report_category_id': instance.report_category_id,
            'name': instance.name,
            'type_id': instance.type_id,
            'selected_fields': instance.selected_fields,
            'conditions': instance.conditions,
            'report_query': instance.report_query,
            'predefined': instance.predefined,
        }
