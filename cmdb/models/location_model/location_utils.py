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
"""
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
