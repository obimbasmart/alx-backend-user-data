#!/usr/bin/env python3


"""Basic Auth Class"""

from flask import request
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
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """--- --- ---"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """--- --- ---"""
        return request
