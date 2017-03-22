#!/usr/bin/python3
import os
import models
import datetime
import uuid
import collections
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        id = Column(String(60), nullable=False,
                    primary_key=True, unique=True)
        created_at = Column(DateTime, default=datetime.datetime.now(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.datetime.now(),
                            nullable=False)

    """The base class for all storage objects in this project"""
    def __init__(self, *args, **kwargs):
        """initialize class object"""
        if len(args) > 0:
            raise Exception("BaseModel was passed invalid args."
                            "Only create objects with **dictionaries")
        if len(kwargs) > 0:
            self.__dict__ = kwargs
        if 'id' not in self:
            self['id'] = str(uuid.uuid4())
        if 'created_at' not in self:
            self['created_at'] = datetime.datetime.now()

    def __missing__(self, key):
        """missing builtin implementation for missing class keys"""
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        """does object have key"""
        return str(key) in self.__dict__

    def __setitem__(self, key, item):
        """set Model item dictionary style"""
        self.__dict__[str(key)] = item

    def __getitem__(self, key):
        """get Model item dictionary style"""
        return self.__dict__[str(key)]

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
