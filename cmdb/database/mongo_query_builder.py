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
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              MongoDBQueryBuilder - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #

class MongoDBQueryBuilder:
    """
    The MongoDBQueryBuilder generates a MongoDB query from a dict of rules
    """
    def __init__(self, query_data: dict, type_id: int):
        self.condition = query_data["condition"]
        self.rules = query_data["rules"]
        self.type_id = type_id

    def build(self):
        """
        Builds the MongoDB query by using the self.conditions
        """
        return self.__build_ruleset(self.condition, self.rules)


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
            "and": {"$and": [{"$and": children}, {"type_id": self.type_id}]},
            "or": {"$and": [{"$or": children}, {"type_id": self.type_id}]},
        }

        return possible_conditions[condition]


    def __build_rule(self, field: str, operator: str, value: Union[int, str, list[str]] = None):
        """TODO: document"""
        possible_operators = {
            "=": {field: {"$eq": value}},
            "!=": {field: {"$ne": value}},
            "<=": {field: {"$lte": value}},
            ">=": {field: {"$gte": value}},
            "<": {field: {"$lt": value}},
            ">": {field: {"$gt": value}},
            "in": {field: {"$in": value}},
            "not in": {field: {"$nin": value}},
            "contains":{field: {"$regex": value}},
            "like": {field: "/"+str(value)+"/"},
            "is null": {field : None},
            "is not null": {"$ne": None},
        }

        return possible_operators[operator]
