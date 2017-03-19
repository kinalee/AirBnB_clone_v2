#!/usr/bin/python3
from models import *


class Review(BaseModel):
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(args[0], kwargs)
        else:
            super().__init__()
