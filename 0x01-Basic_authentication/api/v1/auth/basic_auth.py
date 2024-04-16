#!/usr/bin/env python3

"""Basic Auth
"""

from .auth import Auth


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
