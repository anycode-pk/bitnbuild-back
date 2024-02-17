from packages import app
from flask import request, render_template
from flask import g
from flask import request, g, jsonify
from flask_cors import cross_origin
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import os
import sqlite3
from dateutil import parser
import random
import time

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


@app.route('/')
@cross_origin()
def index():
    """
    Renders the index page with the content of the README.md file formatted as HTML.

    Note:
        This function initializes the database by calling `init_db()` and then reads the content of the README.md file.
        It formats the content as Markdown using the `markdown` library with extensions 'fenced_code' and 'codehilite'.
        Additionally, it applies syntax highlighting to code blocks using the 'emacs' style from the `HtmlFormatter` class in the `codehilite` extension.

    Returns:
        str: HTML content of the README.md file with syntax-highlighted code blocks.

    Raises:
        FileNotFoundError: If the README.md file is not found.
        IOError: If there is an issue reading the README.md file.
        RuntimeError: If the application context is not available.

    Usage:
        Navigate to the index page to view the formatted README.md content.
    """
    init_db()
    readme_file = open("README.md", "r", encoding="utf-8")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code", 'codehilite']
    )
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template


@app.route("/modules", methods=["GET", "POST"])
@cross_origin()
def modules():
    """
    Handles GET and POST requests for the '/modules' endpoint.

    Note:
        This function retrieves a cursor from the database using `get_cursor()` and the database connection using `get_db()`.
        For POST requests, it expects JSON data containing 'title', 'image_url', and 'description'.
        It inserts the received data into the 'modules' table and returns the ID of the inserted module.
        For GET requests, it retrieves all modules from the 'modules' table and returns them as JSON objects.

    Returns:
        For POST requests:
            dict: JSON response containing the ID of the inserted module and a success message.
        For GET requests:
            list: JSON response containing a list of dictionaries, each representing a module with 'id', 'title', 'image_url', and 'description' keys.

    Usage:
        - For POST requests, send JSON data with 'title', 'image_url', and 'description' to add a new module.
        - For GET requests, retrieve a list of all modules.
    """
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
        modules = [{"id": module[0], "title": module[1], "image_url": module[2],
                    "description": module[3]} for module in modules]
        return jsonify(modules)


@app.route("/modules/<module_id>", methods=["GET", "DELETE", "PUT"])
@cross_origin()
def get_module(module_id):
    """
    Handles GET, DELETE, and PUT requests for specific module IDs via the '/modules/<module_id>' endpoint.

    Args:
        module_id (str): The ID of the module to retrieve, delete, or update.

    Returns:
        For GET requests:
            dict: JSON response containing details of the module with the specified ID.
        For DELETE requests:
            dict: JSON response indicating successful deletion.
        For PUT requests:
            dict: JSON response indicating successful update.

    Usage:
        - For GET requests, retrieve details of a module by providing its ID.
        - For DELETE requests, delete a module by providing its ID.
        - For PUT requests, update details of a module by providing its ID and JSON data with updated 'title', 'image_url', and 'description'.
    """
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
    """
    Handles GET and POST requests for events associated with a specific module via the '/events/<module_id>' endpoint.

    Args:
        module_id (str): The ID of the module associated with the events.

    Returns:
        For POST requests:
            dict: JSON response containing the ID of the inserted event and a success message.
        For GET requests:
            list: JSON response containing a list of event IDs associated with the specified module.

    Usage:
        - For POST requests, add a new event associated with the specified module by providing JSON data with 'date', 'title', 'image_url', and 'description'.
        - For GET requests, retrieve a list of event IDs associated with the specified module.
    """
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
    """
    Handles GET, DELETE, and PUT requests for specific event IDs via the '/event/<event_id>' endpoint.

    Args:
        event_id (str): The ID of the event to retrieve, delete, or update.

    Returns:
        For GET requests:
            dict: JSON response containing details of the event with the specified ID.
        For DELETE requests:
            dict: JSON response indicating successful deletion.
        For PUT requests:
            dict: JSON response indicating successful update.

    Usage:
        - For GET requests, retrieve details of an event by providing its ID.
        - For DELETE requests, delete an event by providing its ID.
        - For PUT requests, update details of an event by providing its ID and JSON data with updated 'date', 'title', 'image_url', and 'description'.
    """
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
    """
    Converts a date string in ISO format (YYYY-MM-DD) to a datetime object.

    Args:
        event (tuple): A tuple representing an event with a date string at index 2.

    Returns:
        datetime: A datetime object representing the converted date.

    Usage:
        Pass an event tuple containing a date string to convert it to a datetime object.
    """
    temp = event[2].split("-")
    if len(temp) == 1:
        temp[0] = "0" * (4 - len(temp[0])) + temp[0]
        temp.append("01")
        temp.append("01")
    elif len(temp) == 2:
        temp.append("01")
    elif len(temp) == 3:
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
    """
    Retrieves events associated with a specific module ID and returns them sorted by date in ascending order.

    Args:
        module_id (str): The ID of the module to retrieve events for.

    Returns:
        list: JSON response containing a list of dictionaries, each representing an event with 'id', 'module_id', 'date', 'title', 'image_url', and 'description' keys, sorted by date.

    Usage:
        Retrieve events associated with a module by providing its ID.
    """
    cur = get_cursor()
    if module_id == "1":
        cur.execute("SELECT * FROM event")
    else:
        cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify({"events": []})
    events = sorted(events, key=convert_date)
    events = [{"id": event[0], "module_id": event[1], "date": event[2], "title": event[3],
               "image_url": event[4], "description": event[5]} for event in events]
    return jsonify(events)


