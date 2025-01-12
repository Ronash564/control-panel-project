from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import database
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Login")
        self.setGeometry(400, 200, 300, 150)

        # Layout
        layout = QVBoxLayout()

        # Username and Password Fields
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate_user)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Placeholder for the authenticated user
        self.authenticated_user = None

    def authenticate_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            logging.warning("Empty username or password provided.")
            QMessageBox.warning(self, "Login Failed", "Username and password cannot be empty!")
            return

        logging.info(f"Attempting to authenticate user: {username}")
        try:
            user = database.get_user(username, password)
            logging.debug(f"Database response for user: {user}")  # Check what `get_user` returns
            if user:
                self.authenticated_user = user
                logging.info(f"User authenticated successfully: {self.authenticated_user}")
                self.accept()
            else:
                logging.warning("Invalid credentials provided.")
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            logging.error(f"Unexpected error during authentication: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
