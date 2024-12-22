from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
import database
from PyQt5.QtWidgets import QCheckBox

class UserManagerDialog(QDialog):
    def __init__(self, parent=None, user_role="Default"):
        super().__init__(parent)
        self.setWindowTitle("User Management")
        self.setGeometry(400, 200, 500, 400)

        layout = QVBoxLayout(self)

        # Table to show existing users
        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(["Username", "Password", "Allowed Scripts"])
        layout.addWidget(self.user_table)
        self.load_users()

        # Fields to add new user
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")

        self.scripts_input = QLineEdit()
        self.scripts_input.setPlaceholderText("Comma-separated script names")

        self.admin_checkbox = QCheckBox("Grant Admin Role")

        field_layout = QHBoxLayout()
        field_layout.addWidget(self.username_input)
        field_layout.addWidget(self.password_input)
        field_layout.addWidget(self.scripts_input)
        field_layout.addWidget(self.admin_checkbox)

        layout.addLayout(field_layout)

        # Buttons to add, delete, and close
        button_layout = QHBoxLayout()
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

        # Only show the "Add User" button if the role is Admin
        if user_role == "Admin":
            button_layout.addWidget(self.add_user_button)

        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)
        button_layout.addWidget(self.delete_user_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)


    def load_users(self):
        """Load users from the database and display them."""
        users = database.get_all_users()
        self.user_table.setRowCount(0)
        for user in users:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            self.user_table.setItem(row_position, 0, QTableWidgetItem(user['username']))
            self.user_table.setItem(row_position, 1, QTableWidgetItem(user['password']))
            self.user_table.setItem(row_position, 2, QTableWidgetItem(user['allowed_scripts']))

    def add_user(self):
        """Add a new user to the database."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        allowed_scripts = self.scripts_input.text().strip()
        role = "Admin" if self.admin_checkbox.isChecked() else "Default"

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty!")
            return
    
        database.add_user(username, password, allowed_scripts)
        QMessageBox.information(self, "Success", "User added successfully!")
        self.load_users()  # Refresh the user table
    def delete_user(self):
        """Delete the selected user from the database."""
        selected_row = self.user_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No user selected for deletion.")
            return

        username = self.user_table.item(selected_row, 0).text()

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the user '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            database.delete_user(username)
            QMessageBox.information(self, "Success", f"User '{username}' deleted successfully!")
            self.load_users()
