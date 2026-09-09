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
Unit tests for cmdb.models.location_model.location_utils

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

``to_location_document`` and ``sort_locations_by_name`` are the two helpers the LocationsManager's
tree-facing reads use instead of a dict -> model -> dict round trip: the first is pinned against an
actual ``from_data`` -> ``to_json`` round trip so the two can not drift apart, the second against the
malformed documents (no name, no public_id) a level must survive.
"""
from typing import Any

import pytest

from cmdb.database.predefined_data.cmdb_data import get_root_location_data
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.location_model.location_constants import CmdbLocationDefault, LocationKey, RootLocationDefault
from cmdb.models.location_model.location_utils import (
    sort_locations_by_name,
    to_location_document,
    validate_root_location,
)
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


# -------------------------------------------------------------------------------------------------------------------- #
#                                                to_location_document                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class TestToLocationDocument:
    """The dict -> canonical dict normaliser the tree-facing reads use instead of the model."""

    @staticmethod
    def _stored_document() -> dict[str, Any]:
        """A complete CmdbLocation document as it comes back from MongoDB."""
        return {
            LocationKey.PUBLIC_ID.value: 7,
            LocationKey.NAME.value: 'srv',
            LocationKey.PARENT.value: RootLocationDefault.PUBLIC_ID,
            LocationKey.OBJECT_ID.value: 42,
            LocationKey.TYPE_ID.value: 11,
            LocationKey.TYPE_LABEL.value: 'Server',
            LocationKey.TYPE_ICON.value: 'fas fa-server',
            LocationKey.TYPE_SELECTABLE.value: False,
        }

    def test_complete_document_is_passed_through_unchanged(self) -> None:
        """A document carrying every key comes back with exactly those values"""
        document = self._stored_document()

        assert to_location_document(document) == document

    def test_optional_render_keys_fall_back_to_their_defaults(self) -> None:
        """The two keys a document may omit are filled the same way CmdbLocation.from_data fills them"""
        document = self._stored_document()
        del document[LocationKey.TYPE_ICON.value]
        del document[LocationKey.TYPE_SELECTABLE.value]

        result = to_location_document(document)

        assert result[LocationKey.TYPE_ICON.value] == CmdbLocationDefault.TYPE_ICON
        assert result[LocationKey.TYPE_SELECTABLE.value] == CmdbLocationDefault.TYPE_SELECTABLE

    def test_matches_a_model_round_trip(self) -> None:
        """The normaliser and a from_data -> to_json round trip answer with the identical payload"""
        document = self._stored_document()

        assert to_location_document(document) == CmdbLocation.to_json(CmdbLocation.from_data(document))

    def test_unknown_keys_are_dropped(self) -> None:
        """Keys MongoDB or a legacy migration added are not part of the canonical payload"""
        document = {**self._stored_document(), '_id': 'mongo-owned', 'legacy_key': 'gone'}

        result = to_location_document(document)

        assert '_id' not in result
        assert 'legacy_key' not in result

    def test_missing_required_keys_become_none(self) -> None:
        """A malformed document normalises to None values rather than raising"""
        result = to_location_document({})

        assert result[LocationKey.PUBLIC_ID.value] is None
        assert result[LocationKey.NAME.value] is None
        assert result[LocationKey.PARENT.value] is None


# -------------------------------------------------------------------------------------------------------------------- #
#                                               sort_locations_by_name                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class TestSortLocationsByName:
    """One tree level in the order the tree renders it: name-ascending, public_id as tie-breaker."""

    @staticmethod
    def _location(public_id: int, name: Any) -> dict[str, Any]:
        """A minimal location document carrying just the two keys the sort reads."""
        return {LocationKey.PUBLIC_ID.value: public_id, LocationKey.NAME.value: name}

    def test_sorts_case_insensitively(self) -> None:
        """Upper and lower case interleave by name instead of by byte value"""
        locations = [self._location(1, 'beta'), self._location(2, 'Alpha'), self._location(3, 'gamma')]

        result = sort_locations_by_name(locations)

        assert [location[LocationKey.NAME.value] for location in result] == ['Alpha', 'beta', 'gamma']

    def test_equal_names_are_ordered_by_public_id(self) -> None:
        """Two locations of the same name keep a stable, id-ascending order"""
        locations = [self._location(9, 'Rack'), self._location(4, 'rack')]

        result = sort_locations_by_name(locations)

        assert [location[LocationKey.PUBLIC_ID.value] for location in result] == [4, 9]

    @pytest.mark.parametrize('broken_name', [None, 17, ['a']], ids=['null', 'int', 'list'])
    def test_malformed_name_sorts_first_without_raising(self, broken_name: Any) -> None:
        """A non-string name is treated as an empty name rather than crashing the level"""
        locations = [self._location(1, 'Alpha'), self._location(2, broken_name)]

        result = sort_locations_by_name(locations)

        assert result[0][LocationKey.PUBLIC_ID.value] == 2

    def test_missing_public_id_is_treated_as_zero(self) -> None:
        """A document without a public_id still participates in the tie-break"""
        locations = [self._location(3, 'rack'), {LocationKey.NAME.value: 'rack'}]

        result = sort_locations_by_name(locations)

        assert LocationKey.PUBLIC_ID.value not in result[0]

    def test_input_list_is_not_mutated(self) -> None:
        """Sorting answers with a new list, so a caller's own ordering survives"""
        locations = [self._location(1, 'beta'), self._location(2, 'Alpha')]

        result = sort_locations_by_name(locations)

        assert result is not locations
        assert [location[LocationKey.PUBLIC_ID.value] for location in locations] == [1, 2]
