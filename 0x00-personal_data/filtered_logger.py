#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """obscure values in incoming log records"""
        return filter_datum(self.__fields, self.REDACTION,
                            record.getMessage(),
                            self.SEPARATOR
                            )
