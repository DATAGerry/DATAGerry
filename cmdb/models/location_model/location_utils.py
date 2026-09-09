# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2026 becon GmbH
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
This module contains helper methods for CmdbLocations

``validate_root_location`` answers whether a document is the synthetic root; ``to_location_document``
normalises a raw location document to the canonical key set (the same keys CmdbLocation.to_json
emits, optional render keys defaulted) and ``sort_locations_by_name`` puts one tree level into the
order the tree renders it in
"""
from typing import Any

from cmdb.models.location_model.location_constants import CmdbLocationDefault, LocationKey
# -------------------------------------------------------------------------------------------------------------------- #

def validate_root_location(tested_location: dict) -> bool:
    """
    Checks if a given location holds valid root location data

    Args:
        tested_location (dict): location data which should be tested

    Returns:
        (bool): Returns boolean if the given dict has valid root location data
    """
    # pylint: disable=import-outside-toplevel
    # Resolved at call time, not at module import time: this is the model layer reaching UP into the
    # database layer, and the predefined root document is built from this package's own constants, so a
    # module-level import closes the cycle cmdb.models.location_model (package __init__) ->
    # predefined_data.cmdb_data -> back into location_constants while this package is still
    # half-initialised - which is what made collection_validator, database_updater, route_utils,
    # init_rest_api and gunicorn unimportable as the first cmdb module of a process
    from cmdb.database.predefined_data.cmdb_data import get_root_location_data

    root_location = get_root_location_data()

    for root_key, root_value in root_location.items():
        if root_key not in tested_location.keys():
            return False

        # check if value is valid
        if root_value != tested_location[root_key]:
            return False

    return True


def to_location_document(document: dict[str, Any]) -> dict[str, Any]:
    """
    Normalises a raw CmdbLocation document to the canonical, JSON-compatible key set

    Answers with exactly the keys ``CmdbLocation.to_json`` emits - and with the same two fallbacks
    for the optional render keys (see CmdbLocationDefault) - so a caller that reads location
    documents straight from the database gets the identical payload a
    ``from_data`` -> ``to_json`` round trip would produce, without building the model. Keys the
    database adds (``_id``) or that a legacy document carries on top of the schema are dropped

    Args:
        document (dict[str, Any]): A raw CmdbLocation document as stored in the database

    Returns:
        dict[str, Any]: The canonical CmdbLocation payload
    """
    return {
        LocationKey.PUBLIC_ID.value: document.get(LocationKey.PUBLIC_ID.value),
        LocationKey.NAME.value: document.get(LocationKey.NAME.value),
        LocationKey.PARENT.value: document.get(LocationKey.PARENT.value),
        LocationKey.OBJECT_ID.value: document.get(LocationKey.OBJECT_ID.value),
        LocationKey.TYPE_ID.value: document.get(LocationKey.TYPE_ID.value),
        LocationKey.TYPE_LABEL.value: document.get(LocationKey.TYPE_LABEL.value),
        LocationKey.TYPE_ICON.value: document.get(LocationKey.TYPE_ICON.value, CmdbLocationDefault.TYPE_ICON),
        LocationKey.TYPE_SELECTABLE.value: document.get(
            LocationKey.TYPE_SELECTABLE.value, CmdbLocationDefault.TYPE_SELECTABLE
        ),
    }


def sort_locations_by_name(locations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Orders CmdbLocation documents by name, case-insensitively, with the public_id as tie-breaker

    The database reads behind the location tree are unordered as far as the tree is concerned
    (``BaseManager.get_many`` defaults to public_id descending), which surfaced as an
    insertion-order tree. Sorting happens here rather than in the query because MongoDB's default
    binary collation would order 'Zoo' before 'alpha', and a location level is small enough that the
    in-process sort costs nothing. A missing or non-string name sorts as an empty name, a missing
    public_id as 0, so a malformed document can never raise here

    Args:
        locations (list[dict[str, Any]]): CmdbLocation documents of a single tree level

    Returns:
        list[dict[str, Any]]: The same documents, name-ascending with a public_id tie-break
    """
    def sort_key(location: dict[str, Any]) -> tuple[str, int]:
        name: Any = location.get(LocationKey.NAME.value)
        public_id: Any = location.get(LocationKey.PUBLIC_ID.value)

        return (
            name.casefold() if isinstance(name, str) else '',
            public_id if isinstance(public_id, int) else 0,
        )

    return sorted(locations, key=sort_key)
