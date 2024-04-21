#!/usr/bin/env python3


"""Session Authentication With Expiration
"""

from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta
from models.user import User


class SessionExpAuth(SessionAuth):
    """Session Auth Expiration"""

    def __init__(self) -> None:
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """create session with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user_id using session_id"""
        if session_id is None or \
           self.user_id_by_session_id.get(session_id) is None:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')

        session_dict = self.user_id_by_session_id.get(session_id)
        if "created_at" not in session_dict:
            return None
        if (session_dict["created_at"] +
                timedelta(seconds=self.session_duration)) < datetime.now():
            return None

        return self.user_id_by_session_id.get(session_id).get('user_id')
