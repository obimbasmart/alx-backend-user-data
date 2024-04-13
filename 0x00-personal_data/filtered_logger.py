#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

from typing import (List)
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obscure personal data by replacing each field with @redaction
    """
    for field in fields:
        message = re.sub(r'({}=).*?{}'.format(field, separator),
                         r'\1{}{}'.format(redaction, separator),
                         message)
    return message
