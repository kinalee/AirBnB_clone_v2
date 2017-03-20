#!/usr/bin/python3
from models import *


class Review(BaseModel):
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super().__init__(*args, **kwargs)
        if len(kwargs) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__()
