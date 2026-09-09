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
Unit tests for cmdb.manager.locations_manager.LocationsManager

Pure tests: no Mongo. Each method is driven against a ``MagicMock(spec=LocationsManager)`` with
its database collaborators (insert / get_many / aggregate / update / delete_*) stubbed, so only
the manager's own behavior is exercised - payload coercion, the ``$graphLookup`` pipeline shape,
the update match key, the empty-data guard, the canonical document + name ordering of the
tree-facing reads, the root-deletion and parentless-promotion refusals, and the error-wrapping into
the LocationsManager error hierarchy. The ``$graphLookup`` query itself is pinned against real MongoDB in
tests/integration/framework/test_integration_locations_crud.py.
"""
# pylint: disable=protected-access
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.locations_manager import (
    LocationsManager,
    ancestors_lookup_stage,
    descendants_lookup_stage,
)
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.location_model.location_constants import CmdbLocationDefault, RootLocationDefault

from cmdb.errors.models.cmdb_location import CmdbLocationToJsonError
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
    BaseManagerUpdateError,
)
from cmdb.errors.manager.locations_manager import (
    LocationsManagerInitError,
    LocationsManagerInsertError,
    LocationsManagerGetError,
    LocationsManagerUpdateError,
    LocationsManagerDeleteError,
    LocationsManagerIterationError,
    LocationsManagerChildrenError,
)
# -------------------------------------------------------------------------------------------------------------------- #

MODULE_PATH: str = 'cmdb.manager.locations_manager'

ROOT_PUBLIC_ID: int = RootLocationDefault.PUBLIC_ID
LOCATION_PUBLIC_ID: int = 7
OBJECT_ID: int = 42
PARENT_ID: int = 3
TYPE_ID: int = 11
CHILD_OBJECT_ID: int = 142
TOTAL_LOCATIONS: int = 2

SAMPLE_LOCATION_DICT: dict[str, Any] = {
    'public_id': LOCATION_PUBLIC_ID,
    'name': 'srv',
    'parent': PARENT_ID,
    'object_id': OBJECT_ID,
    'type_id': TYPE_ID,
    'type_label': 'Server',
}


def _mock_manager() -> MagicMock:
    """A MagicMock standing in for a LocationsManager instance."""
    return MagicMock(spec=LocationsManager)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   insert_location                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class TestInsertLocation:
    """``insert_location`` forwards a dict as-is, converts a model, and wraps insert failures."""

    def test_dict_payload_is_inserted_directly(self) -> None:
        """A dict payload is handed straight to ``insert`` and the new public_id is returned."""
        mgr = _mock_manager()
        mgr.insert.return_value = LOCATION_PUBLIC_ID

        result = LocationsManager.insert_location(mgr, dict(SAMPLE_LOCATION_DICT))

        mgr.insert.assert_called_once_with(SAMPLE_LOCATION_DICT)
        assert result == LOCATION_PUBLIC_ID

    def test_cmdb_location_is_converted_via_to_json(self) -> None:
        """A CmdbLocation instance is serialized with ``to_json`` before insert."""
        mgr = _mock_manager()
        mgr.insert.return_value = LOCATION_PUBLIC_ID
        location = MagicMock(spec=CmdbLocation)

        with patch(f'{MODULE_PATH}.CmdbLocation.to_json', return_value=SAMPLE_LOCATION_DICT) as to_json_mock:
            result = LocationsManager.insert_location(mgr, location)

        to_json_mock.assert_called_once_with(location)
        mgr.insert.assert_called_once_with(SAMPLE_LOCATION_DICT)
        assert result == LOCATION_PUBLIC_ID

    def test_base_insert_error_wraps_as_locations_insert_error(self) -> None:
        """A ``BaseManagerInsertError`` from ``insert`` is wrapped as ``LocationsManagerInsertError``."""
        mgr = _mock_manager()
        mgr.insert.side_effect = BaseManagerInsertError('write failed')

        with pytest.raises(LocationsManagerInsertError):
            LocationsManager.insert_location(mgr, dict(SAMPLE_LOCATION_DICT))

    def test_to_json_error_wraps_as_locations_insert_error(self) -> None:
        """A ``CmdbLocationToJsonError`` during conversion is wrapped as ``LocationsManagerInsertError``."""
        mgr = _mock_manager()
        location = MagicMock(spec=CmdbLocation)

        with patch(f'{MODULE_PATH}.CmdbLocation.to_json', side_effect=CmdbLocationToJsonError('bad model')):
            with pytest.raises(LocationsManagerInsertError):
                LocationsManager.insert_location(mgr, location)

    def test_missing_public_id_wraps_as_locations_insert_error(self) -> None:
        """An insert answering with no public_id is reported instead of returned as None."""
        mgr = _mock_manager()
        mgr.insert.return_value = None

        with pytest.raises(LocationsManagerInsertError):
            LocationsManager.insert_location(mgr, dict(SAMPLE_LOCATION_DICT))

    def test_unexpected_error_wraps_as_locations_insert_error(self) -> None:
        """A generic exception is wrapped as ``LocationsManagerInsertError``."""
        mgr = _mock_manager()
        mgr.insert.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerInsertError):
            LocationsManager.insert_location(mgr, dict(SAMPLE_LOCATION_DICT))


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       iterate                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
class TestIterate:
    """``iterate`` runs the aggregation and binds the rows to an IterationResult of CmdbLocation."""

    def test_wraps_query_result_in_iteration_result(self) -> None:
        """The aggregation result and total are forwarded to ``IterationResult`` with the model bound."""
        mgr = _mock_manager()
        aggregation_result = [SAMPLE_LOCATION_DICT]
        mgr.iterate_query.return_value = (aggregation_result, TOTAL_LOCATIONS)
        builder_params = MagicMock(name='builder_params')
        sentinel_result = MagicMock(name='iteration_result')

        with patch(f'{MODULE_PATH}.IterationResult', return_value=sentinel_result) as result_ctor:
            result = LocationsManager.iterate(mgr, builder_params)

        mgr.iterate_query.assert_called_once_with(builder_params)
        result_ctor.assert_called_once_with(aggregation_result, TOTAL_LOCATIONS, CmdbLocation)
        assert result is sentinel_result

    def test_iteration_error_wraps_as_locations_iteration_error(self) -> None:
        """A ``BaseManagerIterationError`` from ``iterate_query`` becomes ``LocationsManagerIterationError``."""
        mgr = _mock_manager()
        mgr.iterate_query.side_effect = BaseManagerIterationError('bad pipeline')

        with pytest.raises(LocationsManagerIterationError):
            LocationsManager.iterate(mgr, MagicMock())

    def test_unexpected_error_wraps_as_locations_iteration_error(self) -> None:
        """A generic exception is also wrapped as ``LocationsManagerIterationError``."""
        mgr = _mock_manager()
        mgr.iterate_query.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerIterationError):
            LocationsManager.iterate(mgr, MagicMock())


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       get_location                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetLocation:
    """``get_location`` / ``get_location_for_object`` translate get failures to the locations variant."""

    def test_get_location_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerGetError`` from ``get_one`` is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_one.side_effect = BaseManagerGetError('db down')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_location(mgr, LOCATION_PUBLIC_ID)

    def test_get_location_for_object_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerGetError`` from ``get_one_by`` is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_one_by.side_effect = BaseManagerGetError('db down')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_location_for_object(mgr, OBJECT_ID)

    def test_get_location_for_object_queries_by_object_id(self) -> None:
        """The lookup criteria pin the ``object_id`` field."""
        mgr = _mock_manager()
        mgr.get_one_by.return_value = SAMPLE_LOCATION_DICT

        result = LocationsManager.get_location_for_object(mgr, OBJECT_ID)

        mgr.get_one_by.assert_called_once_with({'object_id': OBJECT_ID})
        assert result == SAMPLE_LOCATION_DICT

    def test_get_location_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A generic exception from ``get_one`` is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_one.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_location(mgr, LOCATION_PUBLIC_ID)

    def test_get_location_for_object_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A generic exception from ``get_one_by`` is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_one_by.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_location_for_object(mgr, OBJECT_ID)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   get_locations_by                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetLocationsBy:
    """``get_locations_by`` filters the bound collection and hydrates each row to ``CmdbLocation``."""

    def test_hydrates_each_raw_row_via_from_data(self) -> None:
        """Filters are forwarded to ``get_many`` and every row is rehydrated through ``from_data``."""
        mgr = _mock_manager()
        rows = [SAMPLE_LOCATION_DICT, {**SAMPLE_LOCATION_DICT, 'public_id': LOCATION_PUBLIC_ID + 1}]
        mgr.get_many.return_value = rows
        hydrated = [MagicMock(name='loc1'), MagicMock(name='loc2')]

        with patch.object(CmdbLocation, 'from_data', side_effect=hydrated) as from_data_mock:
            result = LocationsManager.get_locations_by(mgr, parent=PARENT_ID)

        mgr.get_many.assert_called_once_with(parent=PARENT_ID)
        assert [c.args[0] for c in from_data_mock.call_args_list] == rows
        assert result == hydrated

    def test_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A failure during retrieval/hydration is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_many.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_locations_by(mgr, parent=PARENT_ID)


# -------------------------------------------------------------------------------------------------------------------- #
#                                              get_all_descendant_locations                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetAllDescendantLocations:
    """``get_all_descendant_locations`` resolves the subtree with a single ``$graphLookup`` aggregation."""

    def test_pipeline_walks_parent_to_public_id_edges(self) -> None:
        """The aggregation matches the start id then graph-walks ``parent`` -> ``public_id`` edges."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'descendants': []}]

        LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID)

        pipeline = mgr.aggregate.call_args.args[0]
        assert pipeline[0]['$match'] == {'public_id': LOCATION_PUBLIC_ID}
        graph_lookup = pipeline[1]['$graphLookup']
        assert graph_lookup['from'] == CmdbLocation.COLLECTION
        assert graph_lookup['connectFromField'] == 'public_id'
        assert graph_lookup['connectToField'] == 'parent'
        assert graph_lookup['as'] == 'descendants'
        # only the descendants' public_id leaves the server
        assert pipeline[2]['$project'] == {'_id': 0, 'descendants.public_id': 1}

    def test_returns_descendants_from_first_result_row(self) -> None:
        """The descendants array of the matched root document is returned."""
        mgr = _mock_manager()
        descendants = [{'public_id': 8}, {'public_id': 9}]
        mgr.aggregate.return_value = [{'descendants': descendants}]

        result = LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID)

        assert result == descendants

    def test_empty_aggregation_result_yields_empty_list(self) -> None:
        """A start id that matches nothing yields an empty list."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = []

        assert LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID) == []

    def test_missing_descendants_key_yields_empty_list(self) -> None:
        """A matched root with no descendants key defaults to an empty list."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{}]

        assert LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID) == []

    def test_iteration_error_wraps_as_locations_children_error(self) -> None:
        """A ``BaseManagerIterationError`` from ``aggregate`` becomes ``LocationsManagerChildrenError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = BaseManagerIterationError('bad pipeline')

        with pytest.raises(LocationsManagerChildrenError):
            LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID)

    def test_unexpected_error_wraps_as_locations_children_error(self) -> None:
        """A generic exception is also wrapped as ``LocationsManagerChildrenError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerChildrenError):
            LocationsManager.get_all_descendant_locations(mgr, LOCATION_PUBLIC_ID)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    update_location                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class TestUpdateLocation:
    """``update_location`` matches the row by its ``object_id`` and wraps update failures."""

    def test_matches_on_object_id(self) -> None:
        """The update is scoped to the row's ``object_id``."""
        mgr = _mock_manager()

        LocationsManager.update_location(mgr, OBJECT_ID, dict(SAMPLE_LOCATION_DICT))

        mgr.update.assert_called_once_with({'object_id': OBJECT_ID}, SAMPLE_LOCATION_DICT)

    def test_cmdb_location_payload_is_converted_via_to_json(self) -> None:
        """A CmdbLocation payload is serialized with ``to_json`` before the update."""
        mgr = _mock_manager()
        data = MagicMock(spec=CmdbLocation)

        with patch(f'{MODULE_PATH}.CmdbLocation.to_json', return_value=SAMPLE_LOCATION_DICT) as to_json_mock:
            LocationsManager.update_location(mgr, OBJECT_ID, data)

        to_json_mock.assert_called_once_with(data)
        mgr.update.assert_called_once_with({'object_id': OBJECT_ID}, SAMPLE_LOCATION_DICT)

    def test_unexpected_error_wraps_as_locations_update_error(self) -> None:
        """A failure from ``update`` is wrapped as ``LocationsManagerUpdateError``."""
        mgr = _mock_manager()
        mgr.update.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerUpdateError):
            LocationsManager.update_location(mgr, OBJECT_ID, dict(SAMPLE_LOCATION_DICT))


