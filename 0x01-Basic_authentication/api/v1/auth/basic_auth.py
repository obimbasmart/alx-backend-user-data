#!/usr/bin/env python3

"""Basic Auth
"""

from .auth import Auth
import base64
from binascii import Error as NotBase64Error


class BasicAuth(Auth):
    """Basic authentication"""

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
        """Base64 decode"""
        if (not base64_authorization_header or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            return base64.b64decode(base64_authorization_header) \
                .decode('utf-8')
        except NotBase64Error:
            return None