#!/usr/bin/env python3


"""Session Authentication
"""

from api.v1.auth.auth import Auth
from typing import Dict
import uuid
from models.user import User


class SessionAuth(Auth):
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

    def current_user(self, request=None):
        """return user instance base on cookie value"""
        user_id = self.user_id_by_session_id.get(
            request.cookies.get("_my_session_id"))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """delete user session"""
        if request is None or self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
