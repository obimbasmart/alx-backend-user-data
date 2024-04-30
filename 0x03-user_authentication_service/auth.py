#!/usr/bin/env python3

""" Auth
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password.encode("utf-8"),
                         salt=bcrypt.gensalt())


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
            return self._db.add_user(email, password)
        return None
