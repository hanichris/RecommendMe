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

    The resource is cached in `g.db`. Returns a connection
    object to the database.
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


def init_db():
    """Initialize the database.

    First, makes a connection to the database. With this
    connection, execute the `schema.sql` to generate the
    required tables.
    """
    db = get_db()
    with current_app.open_resource('main/schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables.

    `init-db` command line command calls the `init_db` function.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Registers functions with the app instance.

    `init_db_command` and `close_db` functions are registered
    with the app instance in this way due to use of factory
    function. Registration makes the functions available to
    the instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