# -------------------------------------------------------------------------------------------------------------------- #
#                                                update_locations_by_type                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class TestUpdateLocationsByType:
    """``update_locations_by_type`` bulk-updates all locations of a type, guarding empty data."""

    def test_empty_data_is_a_noop(self) -> None:
        """Empty update data short-circuits before any ``update_many`` is issued."""
        mgr = _mock_manager()

        assert LocationsManager.update_locations_by_type(mgr, TYPE_ID, {}) is False

        mgr.update_many.assert_not_called()

    def test_issues_update_many_scoped_to_type_id(self) -> None:
        """The happy path issues a single ``update_many`` scoped to the type id."""
        mgr = _mock_manager()
        changed_data = {'type_label': 'Renamed'}

        assert LocationsManager.update_locations_by_type(mgr, TYPE_ID, changed_data) is True

        mgr.update_many.assert_called_once_with(criteria={'type_id': TYPE_ID}, update=changed_data)

    def test_update_error_wraps_as_locations_update_error(self) -> None:
        """A ``BaseManagerUpdateError`` from ``update_many`` becomes ``LocationsManagerUpdateError``."""
        mgr = _mock_manager()
        mgr.update_many.side_effect = BaseManagerUpdateError('write failed')

        with pytest.raises(LocationsManagerUpdateError):
            LocationsManager.update_locations_by_type(mgr, TYPE_ID, {'type_label': 'Renamed'})

    def test_unexpected_error_wraps_as_locations_update_error(self) -> None:
        """A generic exception from ``update_many`` becomes ``LocationsManagerUpdateError``."""
        mgr = _mock_manager()
        mgr.update_many.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerUpdateError):
            LocationsManager.update_locations_by_type(mgr, TYPE_ID, {'type_label': 'Renamed'})


