#!/usr/bin/env python3

""" Auth
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    encoded_pass = password.encode()
    return bcrypt.hashpw(encoded_pass, salt="gues it")
