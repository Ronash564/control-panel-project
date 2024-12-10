# database.py
import sqlite3

DB_FILE = 'scripts.db'

def initialize_database():
    """Initialize the database and create the 'scripts' table if it doesn't exist."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            path TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

def get_all_scripts():
    """Retrieve all scripts from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT name, path, description FROM scripts")
    scripts = cursor.fetchall()
    connection.close()
    return [{"name": script[0], "path": script[1], "description": script[2]} for script in scripts]

def add_script(name, path, description):
    """Add a new script to the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO scripts (name, path, description) VALUES (?, ?, ?)",
        (name, path, description)
    )
    connection.commit()
    connection.close()

def update_script(name, new_name, path, description):
    """Update an existing script in the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE scripts SET name = ?, path = ?, description = ? WHERE name = ?",
        (new_name, path, description, name)
    )
    connection.commit()
    connection.close()