# -------------------------------------------------------------------------------------------------------------------- #
#                                        search_locations_with_ancestors                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class TestSearchLocationsWithAncestors:
    """The search matches names, folds in each match's ancestors, dedupes, drops root, sorts."""

    @staticmethod
    def _match(public_id: int, name: str, parent: int, ancestors: list[dict[str, Any]]) -> dict[str, Any]:
        """An aggregation result row: a matched location carrying its $graphLookup ancestors."""
        return {'public_id': public_id, 'name': name, 'parent': parent, 'ancestors': ancestors}

    def test_returns_matches_and_ancestors_deduped_sorted_without_root(self) -> None:
        """Two matches sharing a parent yield rack + both servers once each, root excluded, sorted."""
        mgr = _mock_manager()
        rack = {'public_id': 5, 'name': 'rack', 'parent': 1}
        root = {'public_id': 1, 'name': 'Root', 'parent': 0}
        mgr.aggregate.return_value = [
            self._match(10, 'srv-a', 5, [dict(rack), dict(root)]),
            self._match(11, 'srv-b', 5, [dict(rack), dict(root)]),
        ]

        result = LocationsManager.search_locations_with_ancestors(mgr, 'srv')

        assert [loc['public_id'] for loc in result] == [5, 10, 11]
        assert all('ancestors' not in loc for loc in result)
        # every row is a canonical location document, with the optional render keys defaulted
        assert result[0]['type_icon'] == CmdbLocationDefault.TYPE_ICON
        assert result[0]['type_selectable'] == CmdbLocationDefault.TYPE_SELECTABLE

    def test_pipeline_uses_escaped_case_insensitive_regex_and_excludes_root(self) -> None:
        """The query is escaped to a literal case-insensitive substring; the synthetic root is skipped."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = []

        LocationsManager.search_locations_with_ancestors(mgr, 'a.b')

        pipeline = mgr.aggregate.call_args.args[0]
        assert pipeline[0]['$match']['name'] == {'$regex': 'a\\.b', '$options': 'i'}
        assert pipeline[0]['$match']['public_id'] == {'$gt': 1}
        graph = pipeline[1]['$graphLookup']
        assert graph['connectFromField'] == 'parent'
        assert graph['connectToField'] == 'public_id'
        assert pipeline[2]['$project'] == {'_id': 0, 'ancestors._id': 0}

    def test_empty_query_returns_empty_without_querying(self) -> None:
        """A blank query short-circuits to [] and never touches the database."""
        mgr = _mock_manager()

        assert LocationsManager.search_locations_with_ancestors(mgr, '   ') == []
        mgr.aggregate.assert_not_called()

    def test_aggregation_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerIterationError`` from the aggregation becomes ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = BaseManagerIterationError('bad pipeline')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.search_locations_with_ancestors(mgr, 'srv')

    def test_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A generic exception from the aggregation is also wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.search_locations_with_ancestors(mgr, 'srv')

    def test_result_is_ordered_by_name_case_insensitively(self) -> None:
        """Matches come back name-ascending regardless of case or of the aggregation's own order."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [
            self._match(10, 'beta', 5, []),
            self._match(11, 'Alpha', 5, []),
        ]

        result = LocationsManager.search_locations_with_ancestors(mgr, 'a')

        assert [loc['name'] for loc in result] == ['Alpha', 'beta']


