import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "Ron",
    "password": "Rs123456",  # Replace with your MySQL password
    "database": "control_panel",  # Replace with your database name
}

def get_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Database connection established successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

def initialize_database():
    """Initialize the database and create the necessary tables."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Initializing database...")

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
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        connection.close()

def add_default_roles():
    """Insert default roles: Admin and Default."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Adding default roles...")
        cursor.execute("INSERT IGNORE INTO roles (role_name, allowed_scripts) VALUES (%s, %s)", ("Admin", "ALL"))
        cursor.execute("INSERT IGNORE INTO roles (role_name, allowed_scripts) VALUES (%s, %s)", ("Default", "Script 1,Script 2"))
        connection.commit()
        print("Default roles added successfully.")
    except Exception as e:
        print(f"Error adding default roles: {e}")
    finally:
        connection.close()

def add_default_admin():
    """Insert a default Admin user."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Adding default admin user...")
        cursor.execute(
            "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("admin", "admin123", "Admin")
        )
        connection.commit()
        print("Default Admin user added successfully.")
    except Exception as e:
        print(f"Error adding default admin user: {e}")
    finally:
        connection.close()

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
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        connection.close()

def get_allowed_scripts_for_user(role):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        print(f"Fetching allowed scripts for role: {role}")
        cursor.execute("SELECT allowed_scripts FROM roles WHERE role_name = %s", (role,))
        result = cursor.fetchone()
        print(f"Allowed scripts: {result}")
        if result:
            return result['allowed_scripts'].split(',') if result['allowed_scripts'] != 'ALL' else 'ALL'
        else:
            print(f"Role '{role}' not found in roles table.")
            return []
    except Exception as e:
        print(f"Error fetching allowed scripts: {e}")
        return []
    finally:
        connection.close()

def delete_user(username):
    """Delete a user from the database by username."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(f"Deleting user: {username}")
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        connection.commit()
        print(f"User '{username}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting user: {e}")
    finally:
        connection.close()

def get_all_scripts():
    """Retrieve all scripts from the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        print("Fetching all scripts...")
        cursor.execute("SELECT name, path, description FROM scripts")
        scripts = cursor.fetchall()
        print(f"Fetched scripts: {scripts}")
        return scripts
    except Exception as e:
        print(f"Error fetching scripts: {e}")
        return []
    finally:
        connection.close()

def add_user(username, password, role):
    """Add a new user to the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(f"Adding user: {username} with role: {role}")
        cursor.execute(
            "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        connection.commit()
        print(f"User '{username}' added successfully.")
    except Exception as e:
        print(f"Error adding user: {e}")
    finally:
        connection.close()

def get_all_users():
    """Retrieve all users with their details from the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        print("Fetching all users...")
        query = '''
        SELECT u.username, u.password, r.allowed_scripts 
        FROM users u
        LEFT JOIN roles r ON u.role = r.role_name
        '''
        cursor.execute(query)
        users = cursor.fetchall()
        print(f"Fetched users: {users}")
        return [{"username": user["username"], "password": user["password"], "allowed_scripts": user["allowed_scripts"] or ""} for user in users]
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        connection.close()

def add_script(name, path, description):
    """Add a new script to the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(f"Adding script: {name}")
        cursor.execute(
            "INSERT INTO scripts (name, path, description) VALUES (%s, %s, %s)",
            (name, path, description),
        )
        connection.commit()
        print(f"Script '{name}' added successfully.")
    except mysql.connector.IntegrityError as e:
        print(f"Error: Script '{name}' already exists. {e}")
    except Exception as e:
        print(f"Unexpected error adding script: {e}")
    finally:
        connection.close()

def update_user_scripts(username, allowed_scripts):
    """Update the allowed scripts for a user in the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(f"Updating allowed scripts for user: {username}")
        cursor.execute(
            "UPDATE users SET allowed_scripts = %s WHERE username = %s", (allowed_scripts, username)
        )
        connection.commit()
        print(f"Allowed scripts updated for user: {username}")
    except Exception as e:
        print(f"Error updating user scripts: {e}")
    finally:
        connection.close()

def test_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection successful!")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    print("Testing database connection...")
    test_connection()
    initialize_database()  # Create tables if they don't exist
    add_default_roles()    # Add default roles
    add_default_admin()    # Add default admin user
