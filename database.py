from flask import g
import sqlite3
import os

def connect_to_database():
    # Use the Linux-like path format for WSL or Linux
    db_directory = '/mnt/c/Users/Administrator/Desktop/SmartDesk'
    
    # Ensure the directory exists
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)  # Creates the directory if it does not exist

    # Define the absolute path to the database file
    db_path = os.path.join(db_directory, 'crudapplication.db')

    # Connect to the database
    sql = sqlite3.connect(db_path)  # Correctly closed the string and used the path variable
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, 'crudapplication_db'):
        g.crudapplication_db = connect_to_database()
    return g.crudapplication_db
