import sqlite3

DB_FILE = 'scripts.db'

def initialize_database():
    """Initialize the database and create the necessary tables."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create scripts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            path TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL,
            allowed_scripts TEXT  -- Comma-separated list of script names
        )
    ''')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Add 'role' column to the users table if it does not exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if "role" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'Default'")
        print("Added 'role' column to users table.")

    connection.commit()
    connection.close()

def add_default_roles():
    """Insert default roles: Admin and Default."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO roles (role_name, allowed_scripts) VALUES (?, ?)", ("Admin", "ALL"))
    cursor.execute("INSERT OR IGNORE INTO roles (role_name, allowed_scripts) VALUES (?, ?)", ("Default", "Script 1,Script 2"))
    connection.commit()
    connection.close()
    print("Default roles 'Admin' and 'Default' added.")

def add_default_admin():
    """Insert a default Admin user."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "admin123", "Admin")
    )
    connection.commit()
    connection.close()
    print("Default Admin user added.")

def get_user(username, password):
    """Retrieve a user with the given username and password."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT username, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        return {"username": user[0], "role": user[1]}  # Return username and role
    return None

def get_allowed_scripts_for_user(role):
    """Retrieve scripts allowed for a specific role."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT allowed_scripts FROM roles WHERE role_name = ?", (role,))
    allowed_scripts = cursor.fetchone()
    connection.close()

    if allowed_scripts and allowed_scripts[0] == "ALL":
        return "ALL"  # Admin role gets access to all scripts
    return allowed_scripts[0].split(",") if allowed_scripts else []

def get_all_scripts():
    """Retrieve all scripts from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT name, path, description FROM scripts")
    scripts = cursor.fetchall()
    connection.close()
    return [{"name": script[0], "path": script[1], "description": script[2]} for script in scripts]

def add_user(username, password, role):
    """Add a new user to the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )
    connection.commit()
    connection.close()
    print(f"User '{username}' added with role '{role}'.")

def get_all_users():
    """Retrieve all users from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    connection.close()
    return [{"username": user[0], "role": user[1]} for user in users]

if __name__ == "__main__":
    initialize_database()  # Create tables if they don't exist
    add_default_roles()    # Add default roles
    add_default_admin()    # Add default admin user
