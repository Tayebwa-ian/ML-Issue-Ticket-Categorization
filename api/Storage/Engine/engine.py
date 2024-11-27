#!/usr/bin/python3
"""Engine - Module"""
from flask_sqlalchemy import SQLAlchemy
from app import app
from Storage.storage import Issue, Base


class Engine:
    """Set up a connection to a database"""

    __session = None
    __db = None

    def __init__(self):
        """intialize the Engine"""
        # setup connection to sqllite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predict.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def new(self, obj):
        """
            Creating new instance in db storage
        """
        self.__session.add(obj)

    def save(self):
        """
            save to the db storage
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete obj from db storage
        """
        if obj:
            self.__session.delete(obj)
        self.save()

    def reload(self):
        """
            create tables in database
        """
        self.__db = SQLAlchemy(model_class=Base)
        self.__db.init_app(app)
        with app.app_context():
            self.__db.create_all()
        self.__session = self.__db.session

    def get_db(self):
        """Return the database object"""
        return self.__db
