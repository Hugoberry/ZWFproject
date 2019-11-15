import json
from importlib import import_module
import os


class Settings(object):
    def __init__(self):
        self.attributes = {}
        self.setmodule('settings.default_settings')

    def __getitem__(self, opt_name):
        if opt_name not in self:
            return None
        return self.attributes[opt_name]

    def __contains__(self, name):
        return name in self.attributes

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getbool(self, name, default=False):
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ("True", "true"):
                return True
            if got in ("False", "false"):
                return False
            raise ValueError("Supported values for boolean settings "
                             "are 0/1, True/False, '0'/'1', "
                             "'True'/'False' and 'true'/'false'")

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getlist(self, name, default=None):
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(',')
        return list(value)

    def getdict(self, name, default=None):
        value = self.get(name, default or {})
        if isinstance(value, str):
            value = json.loads(value)
        return dict(value)

    def setmodule(self, module):
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def set(self, name, value):
        self.attributes[name] = value


def from_settings(settings=None):
    return Settings() if not settings else settings
