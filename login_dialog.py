from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import database

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
        """Check user credentials and validate login."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and Password cannot be empty!")
            return

        user = database.get_user(username, password)  # Check database for user
        if user:
            self.authenticated_user = user['username']
            self.accept()  # Close the dialog with success
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")
