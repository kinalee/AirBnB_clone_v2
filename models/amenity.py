#!/usr/bin/python3
from models import *


class Amenity(BaseModel):
    name = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(args[0], kwargs)
        else:
            super().__init__()