# -------------------------------------------------------------------------------------------------------------------- #
#                                             get_locations_on_path_to                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetLocationsOnPathTo:
    """``get_locations_on_path_to`` expands the tree along a target's ancestor path in one $in query."""

    def test_expands_root_and_each_ancestor_level(self) -> None:
        """The $in over the level query covers the synthetic root plus every (non-root) ancestor id."""
        mgr = _mock_manager()
        # target 9 sits under parent 5 under 2 under the synthetic root 1
        ancestors = [
            {'public_id': 5, 'name': 'b', 'parent': 2},
            {'public_id': 2, 'name': 'a', 'parent': ROOT_PUBLIC_ID},
            {'public_id': ROOT_PUBLIC_ID, 'name': 'Root', 'parent': 0},
        ]
        mgr.aggregate.return_value = [{'public_id': 9, 'name': 't', 'parent': 5, 'ancestors': ancestors}]
        mgr.get_many.return_value = [{'public_id': 9, 'name': 't', 'parent': 5}]

        result = LocationsManager.get_locations_on_path_to(mgr, 9)

        assert [loc['public_id'] for loc in result] == [9]
        assert result[0]['type_icon'] == CmdbLocationDefault.TYPE_ICON
        parent_filter = mgr.get_many.call_args.kwargs['parent']
        assert sorted(parent_filter['$in']) == [ROOT_PUBLIC_ID, 2, 5]

    def test_pipeline_walks_parent_to_public_id_from_the_target(self) -> None:
        """The aggregation matches the target then graph-walks up ``parent`` -> ``public_id`` edges."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'public_id': 9, 'parent': ROOT_PUBLIC_ID, 'ancestors': []}]
        mgr.get_many.return_value = []

        LocationsManager.get_locations_on_path_to(mgr, 9)

        pipeline = mgr.aggregate.call_args.args[0]
        assert pipeline[0]['$match'] == {'public_id': 9}
        graph = pipeline[1]['$graphLookup']
        assert graph['from'] == CmdbLocation.COLLECTION
        assert graph['startWith'] == '$parent'
        assert graph['connectFromField'] == 'parent'
        assert graph['connectToField'] == 'public_id'
        assert pipeline[2]['$project'] == {'_id': 0, 'ancestors.public_id': 1}

    def test_levels_are_ordered_by_name_case_insensitively(self) -> None:
        """The expanded levels come back name-ascending, not in the read's public_id order."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'public_id': 9, 'parent': ROOT_PUBLIC_ID, 'ancestors': []}]
        mgr.get_many.return_value = [
            {'public_id': 9, 'name': 'beta', 'parent': ROOT_PUBLIC_ID},
            {'public_id': 8, 'name': 'Alpha', 'parent': ROOT_PUBLIC_ID},
        ]

        result = LocationsManager.get_locations_on_path_to(mgr, 9)

        assert [loc['name'] for loc in result] == ['Alpha', 'beta']

    def test_root_level_target_expands_only_the_root(self) -> None:
        """A target directly under the synthetic root expands just the root level (no ancestors)."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'public_id': 9, 'parent': ROOT_PUBLIC_ID, 'ancestors': []}]
        mgr.get_many.return_value = []

        LocationsManager.get_locations_on_path_to(mgr, 9)

        assert mgr.get_many.call_args.kwargs['parent'] == {'$in': [ROOT_PUBLIC_ID]}

    def test_missing_target_returns_empty_without_level_query(self) -> None:
        """An unknown target short-circuits to [] and never runs the level query."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = []

        assert LocationsManager.get_locations_on_path_to(mgr, 9) == []
        mgr.get_many.assert_not_called()

    def test_aggregation_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerIterationError`` from the ancestor aggregation becomes ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = BaseManagerIterationError('bad pipeline')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_locations_on_path_to(mgr, 9)

    def test_level_query_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerGetError`` from the level query becomes ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'public_id': 9, 'parent': ROOT_PUBLIC_ID, 'ancestors': []}]
        mgr.get_many.side_effect = BaseManagerGetError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_locations_on_path_to(mgr, 9)

    def test_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A generic exception is also wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_locations_on_path_to(mgr, 9)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    delete_location(s)                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class TestReparentChildrenToGrandparent:
    """``_reparent_children_to_grandparent`` promotes direct children onto the node's own parent."""

    def test_children_are_repointed_to_the_nodes_parent(self) -> None:
        """The node's parent is read and every direct child is re-pointed at it in one update_many."""
        mgr = _mock_manager()
        mgr.get_one_by.return_value = dict(SAMPLE_LOCATION_DICT)  # parent == PARENT_ID

        LocationsManager._reparent_children_to_grandparent(mgr, LOCATION_PUBLIC_ID)

        mgr.get_one_by.assert_called_once_with({'public_id': LOCATION_PUBLIC_ID})
        mgr.update_many.assert_called_once_with(
            criteria={'parent': LOCATION_PUBLIC_ID},
            update={'parent': PARENT_ID},
        )

    def test_missing_location_is_a_noop(self) -> None:
        """When the node does not exist, no re-parenting update is issued."""
        mgr = _mock_manager()
        mgr.get_one_by.return_value = None

        LocationsManager._reparent_children_to_grandparent(mgr, LOCATION_PUBLIC_ID)

        mgr.update_many.assert_not_called()

    @pytest.mark.parametrize(
        'stored_parent', [None, 'not-an-id', True], ids=['null_parent', 'non_int_parent', 'bool_parent'],
    )
    def test_childless_node_without_a_usable_parent_is_a_noop(self, stored_parent: Any) -> None:
        """``parent`` is nullable: with nothing to promote the deletion may still go ahead."""
        mgr = _mock_manager()
        mgr.get_one_by.return_value = {**SAMPLE_LOCATION_DICT, 'parent': stored_parent}
        mgr.get_parents_with_children.return_value = set()

        LocationsManager._reparent_children_to_grandparent(mgr, LOCATION_PUBLIC_ID)

        mgr.update_many.assert_not_called()

    def test_absent_parent_key_is_treated_as_no_parent(self) -> None:
        """A document that carries no ``parent`` key at all is read without raising a KeyError."""
        mgr = _mock_manager()
        stored = {key: value for key, value in SAMPLE_LOCATION_DICT.items() if key != 'parent'}
        mgr.get_one_by.return_value = stored
        mgr.get_parents_with_children.return_value = set()

        LocationsManager._reparent_children_to_grandparent(mgr, LOCATION_PUBLIC_ID)

        mgr.update_many.assert_not_called()

    def test_children_without_a_usable_parent_refuse_the_promotion(self) -> None:
        """Children are never written onto a null parent - that would drop them out of the tree."""
        mgr = _mock_manager()
        mgr.get_one_by.return_value = {**SAMPLE_LOCATION_DICT, 'parent': None}
        mgr.get_parents_with_children.return_value = {LOCATION_PUBLIC_ID}

        with pytest.raises(LocationsManagerUpdateError):
            LocationsManager._reparent_children_to_grandparent(mgr, LOCATION_PUBLIC_ID)

        mgr.update_many.assert_not_called()


