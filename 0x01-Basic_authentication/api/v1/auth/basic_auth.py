#!/usr/bin/env python3

"""Basic Auth
"""

from .auth import Auth
import base64
from models.user import User
from typing import TypeVar
import hashlib


class BasicAuth(Auth):
    """Basic authentication"""

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        auth_header = self.authorization_header(request)
        auth_header_value = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            auth_header_value)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """return Base64 of auth header"""

        if (authorization_header is None or
            not isinstance(authorization_header, str)
                or not authorization_header.startswith("Basic ")):

            return None
        return authorization_header.split("Basic", 1)[1].strip()

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """return Base64 decode"""
        if (not base64_authorization_header or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            return base64.b64decode(base64_authorization_header) \
                .decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """return user email and password"""
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)
                or ":" not in decoded_base64_authorization_header):

            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """return user instance"""
        if (user_email is None or
            not isinstance(user_email, str) or
            user_pwd is None or
                not isinstance(user_pwd, str)):

            return None

        if not User.search({"email": user_email}):
            return None

        user = User.search({"email": user_email})[0]
        if user.password != hashlib.sha256(user_pwd.encode()) \
                .hexdigest().lower():
            return None
        return user
