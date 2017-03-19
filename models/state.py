#!/usr/bin/python3
from models import *


class State(BaseModel):
    name = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            super(State, self).__init__(args[0], kwargs)
        else:
            super().__init__()
