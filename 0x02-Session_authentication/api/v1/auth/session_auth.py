#!/usr/bin/env python3


"""Session Authentication
"""

from api.v1.auth.basic_auth import BasicAuth
from typing import Dict
import uuid


class SessionAuth(BasicAuth):
    """Session Authentication"""
    pass

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get user_id from session"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
