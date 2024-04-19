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
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
