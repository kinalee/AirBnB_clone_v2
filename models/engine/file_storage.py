#!/usr/bin/python3
import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        self.reload()

    def all(self):
        return self.__objects

    def new(self, obj):
        if obj is not None:
            self.__objects[obj.id] = obj

    def save(self):
        store = {}
        for k in self.__objects.keys():
            store[k] = self.__objects[k].to_json()

        with open(self.__file_path, mode="w", encoding="utf-8") as fd:
            fd.write(json.dumps(store))

    def reload(self):
        try:
            with open(self.__file_path,
                      mode="r+", encoding="utf-8") as fd:
                self.__objects = {}
                temp = json.load(fd)
                for k in temp.keys():
                    cls = temp[k].pop("__class__", None)
                    cr_at = temp[k]["created_at"]
                    cr_at = datetime.strptime(cr_at, "%Y-%m-%d %H:%M:%S.%f")
                    if "updated_at" in k:
                        up_at = temp[k]["updated_at"]
                        up_at = datetime.strptime(up_at, "%Y-%m-%d %H:%M:%S.%f")
                    self.__objects[k] = eval(cls)(**temp[k])
        except Exception as e:
            pass

    def delete(self, obj=None):
        if obj in self.__objects:
            for k, v in self.__objects:
                if v == obj:
                    del self.__objects[k]
