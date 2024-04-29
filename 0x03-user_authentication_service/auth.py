#!/usr/bin/env python3

""" Auth
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password, salt="gues it")
