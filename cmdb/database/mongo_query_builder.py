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
from datetime import datetime

from cmdb.models.type_model.type import TypeModel

from cmdb.errors.mongo_query_builder import (
    MongoQueryBuilderInitError,
    MongoQueryBuilderInvalidOperatorError,
    MongoQueryBuilderBuildRuleError,
    MongoQueryBuilderBuildRulesetError,
    MongoQueryBuilderBuildError,
)
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
        try:
            self.condition = None
            self.rules = None

            if query_data:
                self.condition = query_data["condition"]
                self.rules = query_data["rules"]

            self.report_type = report_type
            self.number_fields = self.report_type.get_all_fields_of_type("number")
            self.date_fields = self.report_type.get_all_fields_of_type("date")
            self.ref_fields = self.report_type.get_all_fields_of_type("ref")
            self.ref_section_fields = self.report_type.get_all_fields_of_type("ref-section-field")
            self.mds_fields = self.report_type.get_all_mds_fields()
        except Exception as err:
            LOGGER.debug("[__init__] Exception: %s, Type: %s", err, type(err))
            raise MongoQueryBuilderInitError(err) from err


    def build(self):
        """
        Builds the MongoDB query by using the self.conditions
        """
        try:
            return self.__build_ruleset(self.condition, self.rules)
        except Exception as err:
            LOGGER.debug("[build] Exception: %s, Type: %s", err, type(err))
            raise MongoQueryBuilderBuildError(str(err)) from err

    def __build_ruleset(self, condition: str, rules: list[dict]):
        """TODO. document"""
        try:
            if self.condition and self.rules:
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
            else:
                return {"type_id": self.report_type.public_id}
        except Exception as err:
            raise MongoQueryBuilderBuildRulesetError(str(err)) from err

    def __build_rule(self, field_name: str, operator: str, value: Union[int, str, list[str]] = None):
        """TODO: document"""
        try:
            target_field = 'fields'
            target_value = value

            if field_name in self.date_fields and value:
                target_value = datetime.strptime(value, '%Y-%m-%d')

            if (field_name in self.ref_fields or
                field_name in self.ref_section_fields or field_name in self.number_fields) and value:
                target_value = int(value)

            if field_name in self.mds_fields:
                target_field = 'multi_data_sections.values.data'

            return self.create_rule(target_field, operator, field_name, target_value)
        except MongoQueryBuilderInvalidOperatorError as err:
            raise MongoQueryBuilderInvalidOperatorError(operator) from err
        except Exception as err:
            LOGGER.debug("[__build_rule] Exception: %s, Type: %s", err, type(err))
            raise MongoQueryBuilderBuildRuleError(str(err)) from err

# ------------------------------------------------------ HELPERS ----------------------------------------------------- #

    def create_rule(self,
                    target_field: str,
                    operator: str,
                    field_name: str,
                    value: Union[int, str, list[int], list[str]] = None) -> dict:
        """
        Transforms a rule to a MongoDB compatible query part
        
        Args:
            target_field (str): defines where to search for the value (fields or MDS)
            operator (str): operator of the rule
            field_name (str): name of field
            value (Union[int, str, list[int], list[str]], optional): value of the rule

        Raises:
            MongoQueryBuilderInvalidOperatorError: When an unsupported operator was provided

        Returns:
            dict: rule as MongoDB compatible query part
        """
        try:
            return {target_field: self.get_operator_fragment(operator, field_name, value)}
        except MongoQueryBuilderInvalidOperatorError as err:
            raise MongoQueryBuilderInvalidOperatorError(operator) from err

    def get_operator_fragment(self,
                              operator: str,
                              field_name: str,
                              value: Union[int, str, list[int], list[str]] = None) -> dict:
        """
        Creates the operator part of a condition for a MongoDB query

        Args:
            operator (str): operator of the condition like '<, =, !='
            field_name (str): field name of the condition
            value (Union[int, str, list[int], list[str]], optional): value of the condition

        Raises:
            MongoQueryBuilderInvalidOperatorError: When an unsupported operator was provided

        Returns:
            dict: operator part of the condition
        """
        try:
            return {
                "$elemMatch": {
                    "name": field_name,
                    "value": self.get_value_fragment(operator, value)
                }
            }
        except MongoQueryBuilderInvalidOperatorError as err:
            raise MongoQueryBuilderInvalidOperatorError(operator) from err


    def get_value_fragment(self,
                           operator: str,
                           value: Union[int, str, list[int], list[str]] = None) -> Union[dict, str]:
        """
        Creates the value part of a condition for a MongoDB query

        Args:
            operator (str): operator of the condition like '<, =, !='
            value (Union[int, str, list[int], list[str]], optional): value of the condition

        Raises:
            MongoQueryBuilderInvalidOperatorError: When an unsupported operator was provided

        Returns:
            Union[dict, str]: Value part of a condition
        """

        allowed_operators = {
            "=": {"$eq": value},
            "!=": {"$ne": value},
            "<=": {"$lte": value},
            ">=": {"$gte": value},
            "<": {"$lt": value},
            ">": {"$gt": value},
            "in": {"$in": value},
            "not in": {"$nin": value},
            "contains": {"$regex": value},
            "like": "/"+str(value)+"/",
            "is null": {"$in": [None, ""]},
            "is not null": {"$nin": [None, ""]},
        }

        if operator in allowed_operators:
            return allowed_operators[operator]

        raise MongoQueryBuilderInvalidOperatorError(operator)