class TestDeleteLocation:
    """``delete_location`` removes one row after promoting its direct children."""

    def test_delete_location_matches_on_public_id(self) -> None:
        """A single delete is scoped to the row's ``public_id`` and returns the ack."""
        mgr = _mock_manager()
        mgr.delete.return_value = True

        result = LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

        mgr.delete.assert_called_once_with({'public_id': LOCATION_PUBLIC_ID})
        assert result is True

    def test_delete_location_reparents_children_before_removing_the_node(self) -> None:
        """The node's direct children are promoted before the node itself is deleted."""
        mgr = _mock_manager()
        mgr.delete.return_value = True

        LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

        mgr._reparent_children_to_grandparent.assert_called_once_with(LOCATION_PUBLIC_ID)
        mgr.delete.assert_called_once_with({'public_id': LOCATION_PUBLIC_ID})

    def test_root_location_is_refused(self) -> None:
        """The synthetic root anchors every tree level and can not be deleted."""
        mgr = _mock_manager()

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, ROOT_PUBLIC_ID)

        mgr._reparent_children_to_grandparent.assert_not_called()
        mgr.delete.assert_not_called()

    def test_delete_location_error_wraps_as_locations_delete_error(self) -> None:
        """A ``BaseManagerDeleteError`` from ``delete`` becomes ``LocationsManagerDeleteError``."""
        mgr = _mock_manager()
        mgr.delete.side_effect = BaseManagerDeleteError('delete failed')

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

    def test_delete_location_reparent_get_error_wraps_as_locations_delete_error(self) -> None:
        """A ``BaseManagerGetError`` raised while re-parenting becomes ``LocationsManagerDeleteError``."""
        mgr = _mock_manager()
        mgr._reparent_children_to_grandparent.side_effect = BaseManagerGetError('lookup failed')

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

    def test_delete_location_reparent_update_error_wraps_as_locations_delete_error(self) -> None:
        """A ``BaseManagerUpdateError`` raised while re-parenting becomes ``LocationsManagerDeleteError``."""
        mgr = _mock_manager()
        mgr._reparent_children_to_grandparent.side_effect = BaseManagerUpdateError('update failed')

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

    def test_delete_location_reparent_refusal_wraps_as_locations_delete_error(self) -> None:
        """The parentless-promotion refusal reaches the caller as a delete error."""
        mgr = _mock_manager()
        mgr._reparent_children_to_grandparent.side_effect = LocationsManagerUpdateError('no parent')

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)

    def test_delete_location_unexpected_error_wraps_as_locations_delete_error(self) -> None:
        """A generic exception is also wrapped as ``LocationsManagerDeleteError``."""
        mgr = _mock_manager()
        mgr.delete.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerDeleteError):
            LocationsManager.delete_location(mgr, LOCATION_PUBLIC_ID)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       __init__                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
