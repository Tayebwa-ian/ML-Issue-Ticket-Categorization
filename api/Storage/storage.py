#!/usr/bin/python3"
"""Issue Model - Module"""
from datetime import datetime
from sqlalchemy import String, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Issue(Base):
    """Creating an Issue table in the database
    Args
        id: the id of each issue
        created_at: the time when the issue was submited or reported
        updated_at: last time the issue was modified
        author: who reported the issue
        title: the headline of the issue
        body: detailed description of the issue
        url: the url of the origin of the issue
        prediction: what the model predicted
    """
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    author = Column(String(100), nullable=False)
    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)
    url = Column(String(200))
    prediction = Column(String(20), nullable=False)
    actual_label = Column(String(20))

    def __str__(self) -> str:
        """Return string representation of the object"""
        self_dict = self.__dict__
        rep = "[{}] ({}) {}".format(self.__class__.__name__,
                                    self.id, self_dict)
        return (rep)
