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
This module contains the implementation of CmdbWebhook, which is representing
a webhook in Datagarry
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  CmdbWebhook - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbWebhook(CmdbDAO):
    """
    TODO: document

    Attributes:
        COLLECTION (str):    Name of the database collection
        MODEL (Model):              Name of the DAO
        DEFAULT_VERSION (str):      The default "starting" version number
        SCHEMA (dict):              The validation schema for this DAO
        INDEX_KEYS (list):          List of index keys for the database
    """
    COLLECTION = 'framework.webhooks'
    MODEL = 'Webhook'
    DEFAULT_VERSION: str = '1.0.0'
    REQUIRED_INIT_KEYS = [
        'name',
        'url',
        'event_types',
        'active',
    ]

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
        },
        'url': {
            'type': 'string',
            'required': True,
        },
        'event_types': {
            'type': 'list',
            'required': True,
        },
        'active': {
            'type': 'boolean',
            'default': True
        },
    }

# ---------------------------------------------------- CONSTRUCTOR --------------------------------------------------- #

    def __init__(
            self,
            name:str,
            url: str,
            event_types: list,
            active: bool,
            **kwargs):
        """TODO: document"""
        self.name = name
        self.url = url
        self.event_types = event_types
        self.active = active

        super().__init__(**kwargs)

# --------------------------------------------------- CLASS METHODS -------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbWebhook":
        """
        Convert data to instance of CmdbWebhook
        """
        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            url=data.get('url'),
            event_types=data.get('event_types'),
            active=data.get('active'),
        )


    @classmethod
    def to_json(cls, instance: "CmdbWebhook") -> dict:
        """Convert a CmdbWebhook instance to json conform data"""
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'url': instance.url,
            'event_types': instance.event_types,
            'active': instance.active,
        }
