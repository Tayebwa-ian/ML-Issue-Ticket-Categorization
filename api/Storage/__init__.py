#!/usr/bin/python3
"""create a unique Storage instance for the application"""
from .Engine.engine import Engine
from .storage import Issue


# load from database
storage = Engine()
db = storage.get_db()
storage.reload() # create all tables in the database
