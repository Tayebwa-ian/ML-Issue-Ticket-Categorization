#!/usr/bin/python3
"""create a unique Storage instance for the application"""
from .Engine.engine import Engine
from .storage import Issue
from os import getenv



# load from database
db = getenv('TICKET_MYSQL_DB')
if db:
    storage = Engine()
    storage.reload() # create all tables in the database
