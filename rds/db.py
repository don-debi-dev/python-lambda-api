"""
Connects to the MySQL database using environment variables and returns the connection.
"""
import logging
import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Class picks up values for DB connection from .env file
    """
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.max_connections = 3
        self.max_idle_conns = 1

def get_db():
    """
    Connects to the MySQL database using environment variables and returns the connection.
    """
    try:
        settings = get_settings()
        return get_db_from_settings(settings)
    except Exception as e:
        logging.error(f"Error getting env variables: {str(e)}")
        return None

def get_db_from_info(host, user, password, db_name):
    """
    Connects to the MySQL database using provided parameters and returns the connection.
    """
    settings = Settings()
    settings.db_host = host
    settings.db_user = user
    settings.db_password = password
    settings.db_name = db_name
    return get_db_from_settings(settings)

def get_db_from_settings(settings):
    """
    Connects to the MySQL database using the given settings and returns the connection.
    """
    try:
        conn = mysql.connector.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name
        )

        if conn.is_connected():
            logging.info(f"Connected to MySQL Database at {settings.db_host}")
            return conn
    except Error as e:
        logging.error(f"Error connecting to DB: {str(e)}")
        return None

def get_settings():
    """
    Loads settings from environment variables.
    """
    return Settings()

# Example usage:
if __name__ == "__main__":
    connection = get_db()
    if connection:
        logging.info("Database connection successful.")
        # Don't forget to close the connection
        connection.close()
    else:
        logging.error("Failed to connect to the database.")
