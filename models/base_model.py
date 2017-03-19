#!/usr/bin/python3
import datetime
import uuid
import models
import collections

class BaseModel(dict):
    """The base class for all storage objects in this project"""
    def __init__(self, *args, **kwargs):
        """initialize class object"""
        if len(args) > 0:
            self.__dict__ = args[0]
        elif len(kwargs) > 0:
            for k, v in kwargs:
                self.__dict__[k] = v
        else:
            self.created_at = datetime.datetime.now()
            self.id = str(uuid.uuid4())

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.__dict__

    def __setitem__(self, key, item):
        self.__dict__[str(key)] = item

    def save(self):
        """method to update self"""
        self.updated_at = datetime.datetime.now()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """edit string representation"""
        return "[{}] ({}) {}".format(type(self)
                                     .__name__, self.id, self.__dict__)

    def to_json(self):
        """convert to json"""
        dupe = self.__dict__.copy()
        dupe["created_at"] = str(dupe["created_at"])
        if ("updated_at" in dupe):
            dupe["updated_at"] = str(dupe["updated_at"])
        dupe["__class__"] = type(self).__name__
        return dupe
