"""
    This file contains the code to connect to the application's database
"""

import sqlite3

import click
from flask import current_app, g

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Define a command line command that calls init_db
@click.command('init-db')
def init_db_command():
    """ Clear the existing data and create new tables. """
    init_db()
    click.echo('Initialized the database')

def get_db():
    if 'db' not in g:
        # connection does not already exist. Create new
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    # Close connection if it exists
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    # Tell flask to run close_db when cleaning up
    app.teardown_appcontext(close_db)
    # Add a new command that can be caleld with the flask command
    app.cli.add_command(init_db_command)