@app.route("/game/image-name/<module_id>/<number_of_events>", methods=["GET"])
@cross_origin()
def image_name_game(module_id, number_of_events):
    """
    Retrieves a random selection of events' titles and image URLs associated with a specific module ID.

    Args:
        module_id (str): The ID of the module to retrieve events for.
        number_of_events (str): The number of events to retrieve.

    Returns:
        list: JSON response containing a list of dictionaries, each representing an event with 'title' and 'image_url' keys.

    Usage:
        Retrieve a random selection of events' titles and image URLs associated with a module by providing its ID and the desired number of events.
    """
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify({[]})
    events = random.sample(events, int(number_of_events))
    events = [{"title": event[3], "image_url": event[4]} for event in events]
    return jsonify(events)


@app.route("/game/image-date/<module_id>/<number_of_events>", methods=["GET"])
@cross_origin()
def image_date_game(module_id, number_of_events):
    """
    Retrieves a random selection of events' dates and image URLs associated with a specific module ID.

    Args:
        module_id (str): The ID of the module to retrieve events for.
        number_of_events (str): The number of events to retrieve.

    Returns:
        list: JSON response containing a list of dictionaries, each representing an event with 'date' and 'image_url' keys.

    Usage:
        Retrieve a random selection of events' dates and image URLs associated with a module by providing its ID and the desired number of events.
    """
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify({[]})
    events = random.sample(events, int(number_of_events))
    events = [{"date": event[2], "image_url": event[4]} for event in events]
    return jsonify(events)


@app.route("/game/higher-lower/<module_id>", methods=["GET"])
@cross_origin()
def higher_lower(module_id):
    """
    Retrieves two random events associated with a specific module ID for the higher-lower game.

    Args:
        module_id (str): The ID of the module to retrieve events for.

    Returns:
        list: JSON response containing a list of two dictionaries, each representing an event with 'date', 'title', and 'image_url' keys.

    Usage:
        Retrieve two random events associated with a module for the higher-lower game by providing its ID.
    """
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify([])
    random.seed(time.time())
    events = random.sample(events, 2)
    events = sorted(events, key=convert_date)
    events = [{"date": event[2], "title": event[3],
               "image_url": event[4]} for event in events]
    return jsonify(events)


@app.route("/game/chronological/<module_id>/<number_of_events>", methods=["GET"])
@cross_origin()
def chronological(module_id, number_of_events):
    """
    Retrieves a random selection of events associated with a specific module ID and returns them sorted chronologically by date.

    Args:
        module_id (str): The ID of the module to retrieve events for.
        number_of_events (str): The number of events to retrieve.

    Returns:
        list: JSON response containing a list of dictionaries, each representing an event with 'date', 'title', and 'image_url' keys, sorted chronologically by date.

    Usage:
        Retrieve a random selection of events associated with a module and sorted chronologically by date by providing its ID and the desired number of events.
    """
    cur = get_cursor()
    cur.execute(f"SELECT * FROM event WHERE fk_module_id = {module_id}")
    events = cur.fetchall()
    if events is None:
        return jsonify([])
    random.seed(time.time())
    events = random.sample(events, int(number_of_events))
    events = sorted(events, key=convert_date)
    events = [{"date": event[2], "title": event[3],
               "image_url": event[4]} for event in events]
    return jsonify(events)


