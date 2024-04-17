#!/usr/bin/env python3

"""Regex-ing: obfuscated personal identifiable data"""

import logging
from typing import (List, Sequence)
import re
import mysql.connector
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """create a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connect to mysql db"""
    return mysql.connector.connect(
        password=getenv('PERSONAL_DATA_DB_PASSWORD', 'root'),
        username=getenv('PERSONAL_DATA_DB_USERNAME', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )


def main() -> None:
    """display user data"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for user in cursor:
        info = ' '.join([f'{key}={val};' for key, val in user.items()])
        logger.info(info)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields
        logging.basicConfig(format=RedactingFormatter.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """obscure values in incoming log records"""
        return filter_datum(self.__fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


if __name__ == "__main__":
    main()
