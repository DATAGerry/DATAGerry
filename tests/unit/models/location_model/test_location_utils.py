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
Unit tests for cmdb.models.location_model.location_utils.validate_root_location

Pure tests: no Mongo, no Flask. The function answers one question - does this dict carry the
predefined root document's values - by walking the keys of ``get_root_location_data()``, so the tests
pin what that walk decides: the predefined document itself passes, a document read back from Mongo
(plain string keys, since the document keys are ``LocationKey`` members only while being built)
passes too, and a missing key or a changed value fails. A dict that carries the root's values PLUS
extra keys also passes, which is the walk's direction and worth pinning as behaviour rather than
leaving to be rediscovered.

The database-layer import inside the function is deliberate (it is the model layer reaching UP, and
importing it at module level made every module that reaches the database services unimportable on its
own - see tests/unit/test_standalone_module_imports.py); calling the function is what proves the
deferred import resolves.
"""
from typing import Any

import pytest

from cmdb.database.predefined_data.cmdb_data import get_root_location_data
from cmdb.models.location_model.location_constants import LocationKey, RootLocationDefault
from cmdb.models.location_model.location_utils import validate_root_location
# -------------------------------------------------------------------------------------------------------------------- #

EXTRA_KEY: str = 'inserted_by_a_later_migration'
WRONG_NAME: str = 'Not the root'


def _string_keyed_root() -> dict[str, Any]:
    """
    Builds the root document the way it comes back from MongoDB - with plain string keys

    Returns:
        dict[str, Any]: The predefined root document, re-keyed to plain strings
    """
    # str() of a (str, Enum) member is 'LocationKey.NAME', not its value - the value is the key
    return {key.value: value for key, value in get_root_location_data().items()}


def test_accepts_the_predefined_root_document():
    """The document the seeding inserts is by definition valid root data"""
    assert validate_root_location(get_root_location_data()) is True


def test_accepts_the_root_document_read_back_with_string_keys():
    """A stored root document carries plain string keys and must still be recognised"""
    assert validate_root_location(_string_keyed_root()) is True


def test_accepts_a_root_document_carrying_extra_keys():
    """Only the root's own keys are checked, so additional keys do not make a document invalid"""
    tested_location = _string_keyed_root() | {EXTRA_KEY: 'anything'}

    assert validate_root_location(tested_location) is True


@pytest.mark.parametrize('missing_key', [key.value for key in LocationKey])
def test_rejects_a_document_missing_any_root_key(missing_key: str):
    """Every key of the predefined document is required, one at a time"""
    tested_location = _string_keyed_root()
    del tested_location[missing_key]

    assert validate_root_location(tested_location) is False


def test_rejects_a_document_whose_value_differs():
    """A present key with a different value is as invalid as a missing one"""
    tested_location = _string_keyed_root() | {LocationKey.NAME.value: WRONG_NAME}

    assert validate_root_location(tested_location) is False


def test_rejects_an_empty_document():
    """Nothing at all fails on the first key rather than passing vacuously"""
    assert validate_root_location({}) is False


def test_the_root_public_id_is_the_one_the_tree_expects():
    """Guards the predefined document against a changed root identity"""
    assert get_root_location_data()[LocationKey.PUBLIC_ID] == RootLocationDefault.PUBLIC_ID
