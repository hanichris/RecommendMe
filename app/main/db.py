#!/usr/bin/python3
"""Create a database connection.

Any operations and queries are made through the connection,
which is closed after the fact. The connection is tied to
the request being made.
"""
import sqlite3
import click
from flask import current_app, g


def get_db():
    """Creates a database resource, if it doesn't exist.

    The resource is cached in `g.db`.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exception=None):
    """Deallocates the database resource, if it exists."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


