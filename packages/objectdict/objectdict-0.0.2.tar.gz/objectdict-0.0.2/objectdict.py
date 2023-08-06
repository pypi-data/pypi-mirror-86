# -*- coding: utf-8 -*-

import json


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def from_json(self, json_data, json_loads=json.loads):
        return self.update(json_loads(json_data))
