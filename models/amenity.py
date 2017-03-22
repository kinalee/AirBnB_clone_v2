#!/usr/bin/python3
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(*args, **kwargs)
        if len(kwargs) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__()
