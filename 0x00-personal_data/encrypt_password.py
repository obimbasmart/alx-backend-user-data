#!/usr/bin/env python3

"""Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
