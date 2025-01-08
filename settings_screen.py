from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, 
    QPushButton, QLineEdit, QFileDialog, QGroupBox, QMessageBox, QDialog
)

from PyQt5.QtCore import Qt
from user_manager import UserManagerDialog
from styles import get_light_mode_stylesheet, get_dark_mode_stylesheet  # Import the styles from styles.py

class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        # Main layout
        main_layout = QVBoxLayout(self)

        # Appearance Section
        dark_mode_group = QGroupBox("Appearance")
        dark_mode_layout = QVBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)  # Connect the checkbox
        dark_mode_layout.addWidget(self.dark_mode_checkbox)
        dark_mode_group.setLayout(dark_mode_layout)
        main_layout.addWidget(dark_mode_group)

        # Notifications Section
        notification_group = QGroupBox("Notifications")
        notification_layout = QVBoxLayout()
        notification_layout.addWidget(QLabel("Notification Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        notification_layout.addWidget(self.email_input)
        notification_group.setLayout(notification_layout)
        main_layout.addWidget(notification_group)

        # Script Settings Section
        script_path_group = QGroupBox("Script Settings")
        script_path_layout = QVBoxLayout()
        script_path_layout.addWidget(QLabel("Default Script Path:"))
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select a directory")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        script_path_layout.addLayout(path_layout)
        script_path_group.setLayout(script_path_layout)
        main_layout.addWidget(script_path_group)

        # User Management Section
        user_management_group = QGroupBox("User Management")
        user_management_layout = QVBoxLayout()
        self.add_user_button = QPushButton("Manage Scripts")
        self.add_user_button.clicked.connect(self.open_user_manager)
        user_management_layout.addWidget(self.add_user_button)
        user_management_group.setLayout(user_management_layout)
        main_layout.addWidget(user_management_group)

        # Action Buttons
        action_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_settings)
        action_layout.addWidget(self.save_button)
        action_layout.addWidget(self.reset_button)
        main_layout.addLayout(action_layout)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button)

    def browse_directory(self):
        """Open a file dialog to select a directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.path_input.setText(directory)

    def save_settings(self):
        """Save settings when the save button is clicked."""
        dark_mode = self.dark_mode_checkbox.isChecked()
        email = self.email_input.text()
        script_path = self.path_input.text()

        # Toggle dark mode
        if dark_mode:
            self.parent().parent().setStyleSheet(get_dark_mode_stylesheet())
        else:
            self.parent().parent().setStyleSheet(get_light_mode_stylesheet())

        print(f"Settings saved: Dark Mode = {dark_mode}, Email = {email}, Script Path = {script_path}")

    def toggle_dark_mode(self):
        """Toggle between dark mode and light mode."""
        if self.dark_mode_checkbox.isChecked():
            self.parent().parent().setStyleSheet(get_dark_mode_stylesheet())
            print("Dark mode enabled.")
        else:
            self.parent().parent().setStyleSheet(get_light_mode_stylesheet())
            print("Dark mode disabled.")

    def reset_settings(self):
        """Reset all settings to default."""
        self.dark_mode_checkbox.setChecked(False)
        self.email_input.clear()
        self.path_input.clear()
        print("Settings reset to default.")

    def open_user_manager(self):
        """Open the User Management dialog."""
        dialog = UserManagerDialog(self)
        dialog.exec_()


    def go_back(self):
        """Return to the main screen."""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Assumes main screen is at index 0
