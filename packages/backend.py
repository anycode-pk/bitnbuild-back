from packages import app
from flask import render_template, request, redirect, url_for
from flask import g
import os
import sqlite3
from dataclasses import dataclass
import logging
DATABASE_DIR = 'databases/'
DATABASE_NAME = 'app.db'
DATABASE_SCHEMA = 'app.sql'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("packages", "")

# https://www.geeksforgeeks.org/how-to-build-a-web-app-using-flask-and-sqlite-in-python/

# w formie komentarz


def get_db() -> sqlite3.Connection:
    """
    Retrieves the SQLite database connection.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        sqlite3.Error: If there is an issue connecting to the database.

    Usage:
        Use this function to obtain a connection to the SQLite database for executing queries.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            f'{ROOT_DIR}{DATABASE_DIR}{DATABASE_NAME}')
    return db


def get_cursor() -> sqlite3.Cursor:
    """
    Retrieves a cursor object connected to the database.

    Returns:
        sqlite3.Cursor: A cursor object linked to the database.

    Raises:
        RuntimeError: If the application context is not available.
        sqlite3.Error: If there is an issue connecting to the database or creating a cursor.

    Usage:
        Use this function to obtain a cursor for executing SQL queries on the database.
    """
    return get_db().cursor()


def init_db():
    """
    Initializes the database by running the SQL schema script if the database is empty or if changes were made to ksiazki.sql.

    Note:
        This function should be run only when necessary, such as when the database is empty or when changes have been made to the database schema.

    Raises:
        RuntimeError: If the application context is not available.
        sqlite3.Error: If there is an issue executing the SQL script or committing the changes to the database.

    Usage:
        Call this function to ensure the database is set up with the latest schema.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource(f'{ROOT_DIR}{DATABASE_DIR}{DATABASE_SCHEMA}', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def make_dicts(cursor, row):
    """
    Convert a database row into a dictionary with column names as keys.

    Args:
        cursor (sqlite3.Cursor): The cursor object representing the database connection.
        row (tuple): A database row to be converted into a dictionary.

    Returns:
        dict: A dictionary with column names as keys and corresponding values from the row.

    Usage:
        This function is typically used as the `row_factory` when fetching data from the database to obtain results as dictionaries.
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


@app.route('/')
def index():
    """
    Renders the main page displaying information about books and their authors.

    Returns:
        render_template: Renders the 'base.html' template with the book and author data.

    Usage:
        Access this route to view the main page with information about books and their authors.
    """
    cur = get_cursor()
    return 'Default Site'


@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection when the application context is torn down.

    Args:
        exception (Exception): An exception that might have occurred during the application context tear down.

    Usage:
        This function is automatically called by Flask when the application context is torn down.
        It ensures that the database connection is properly closed to prevent resource leaks.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
