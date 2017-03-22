#!/usr/bin/python3
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name=""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(*args, **kwargs)
        if len(kwargs) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__()
