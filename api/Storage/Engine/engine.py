#!/usr/bin/python3
"""Engine - Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from ..storage import Base
from os import getenv


class Engine:
    """Set up a connection to a database"""

    __session = None
    __engine = None

    def __init__(self):
        """intialize the Engine"""
        # setup connection to MySQL
        TICKET_MYSQL_USER = getenv('TICKET_MYSQL_USER')
        TICKET_MYSQL_PWD = getenv('TICKET_MYSQL_PWD')
        TICKET_MYSQL_HOST = getenv('TICKET_MYSQL_HOST')
        TICKET_MYSQL_DB = getenv('TICKET_MYSQL_DB')
        TICKET_ENV = getenv('TICKET_ENV')
        exec_db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            TICKET_MYSQL_USER,
                                            TICKET_MYSQL_PWD,
                                            TICKET_MYSQL_HOST,
                                            TICKET_MYSQL_DB
                                                )
        self.__engine = create_engine(exec_db, pool_pre_ping=True)
        if TICKET_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

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
            create table in database
        """
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self) -> None:
        """
            Closing the session
        """
        self.reload()
        self.__session.close()
