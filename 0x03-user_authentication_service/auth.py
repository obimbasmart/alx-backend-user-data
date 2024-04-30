#!/usr/bin/env python3

""" Auth
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password.encode("utf-8"),
                         salt=bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound as err:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        return None

    def valid_login(self, email: str, password: str) -> bool:
        """validate login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as err:
            return False
        else:
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        return False

    def create_session(self, email: str) -> str:
        """create a user session"""
        user = self._db.find_user_by(email=email)
        if user is None:
            return None
        session_id = _generate_uuid()
        user.session_id = session_id
        return session_id
