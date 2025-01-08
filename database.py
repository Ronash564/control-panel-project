import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "Ron",
    "password": "Rs123456",  # Replace with your MySQL password
    "database": "control_panel",  # Replace with your database name
}

def get_connection():
    """Create a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def initialize_database():
    """Initialize the database and create the necessary tables."""
    connection = get_connection()
    cursor = connection.cursor()

    # Create scripts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            path TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            role_name VARCHAR(255) UNIQUE NOT NULL,
            allowed_scripts TEXT  -- Comma-separated list of script names
        )
    ''')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL DEFAULT 'Default'
        )
    ''')

    connection.commit()
    connection.close()

def add_default_roles():
    """Insert default roles: Admin and Default."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT IGNORE INTO roles (role_name, allowed_scripts) VALUES (%s, %s)", ("Admin", "ALL"))
    cursor.execute("INSERT IGNORE INTO roles (role_name, allowed_scripts) VALUES (%s, %s)", ("Default", "Script 1,Script 2"))
    connection.commit()
    connection.close()
    print("Default roles 'Admin' and 'Default' added.")

def add_default_admin():
    """Insert a default Admin user."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
        ("admin", "admin123", "Admin")
    )
    connection.commit()
    connection.close()
    print("Default Admin user added.")

def get_user(username, password):
    """Retrieve a user with the given username and password."""
    print(f"Fetching user: {username}")
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        print(f"Fetched user: {user}")
        return user
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        connection.close()


def get_allowed_scripts_for_user(role):
    """Retrieve scripts allowed for a specific role."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT allowed_scripts FROM roles WHERE role_name = %s", (role,))
    allowed_scripts = cursor.fetchone()
    connection.close()

    if allowed_scripts and allowed_scripts[0] == "ALL":
        return "ALL"  # Admin role gets access to all scripts
    return allowed_scripts[0].split(",") if allowed_scripts else []

def delete_user(username):
    """Delete a user from the database by username."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    connection.commit()
    connection.close()
    print(f"User '{username}' deleted from the database.")

def get_all_scripts():
    """Retrieve all scripts from the database."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, path, description FROM scripts")
    scripts = cursor.fetchall()
    connection.close()
    return scripts

def add_user(username, password, role):
    """Add a new user to the database."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role)
    )
    connection.commit()
    connection.close()
    print(f"User '{username}' added with role '{role}'.")

def get_all_users():
    """Retrieve all users with their details from the database."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT u.username, u.password, r.allowed_scripts 
    FROM users u
    LEFT JOIN roles r ON u.role = r.role_name
    '''
    cursor.execute(query)
    users = cursor.fetchall()
    connection.close()

    return [{"username": user["username"], "password": user["password"], "allowed_scripts": user["allowed_scripts"] or ""} for user in users]

def add_script(name, path, description):
    """Add a new script to the database."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO scripts (name, path, description) VALUES (%s, %s, %s)",
            (name, path, description),
        )
        connection.commit()
        print(f"Script '{name}' added successfully.")
    except mysql.connector.IntegrityError as e:
        print(f"Error: Script '{name}' already exists. {e}")
    finally:
        connection.close()

def update_user_scripts(username, allowed_scripts):
    """Update the allowed scripts for a user in the database."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET allowed_scripts = %s WHERE username = %s", (allowed_scripts, username)
    )
    connection.commit()
    connection.close()
def test_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection successful!")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    initialize_database()  # Create tables if they don't exist
    add_default_roles()    # Add default roles
    add_default_admin()    # Add default admin user
