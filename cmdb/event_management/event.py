# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

"""Event definition

This module defines an internal CMDB event
"""
import json


class Event:
    """CMDB Event

    A CMDB event consists of a type (e.g. cmdb.core.objects.added)
    and a map of parameters (specific for a type).
    """

    def __init__(self, event_type, params=None):
        """Create a new event

        Args:
            event_type(str): event type (e.g. cmdb.core.objects.added)
            parms(dict): key value pairs of parameters
        """
        self.__event_type = event_type
        self.__params = {}
        if params:
            self.__params = params

    @staticmethod
    def create_event(json_repr):
        """ Create a new event from json strinf

        Args:
            json_repr: JSON representation of an event

        Returns
            Event: an event object
        """
        loaded_json = json.loads(json_repr)
        event_type = "default"
        event_params = {}
        if "type" in loaded_json:
            event_type = loaded_json["type"]
        if "params" in loaded_json:
            event_params = loaded_json["params"]
        return Event(event_type, event_params)

    def get_type(self):
        """Returns the event type

        Returns:
            str: type of the event
        """
        return self.__event_type

    def get_param(self, key, default=None):
        """ Returns the value of a parameter

        Args:
            key(str): parameter key
            default(str): default value

        Returns:
            str: parameter value, or default value, if parameter
                does not exist
        """
        output = default
        if key in self.__params:
            output = self.__params[key]
        return output

    def json_repr(self):
        """ Returns the JSON representation

        Returns:
            str: JSON representation of the event
        """
        output = {}
        output["type"] = self.__event_type
        output["params"] = self.__params
        return json.dumps(output)

    def __str__(self):
        output = "Event {}".format(self.__event_type)
        output += "Parameters: {}".format(self.__params)
        return output
