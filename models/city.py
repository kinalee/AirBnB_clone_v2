#!/usr/bin/python3
import os
from models.base_model import BaseModel, Base
from models.state import State
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(*args, **kwargs)
        if len(kwargs) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__()
