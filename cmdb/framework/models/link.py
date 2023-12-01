# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
from datetime import datetime, timezone

from cmdb.framework import CmdbDAO
from cmdb.framework.utils import Collection, Model
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectLinkModel(CmdbDAO):
    """TODO: document"""

    COLLECTION: Collection = "framework.links"
    MODEL: Model = 'ObjectLink'

    def __init__(self, public_id: int, primary: int, secondary: int, creation_time: datetime = None):
        if primary == secondary:
            raise ValueError(f'Same link IDs: {primary}/{secondary}')
        self.primary: int = primary
        self.secondary: int = secondary
        self.creation_time: datetime = creation_time or datetime.now(timezone.utc)
        super().__init__(public_id=public_id)


    def get_primary(self) -> int:
        """TODO: document"""
        return self.primary


    def get_secondary(self) -> int:
        """TODO: document"""
        return self.secondary


    def get_creation_time(self) -> datetime:
        """TODO: document"""
        return self.creation_time


    def get_partners(self) -> (int, int):
        """TODO: document"""
        return self.get_primary(), self.get_secondary()


    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "ObjectLinkModel":
        """Convert the database data to a link instance."""
        return cls(
            public_id=data.get('public_id'),
            primary=int(data.get('primary')),
            secondary=int(data.get('secondary')),
            creation_time=data.get('creation_time', None),
        )


    @classmethod
    def to_json(cls, instance: "ObjectLinkModel") -> dict:
        """Convert a links instance to json conform data."""
        return {
            'public_id': instance.public_id,
            'primary': instance.primary,
            'secondary': instance.secondary,
            'creation_time': instance.creation_time,
        }
