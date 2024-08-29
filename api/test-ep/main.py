import sys
import os
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../../')))

from rds import db, queries

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _context):
    name, err = parse_body(event)
    if err is not None:
        return format_response(err)

    conn, err = get_db_connection()
    if err is not None:
        return format_response(err)

    user, err = queries.get_user(conn, name)
    if err is not None:
        return format_response(build_response(404, json.dumps({"error": err})))

    return format_response(build_response(200, json.dumps({"user": user})))

def parse_body(event):
    err = None
    name = None

    try:
        body = json.loads(event['body'])
        name = body.get('name')
        if name is None:
            raise json.JSONDecodeError("The 'name' field is missing", event['body'], 0)
    except json.JSONDecodeError as e:
        err = build_response(400, json.dumps({"error": e.msg}))

    return name, err

def get_db_connection():
    err = None
    conn = None

    try:
        conn = db.get_db()
        if conn is None:
            raise Exception("Database connection could not be established.")

        logger.info("Database connection established.")

    except Exception as e:
        logger.error(f"Error in database operations: {str(e)}")
        err = build_response(500, json.dumps({"error": str(e)}))

    return conn, err

def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "body": body
    }

def format_response(response):
    # Define headers
    headers = {
        "Content-Type": "application/json"
    }

    # Combine the headers with the response
    formatted_response = {
        **response,
        "headers": headers
    }

    # Return the final response as a dictionary (not a JSON string)
    return formatted_response
