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
Request options and manager bundle for the CI Explorer graph builder

``build_ci_explorer_graph`` used to take thirteen positional parameters - eight primitives and five
managers - which is why it carried three pylint suppressions and why a test of one scenario needed
thirteen arguments. The two frozen dataclasses here split that list along the seam it already had:
what the caller asked for, and what the builder may read it from.

``CiExplorerGraphRequest`` also owns the three flags derived from ``target_type`` and ``item_limit``,
so the direction and budget rules are stated once instead of being recomputed in every helper
"""
from dataclasses import dataclass

from cmdb.manager import (
    LocationsManager,
    ObjectRelationsManager,
    ObjectsManager,
    RelationsManager,
    TypesManager,
)
from cmdb.models.ci_explorer_model import NodeType
# -------------------------------------------------------------------------------------------------------------------- #

__all__: list[str] = [
    'CiExplorerGraphRequest',
    'CiExplorerManagers',
]


@dataclass(frozen=True)
class CiExplorerGraphRequest:
    """
    What the caller asked the CI Explorer for

    Attributes:
        target_id (int): public_id of the focal CmdbObject
        target_type (NodeType): Which direction(s) the response includes
        with_root (bool): Whether the response carries a 'root_node' block
        with_locations (bool): Whether dg_location neighbours are grafted in
        with_ipam_relations (bool): Whether IPAM-hierarchy neighbours are grafted in
        item_limit (int): Upper bound on neighbour nodes; 0 means unlimited
        types_filter (frozenset[int]): Allowed neighbour type_ids; empty disables filtering
        relations_filter (frozenset[int]): Allowed CmdbRelation public_ids; empty disables filtering
    """
    target_id: int
    target_type: NodeType
    with_root: bool = False
    with_locations: bool = False
    with_ipam_relations: bool = False
    item_limit: int = 0
    types_filter: frozenset[int] = frozenset()
    relations_filter: frozenset[int] = frozenset()

    @property
    def item_limit_active(self) -> bool:
        """
        Whether a neighbour cap applies at all

        Returns:
            bool: True when a positive item_limit was requested
        """
        return self.item_limit > 0

    @property
    def include_children(self) -> bool:
        """
        Whether the child direction is part of the response

        Returns:
            bool: True for NodeType.BOTH and NodeType.CHILD
        """
        return self.target_type in (NodeType.BOTH, NodeType.CHILD)

    @property
    def include_parents(self) -> bool:
        """
        Whether the parent direction is part of the response

        Returns:
            bool: True for NodeType.BOTH and NodeType.PARENT
        """
        return self.target_type in (NodeType.BOTH, NodeType.PARENT)


@dataclass(frozen=True)
class CiExplorerManagers:
    """
    The five managers the graph builder reads through

    Bundled so the builder and its helpers pass one argument instead of five, and so a test states
    only the managers its scenario touches

    Attributes:
        objects (ObjectsManager): db interface for CmdbObjects
        types (TypesManager): db interface for CmdbTypes
        relations (RelationsManager): db interface for CmdbRelations
        object_relations (ObjectRelationsManager): db interface for CmdbObjectRelations
        locations (LocationsManager): db interface for CmdbLocations
    """
    objects: ObjectsManager
    types: TypesManager
    relations: RelationsManager
    object_relations: ObjectRelationsManager
    locations: LocationsManager
