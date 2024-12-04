#!/usr/bin/python3"
"""Issue Model - Module"""
from datetime import datetime
from ..Storage import storage
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

    def save(self) -> None:
        """
        Description:
            Update the updated_at field with current date
            and save to JSON file
        """
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self) -> None:
        """delete the current instance from the storage"""
        storage.delete(self)

    def get(self, id):
        """
        Retrieve one object based on id
        Args:
            id: Id of the object
        Return: object based on its ID, or None
        """
        return self.query.get(id)
    
    def all(self):
        """Retrieve all instances of the table"""
        return self.query.all()

    def __str__(self) -> str:
        """Return string representation of the object"""
        self_dict = self.__dict__
        rep = "[{}] ({}) {}".format(self.__class__.__name__,
                                    self.id, self_dict)
        return (rep)
    
    def update(self, id, **kwargs):
        """Update an object in the database
        Args:
            kwargs: a dictionary of fields to update and their new values
        """
        obj = self.get(id)
        if kwargs:
            for field in kwargs.keys():
                if hasattr(obj, field):
                        setattr(obj, field, kwargs[field])
            obj.updated_at = datetime.now()
            storage.save()
        return obj
