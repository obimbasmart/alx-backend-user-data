#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

from typing import (List)
import re


def filter_datum(fields: List, redaction: str,
                 msg: str, seperator: str) -> str:
    """
    Obscure personal data

    Args:
        @fields: list representing all fields to obfuscate
        @redaction: what the field will be obfuscated with
        @msg: log line
        @seperator: character separating all fields in the log line
    """
    for field in fields:
        msg = re.sub(r'({}=).*?{}'.format(field, seperator),
                     r'\1{}{}'.format(redaction, seperator),
                     msg)
    return msg
