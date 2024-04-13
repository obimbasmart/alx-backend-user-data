#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

import logging
from typing import (List, Sequence)
import re

PII_FIELDS = ('email', 'phone', 'ssn', 'name', 'ip')


def filter_datum(fields: Sequence[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obscure personal data by replacing each field with @redaction
    """
    for field in fields:
        message = re.sub(r'({}=).*?{}'.format(field, separator),
                         r'\1{}{}'.format(redaction, separator),
                         message)
    return message


def get_logger() -> logging.Logger:
    """create a logger"""
    logger = logging.Logger("user_data", logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields
        logging.basicConfig(format=RedactingFormatter.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """obscure values in incoming log records"""
        return filter_datum(self.__fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)