class TestInit:
    """The constructor binds the CmdbLocation collection and reports a failing base init."""

    def test_base_init_failure_wraps_as_locations_init_error(self) -> None:
        """A failure inside ``BaseManager.__init__`` surfaces as ``LocationsManagerInitError``."""
        with patch.object(BaseManager, '__init__', side_effect=RuntimeError('no connection')):
            with pytest.raises(LocationsManagerInitError):
                LocationsManager(MagicMock())


# -------------------------------------------------------------------------------------------------------------------- #
#                                             get_child_location_documents                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetChildLocationDocuments:
    """One tree level: canonical documents of the direct children, name-ordered, no model round trip."""

    def test_reads_the_children_of_the_parent(self) -> None:
        """The read is scoped to the ``parent`` field of the requested location."""
        mgr = _mock_manager()
        mgr.get_many.return_value = []

        assert LocationsManager.get_child_location_documents(mgr, PARENT_ID) == []
        mgr.get_many.assert_called_once_with(parent=PARENT_ID)

    def test_documents_are_canonical_with_defaulted_render_keys(self) -> None:
        """Every row carries the canonical key set; the optional render keys fall back to their defaults."""
        mgr = _mock_manager()
        mgr.get_many.return_value = [dict(SAMPLE_LOCATION_DICT)]

        result = LocationsManager.get_child_location_documents(mgr, PARENT_ID)

        assert result == [{
            'public_id': LOCATION_PUBLIC_ID,
            'name': 'srv',
            'parent': PARENT_ID,
            'object_id': OBJECT_ID,
            'type_id': TYPE_ID,
            'type_label': 'Server',
            'type_icon': CmdbLocationDefault.TYPE_ICON,
            'type_selectable': CmdbLocationDefault.TYPE_SELECTABLE,
        }]

    def test_level_is_ordered_by_name_case_insensitively(self) -> None:
        """The level is name-ascending regardless of the public_id-descending document read."""
        mgr = _mock_manager()
        mgr.get_many.return_value = [
            {**SAMPLE_LOCATION_DICT, 'public_id': 9, 'name': 'beta'},
            {**SAMPLE_LOCATION_DICT, 'public_id': 8, 'name': 'Alpha'},
        ]

        result = LocationsManager.get_child_location_documents(mgr, PARENT_ID)

        assert [location['name'] for location in result] == ['Alpha', 'beta']

    def test_keys_outside_the_schema_are_dropped(self) -> None:
        """A legacy document's extra keys do not leak into the tree payload."""
        mgr = _mock_manager()
        mgr.get_many.return_value = [{**SAMPLE_LOCATION_DICT, 'legacy_key': 'gone'}]

        result = LocationsManager.get_child_location_documents(mgr, PARENT_ID)

        assert 'legacy_key' not in result[0]

    def test_get_error_wraps_as_locations_get_error(self) -> None:
        """A ``BaseManagerGetError`` from the read is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_many.side_effect = BaseManagerGetError('db down')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_child_location_documents(mgr, PARENT_ID)

    def test_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A generic exception from the read is also wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.get_many.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_child_location_documents(mgr, PARENT_ID)


# -------------------------------------------------------------------------------------------------------------------- #
#                                               get_parents_with_children                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class TestGetParentsWithChildren:
    """The per-level has-children hint: one grouped aggregation, never a count per node."""

    def test_groups_the_candidate_parents_in_one_pipeline(self) -> None:
        """The pipeline matches the candidates by ``parent`` and groups by that same field."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = []

        LocationsManager.get_parents_with_children(mgr, [PARENT_ID, LOCATION_PUBLIC_ID])

        pipeline = mgr.aggregate.call_args.args[0]
        assert pipeline == [
            {'$match': {'parent': {'$in': [PARENT_ID, LOCATION_PUBLIC_ID]}}},
            {'$group': {'_id': '$parent'}},
        ]

    def test_returns_the_grouped_parent_ids(self) -> None:
        """The group ids are the parents that actually have a child."""
        mgr = _mock_manager()
        mgr.aggregate.return_value = [{'_id': PARENT_ID}, {'_id': LOCATION_PUBLIC_ID}]

        result = LocationsManager.get_parents_with_children(mgr, [PARENT_ID, LOCATION_PUBLIC_ID])

        assert result == {PARENT_ID, LOCATION_PUBLIC_ID}

    def test_empty_input_short_circuits_without_querying(self) -> None:
        """An empty candidate list answers with an empty set and never touches the database."""
        mgr = _mock_manager()

        assert LocationsManager.get_parents_with_children(mgr, []) == set()
        mgr.aggregate.assert_not_called()

    def test_unexpected_error_wraps_as_locations_get_error(self) -> None:
        """A failing aggregation is wrapped as ``LocationsManagerGetError``."""
        mgr = _mock_manager()
        mgr.aggregate.side_effect = RuntimeError('boom')

        with pytest.raises(LocationsManagerGetError):
            LocationsManager.get_parents_with_children(mgr, [PARENT_ID])


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   lookup stage builders                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class TestLookupStageBuilders:
    """The two shared ``$graphLookup`` stages walk the parent edge in opposite directions."""

    def test_ancestors_stage_walks_upwards(self) -> None:
        """The ancestor stage starts at ``parent`` and connects ``parent`` -> ``public_id``."""
        assert ancestors_lookup_stage() == {
            '$graphLookup': {
                'from': CmdbLocation.COLLECTION,
                'startWith': '$parent',
                'connectFromField': 'parent',
                'connectToField': 'public_id',
                'as': 'ancestors',
            }
        }

    def test_descendants_stage_walks_downwards(self) -> None:
        """The descendant stage starts at ``public_id`` and connects ``public_id`` -> ``parent``."""
        assert descendants_lookup_stage() == {
            '$graphLookup': {
                'from': CmdbLocation.COLLECTION,
                'startWith': '$public_id',
                'connectFromField': 'public_id',
                'connectToField': 'parent',
                'as': 'descendants',
            }
        }
