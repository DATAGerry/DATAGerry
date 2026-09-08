# DataGerry - OpenSource Enterprise CMDB
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
Constants of the IsmsRiskMatrix: its singleton id and the keys of one matrix cell

The document's own top-level keys are ``RiskMatrixKey`` in
``cmdb/database/predefined_data/predefined_data_constants.py``, where they sit next to the seeded
default. What lives here is what that module does not name: the id the singleton is always stored
under, and the keys *inside* a cell - which were spelled as bare literals in all four risk-matrix
helpers, the Cerberus schema, the report builder and the report routes' aggregations.

``UNASSIGNED_RISK_CLASS_ID`` is the value a cell carries while no IsmsRiskClass is assigned to it. It
is 0 rather than null because the whole grid is written at once: a freshly generated cell and a cell
whose risk class was deleted are the same state, and the config wizard's "are all cells assigned"
check reads it as "not yet"
"""
from cmdb.utils import BaseStrEnum
# -------------------------------------------------------------------------------------------------------------------- #

__all__: list[str] = [
    'RiskMatrixCellKey',
    'RISK_MATRIX_PUBLIC_ID',
    'UNASSIGNED_RISK_CLASS_ID',
]

# The IsmsRiskMatrix is a singleton: one document, always at this public_id
RISK_MATRIX_PUBLIC_ID: int = 1

# A cell with no IsmsRiskClass assigned yet
UNASSIGNED_RISK_CLASS_ID: int = 0


class RiskMatrixCellKey(BaseStrEnum):
    """
    Keys of one cell of the IsmsRiskMatrix grid

    A cell's IDENTITY is the (impact_id, likelihood_id) pair, not its row/column: the grid is ordered
    by ``calculation_basis``, so changing a level's weight moves the cell but must not move the risk
    class an admin assigned to it. ``_transfer_risk_classes`` keys on exactly that pair for that reason
    """
    ROW = 'row'
    COLUMN = 'column'
    IMPACT_ID = 'impact_id'
    IMPACT_VALUE = 'impact_value'
    LIKELIHOOD_ID = 'likelihood_id'
    LIKELIHOOD_VALUE = 'likelihood_value'
    CALCULATED_VALUE = 'calculated_value'
    RISK_CLASS_ID = 'risk_class_id'
