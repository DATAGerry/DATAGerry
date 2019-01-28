import json

class Event:

    def __init__(self, event_type, params=None):
        self.__event_type = event_type
        self.__params = {}
        if params:
            self.__params = params

    @staticmethod
    def create_event(json_repr):
        loaded_json = json.loads(json_repr)
        event_type = "default"
        event_params = {}
        if "type" in loaded_json:
            event_type = loaded_json["type"]
        if "params" in loaded_json:
            event_params = loaded_json["params"]
        return Event(event_type, event_params)

    def get_type(self):
        return self.__event_type

    def get_param(self, key, default=None):
        output = default
        if key in self.__params:
            output = self.__params[key]
        return output

    def json_repr(self):
        output = {}
        output["type"] = self.__event_type
        output["params"] = self.__params
        return json.dumps(output)

    def __str__(self):
        output = "Event {}".format(self.__event_type)
        output += "Parameters: {}".format(self.__params)
        return output
