#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

from typing import (List)
import re


def filter_datum(fields: List[str], redaction: str,
                 msg: str, seperator: str) -> str:
    """
    Obscure personal data by replacing each field with @redaction
    """
    for field in fields:
        msg = re.sub(r'({}=).*?{}'.format(field, seperator),
                     r'\1{}{}'.format(redaction, seperator),
                     msg)
    return msg
