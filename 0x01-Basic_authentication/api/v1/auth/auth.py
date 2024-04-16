#!/usr/bin/env python3


"""Basic Auth Class"""

from flask import request
import re
from typing import (
    List,
    TypeVar
)


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """--- --- --- """
        if not path or not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"

        for ex_path in excluded_paths:
            pattern = re.escape(ex_path).replace(r'\*', r'.*')
            if re.match(pattern, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """--- --- ---"""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """--- --- ---"""
        return None
