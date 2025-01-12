from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QCheckBox
)

import database
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QLineEdit, QMessageBox, QListWidget, QListWidgetItem
)
import database


class UserManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Management")
        self.setModal(True)
        self.resize(600, 400)

        # Main layout
        layout = QVBoxLayout(self)

        # User Table
        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Username", "Password", "Allowed Scripts"])
        layout.addWidget(self.user_table)

        # Input fields for adding a user
        input_layout = QHBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)
        layout.addLayout(input_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.add_user_button = QPushButton("Add User", self)
        self.add_user_button.clicked.connect(self.add_user)
        self.delete_user_button = QPushButton("Delete User", self)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.add_user_button)
        button_layout.addWidget(self.delete_user_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        # Connect double-click event
        self.user_table.cellDoubleClicked.connect(self.handle_cell_double_click)

        # Load users into the table
        self.load_users()

    def load_users(self):
        """Load users from the database and display them in the table."""
        self.user_table.setRowCount(0)  # Clear existing rows
        users = database.get_all_users()  # Fetch all users from the database
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

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty!")
            return

        database.add_user(username, password, "")  # Add user with no scripts initially
        QMessageBox.information(self, "Success", "User added successfully!")
        self.load_users()  # Refresh the table

    def delete_user(self):
        """Delete the selected user from the database."""
        selected_row = self.user_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No user selected for deletion.")
            return

        username = self.user_table.item(selected_row, 0).text()
        confirmation = QMessageBox.question(
            self, "Confirm Deletion", f"Are you sure you want to delete '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            database.delete_user(username)  # Delete user from the database
            QMessageBox.information(self, "Success", f"User '{username}' deleted successfully!")
            self.load_users()  # Refresh the table

    def handle_cell_double_click(self, row, column):
        """Handle double-click events on the table."""
        if column == 2:  # Only handle clicks on the 'Allowed Scripts' column
            username = self.user_table.item(row, 0).text()  # Get the username for the row
            current_scripts = self.user_table.item(row, 2).text() if self.user_table.item(row, 2) else ""

            # Open the ScriptSelectionDialog
            available_scripts = database.get_all_scripts()  # Fetch all available scripts
            selected_scripts = current_scripts.split(",") if current_scripts else []

            dialog = ScriptSelectionDialog([script['name'] for script in available_scripts], selected_scripts, self)
            if dialog.exec_() == QDialog.Accepted:
                # Get the updated scripts and update the table and database
                updated_scripts = dialog.get_selected_scripts()
                self.user_table.setItem(row, 2, QTableWidgetItem(",".join(updated_scripts)))
                database.update_user_scripts(username, ",".join(updated_scripts))  # Save to database


class ScriptSelectionDialog(QDialog):
    def __init__(self, available_scripts, selected_scripts=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Allowed Scripts")
        self.setModal(True)

        self.available_scripts = available_scripts
        self.selected_scripts = selected_scripts or []

        layout = QVBoxLayout(self)

        # Script list with checkboxes
        self.script_list = QListWidget(self)
        for script in self.available_scripts:
            item = QListWidgetItem(script)
            item.setCheckState(
                2 if script in self.selected_scripts else 0
            )  # 2 = Checked, 0 = Unchecked
            self.script_list.addItem(item)
        layout.addWidget(self.script_list)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_selection)
        close_button = QPushButton("Cancel", self)
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def save_selection(self):
        self.selected_scripts = [
            self.script_list.item(i).text()
            for i in range(self.script_list.count())
            if self.script_list.item(i).checkState() == 2
        ]
        self.accept()

    def get_selected_scripts(self):
        return self.selected_scripts


class UserManagement(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.resize(600, 400)

        # Layout and widgets
        layout = QVBoxLayout(self)

        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Username", "Password", "Allowed Scripts"])
        layout.addWidget(self.user_table)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.scripts_input = QLineEdit(self)
        self.scripts_input.setPlaceholderText("Comma-separated scripts")
        self.admin_checkbox = QCheckBox("Grant Admin Role", self)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)
        input_layout.addWidget(self.scripts_input)
        input_layout.addWidget(self.admin_checkbox)
        layout.addLayout(input_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_user_button = QPushButton("Add User", self)
        add_user_button.clicked.connect(self.add_user)
        delete_user_button = QPushButton("Delete User", self)
        delete_user_button.clicked.connect(self.delete_user)
        script_selection_button = QPushButton("Select Scripts", self)
        script_selection_button.clicked.connect(self.open_script_selection_dialog)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(add_user_button)
        button_layout.addWidget(delete_user_button)
        button_layout.addWidget(script_selection_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_users()

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

        try:
            database.add_user(username, password, allowed_scripts)
            QMessageBox.information(self, "Success", "User added successfully!")
            self.load_users()  # Refresh the user table
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

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
            try:
                database.delete_user(username)
                QMessageBox.information(self, "Success", f"User '{username}' deleted successfully!")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))

    def open_script_selection_dialog(self):
        available_scripts = database.get_available_scripts()  # Fetch from database
        selected_scripts = self.scripts_input.text().split(",") if self.scripts_input.text() else []

        dialog = ScriptSelectionDialog(available_scripts, selected_scripts, self)
        if dialog.exec_():  # If dialog was accepted
            self.scripts_input.setText(",".join(dialog.get_selected_scripts()))
   