@app.route("/game/trivia/<module_id>", methods=["GET"])
@cross_origin()
def trivia(module_id):
    """
    Retrieves a random trivia question associated with a specific module ID.

    Args:
        module_id (str): The ID of the module to retrieve trivia questions for.

    Returns:
        dict: JSON response containing a trivia question with 'question', 'answers', and 'correct_answer' keys.

    Usage:
        Retrieve a random trivia question associated with a module by providing its ID.
    """
    cur = get_cursor()
    cur.execute(f"SELECT * FROM questions WHERE fk_module_id = {module_id}")
    questions = cur.fetchall()
    if questions is None:
        return jsonify([])
    random.seed(time.time())
    questions = random.sample(questions, 1)
    answers = questions[3].split("|")
    answers = [answer.strip() for answer in answers]
    questions = {"question": questions[2], "answers": answers,
                 "correct_answer": questions[4].strip()}
    return jsonify(questions)


@app.route("/questions/<module_id>", methods=["GET", "POST"])
@cross_origin()
def questions(module_id):
    """
    Handles GET and POST requests for questions associated with a specific module ID via the '/questions/<module_id>' endpoint.

    Args:
        module_id (str): The ID of the module associated with the questions.

    Returns:
        For POST requests:
            dict: JSON response containing the ID of the inserted question and a success message.
        For GET requests:
            list: JSON response containing a list of question IDs associated with the specified module.

    Usage:
        - For POST requests, add a new question associated with the specified module by providing JSON data with 'question', 'answers', and 'correct_answer'.
        - For GET requests, retrieve a list of question IDs associated with the specified module.
    """
    cur = get_cursor()
    db = get_db()
    if request.method == "POST":
        data = request.json
        fk_module_id = int(module_id)
        question = data['question']
        answers = data['answers']
        answers = "|".join(answers)
        correct_answer = data['correct_answer']
        cur.execute("INSERT INTO questions (fk_module_id, question, answers, correct_answer) VALUES (?, ?, ?, ?, ?)",
                    (fk_module_id, question, answers, correct_answer))
        db.commit()
        cur.execute('SELECT * FROM questions WHERE question = ?',
                    (question,))
        onequestion = cur.fetchone()
        return jsonify({"id": onequestion[0], "response": 200})
    elif request.method == "GET":
        cur.execute(
            f"SELECT * FROM questions WHERE fk_module_id = {module_id}")
        question_list = cur.fetchall()
        question_list = [onequestion[0] for onequestion in question_list]
        return jsonify(events)


@app.route("/question/<question_id>", methods=["GET", "DELETE", "PUT"])
@cross_origin()
def get_question(question_id):
    """
    Handles GET, DELETE, and PUT requests for specific question IDs via the '/question/<question_id>' endpoint.

    Args:
        question_id (str): The ID of the question to retrieve, delete, or update.

    Returns:
        For GET requests:
            dict: JSON response containing details of the question with the specified ID.
        For DELETE requests:
            dict: JSON response indicating successful deletion.
        For PUT requests:
            dict: JSON response indicating successful update.

    Usage:
        - For GET requests, retrieve details of a question by providing its ID.
        - For DELETE requests, delete a question by providing its ID.
        - For PUT requests, update details of a question by providing its ID and JSON data with updated 'question', 'answers', and 'correct_answer'.
    """
    cur = get_cursor()
    db = get_db()
    if request.method == "GET":
        cur.execute(
            "SELECT * FROM questions WHERE question_id = ?", (question_id,))
        onequestion = cur.fetchone()
        if onequestion is None:
            return jsonify({})
        return jsonify({"id": onequestion[0], "module_id": onequestion[1], "question": onequestion[2], "answers": onequestion[3], "correct_answer": onequestion[4]})
    elif request.method == "DELETE":
        cur.execute("DELETE FROM questions WHERE question_id = ?",
                    (question_id,))
        db.commit()
        return jsonify({"response": 200})
    elif request.method == "PUT":
        data = request.json
        question = data['question']
        answers = data['answers']
        correct_answer = data['correct_answer']
        cur.execute("UPDATE questions SET question = ?, answers = ?, correct_answer = ? WHERE question_id = ?",
                    (question, answers, correct_answer))
        db.commit()
        return jsonify({"response": 200})


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
