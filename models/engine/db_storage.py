#!/usr/bin/python3
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db))

        if os.getenv('HBNB_MYSQL_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        queryList = [User, State, City, Amenity, Place, Review]
        queryDict = {}
        s = self.__session
        for q in queryList:
            for data in s.query(q):
                queryDict[data.__dict__["id"]] = data
        return queryDict

    def new(self, obj):
        s = self.__session
        if obj is not None:
            s.add(obj)

    def save(self):
        s = self.__session
        s.commit()

    def delete(self, obj=None):
        s = self.__session
        if obj is not None:
            s.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
