#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from uuid import uuid4
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user"""
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        user.session_id = uuid4().hex
        user.reset_token = '112'
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find user by attribute"""
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user"""
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        for attr, value in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError()
            setattr(user, attr, value)
