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
The module builds a MongoDB query for a dict of conditions
"""
import logging
from typing import Union

from cmdb.models.type_model.type import TypeModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              MongoDBQueryBuilder - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #

class MongoDBQueryBuilder:
    """
    The MongoDBQueryBuilder generates a MongoDB query from a dict of rules
    """
    def __init__(self, query_data: dict, report_type: TypeModel):
        self.condition = None
        self.rules = None

        if query_data:
            self.condition = query_data["condition"]
            self.rules = query_data["rules"]

        self.report_type = report_type
        self.mds_fields = self.report_type.get_all_mds_fields()

    def build(self):
        """
        Builds the MongoDB query by using the self.conditions
        """
        if self.condition and self.rules:
            return self.__build_ruleset(self.condition, self.rules)

        return {}


    def __build_ruleset(self, condition: str, rules: list[dict]):
        """TODO. document"""
        children = []

        for rule in rules:
            if "condition" in rule:
                children.append(self.__build_ruleset(rule["condition"], rule["rules"]))
            else:
                if "value" in rule:
                    children.append(self.__build_rule(rule["field"], rule["operator"], rule["value"]))
                else:
                    children.append(self.__build_rule(rule["field"], rule["operator"]))


        possible_conditions = {
            "and": {'$and': [{'$and': children}, {"type_id": self.report_type.public_id}]},
            "or": {'$and': [{'$or': children}, {"type_id": self.report_type.public_id}]},
        }

        return possible_conditions[condition]


    def __build_rule(self, field: str, operator: str, value: Union[int, str, list[str]] = None):
        """TODO: document"""
        target_field_name = 'fields.name'
        target_field_value = 'fields.value'

        if field in self.mds_fields:
            target_field_name = 'multi_data_sections.values.data.name'
            target_field_value = 'multi_data_sections.values.data.value'

        possible_operators = {
            "=": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$eq": value}}]},
            "!=": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$ne": value}}]},
            "<=": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$lte": value}}]},
            ">=": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$gte": value}}]},
            "<": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$lt": value}}]},
            ">": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$gt": value}}]},
            "in": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$in": value}}]},
            "not in": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$nin": value}}]},
            "contains": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$regex": value}}]},
            "like": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: "/"+str(value)+"/"}]},
            "is null": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: None}]},
            "is not null": {'$and':[{target_field_name: {'$eq':field}}, {target_field_value: {"$ne": None}}]},
        }

        return possible_operators[operator]
