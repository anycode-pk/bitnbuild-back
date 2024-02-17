from packages import app
from flask import request
from flask import g
import os
import sqlite3
from flask import jsonify
from dateutil import parser
import random
import time
from flask_cors import cross_origin

DATABASE_DIR = 'databases/'
DATABASE_NAME = 'app.db'
DATABASE_SCHEMA = 'app.sql'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("packages", "")


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
@cross_origin()
def index():
    """
    Renders the main page displaying information about books and their authors.

    Returns:
        render_template: Renders the 'base.html' template with the book and author data.

    Usage:
        Access this route to view the main page with information about books and their authors.
    """
    init_db()
    return 'Default Site'


@app.route("/modules", methods=["GET", "POST"])
@cross_origin()
def modules():
    cur = get_cursor()
    db = get_db()
    if request.method == "POST":
        data = request.json
        title = data['title']
        image_url = data['image_url']
        description = data['description']
        cur.execute("INSERT INTO modules (module_title, module_image_url, module_description) VALUES (?, ?, ?)",
                    (title, image_url, description))
        db.commit()
        cur.execute('SELECT * FROM modules WHERE module_title = ?', (title,))
        module = cur.fetchone()
        return jsonify({"id": module[0], "response": 200})
    elif request.method == "GET":
        cur.execute("SELECT * FROM modules")
        modules = cur.fetchall()
        modules = [{"id": module[0], "title": module[1], "image_url": module[2], "description": module[3]} for module in modules]
        # modules = [module[0] for module in modules]
        return jsonify(modules)


@app.route("/modules/<module_id>", methods=["GET", "DELETE", "PUT"])
@cross_origin()
def get_module(module_id):
    cur = get_cursor()
    db = get_db()
    if request.method == "GET":
        cur.execute("SELECT * FROM modules WHERE module_id = ?", (module_id,))
        module = cur.fetchone()
        if module is None:
            return jsonify({})
        return jsonify({"id": module[0], "title": module[1], "image_url": module[2], "description": module[3]})
    elif request.method == "DELETE":
        cur.execute("DELETE FROM modules WHERE module_id = ?", (module_id,))
        db.commit()
        return jsonify({"response": 200})
    elif request.method == "PUT":
        data = request.json
        title = data['title']
        image_url = data['image_url']
        description = data['description']
        cur.execute("UPDATE modules SET module_title = ?, module_image_url = ?, module_description = ? WHERE module_id = ?",
                    (title, image_url, description, module_id))
        db.commit()
    return jsonify({"response": 200})


@app.route("/events/<module_id>", methods=["GET", "POST"])
@cross_origin()
def events(module_id):
    cur = get_cursor()
    db = get_db()
    if request.method == "POST":
        data = request.json
        fk_module_id = int(module_id)
        event_date = data['date']
        event_title = data['title']
        event_image_url = data['image_url']
        event_description = data['description']
        cur.execute("INSERT INTO event (fk_module_id, event_date, event_title, event_image_url, event_description) VALUES (?, ?, ?, ?, ?)",
                    (fk_module_id, event_date, event_title, event_image_url, event_description))
        db.commit()
        cur.execute('SELECT * FROM event WHERE event_title = ?',
                    (event_title,))
        event = cur.fetchone()
        return jsonify({"id": event[0], "response": 200})
    elif request.method == "GET":
        cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
        events = cur.fetchall()
        events = [event[0] for event in events]
        return jsonify(events)


@app.route("/event/<event_id>", methods=["GET", "DELETE", "PUT"])
@cross_origin()
def get_event(event_id):
    cur = get_cursor()
    db = get_db()
    if request.method == "GET":
        cur.execute("SELECT * FROM event WHERE event_id = ?", (event_id,))
        event = cur.fetchone()
        if event is None:
            return jsonify({})
        return jsonify({"id": event[0], "module_id": event[1], "date": event[2], "title": event[3], "image_url": event[4], "description": event[5]})
    elif request.method == "DELETE":
        cur.execute("DELETE FROM event WHERE event_id = ?", (event_id,))
        db.commit()
        return jsonify({"response": 200})
    elif request.method == "PUT":
        data = request.json
        event_date = data['date']
        event_title = data['title']
        event_image_url = data['image_url']
        event_description = data['description']
        cur.execute("UPDATE event SET event_date = ?, event_title = ?, event_image_url = ?, event_description = ? WHERE event_id = ?",
                    (event_date, event_title, event_image_url, event_description, event_id))
        db.commit()
        return jsonify({"response": 200})


def convert_date(event):
    temp = event[2].split("-")
    if len(temp[0]) < 4:
        temp[0] = "0" * (4 - len(temp[0])) + temp[0]
    if len(temp[1]) < 2:
        temp[1] = "0" + temp[1]
    if len(temp[2]) < 2:
        temp[2] = "0" + temp[2]
    temp = "-".join(temp)
    return parser.parse(temp, yearfirst=True)


@app.route("/timeline/<module_id>", methods=["GET"])
@cross_origin()
def event_timeline(module_id):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify({"events": []})
    events = sorted(events, key=convert_date)
    events = [{"id": event[0], "module_id": event[1], "date": event[2], "title": event[3], "image_url": event[4], "description": event[5]} for event in events]
    return jsonify(events)


@app.route("/game/image-name/<module_id>/<number_of_events>", methods=["GET"])
@cross_origin()
def image_name_game(module_id, number_of_events):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify({[]})
    events = random.sample(events, int(number_of_events))
    events = [{"title": event[3], "image_url": event[4]} for event in events]
    return jsonify(events)


@app.route("/game/higher-lower/<module_id>", methods=["GET"])
@cross_origin()
def higher_lower(module_id):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify([])
    random.seed(time.time())
    events = random.sample(events, 2)
    events = sorted(events, key=convert_date)
    events = [{"date": event[2], "title": event[3], "image_url": event[4]} for event in events]
    return jsonify(events)


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
