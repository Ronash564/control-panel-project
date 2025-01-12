# control_panel.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QTextEdit, QDialog, QStackedWidget, QCheckBox, QLabel
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import database
from dialog_manager import ScriptDialog
from process_manager import ScriptRunner
from script_detail_screen import ScriptDetailScreen
from styles import get_light_mode_stylesheet, get_dark_mode_stylesheet  # Import the styles from styles.py
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from login_dialog import LoginDialog
from PyQt5.QtWidgets import QMessageBox
from settings_screen import SettingsScreen
from user_manager import ScriptSelectionDialog
from database import get_connection


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        login_dialog = LoginDialog()
        try:
            if login_dialog.exec_() == QDialog.Accepted:
                self.current_user = login_dialog.authenticated_user
                print(f"Logged in user: {self.current_user}")  # Debugging
                if not self.current_user:
                    raise ValueError("Authenticated user is None or invalid!")
            else:
                print("Login was canceled.")
                sys.exit()
        except Exception as e:
            print(f"Error during login or transition: {e}")
            sys.exit()

        
        self.setWindowTitle("Script Control Panel")
        self.setGeometry(300, 100, 800, 600)

        # Main layout with QStackedWidget
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # QStackedWidget to hold multiple screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Initialize screens and add them to the stacked widget
        self.init_main_screen()
        self.init_settings_screen()
        self.init_script_detail_screen()

        # Explicitly set the main screen as the current screen
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))  # Assuming the main screen is the first screen added

        self.setStyleSheet(get_light_mode_stylesheet())

        # ScriptRunner instance for handling script processes
        self.script_runner = ScriptRunner(self.handle_stdout, self.handle_stderr, self.process_finished)

        # Timer for resetting "finished" state to "idle" after 20 seconds
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_script_status)


    def init_main_screen(self):
        """Initialize the main screen with script list and controls."""
        main_screen = QWidget()
        main_layout = QVBoxLayout(main_screen)

        # Top-right settings button
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()  # Push the button to the right

        # Add the gear icon
        gear_icon_path = os.path.join(os.path.dirname(__file__), "Icons/gear.png")
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(gear_icon_path))
        self.settings_button.setIconSize(QSize(24, 24))
        self.settings_button.setFlat(True)  # Remove button borders
        self.settings_button.clicked.connect(self.open_settings)  # Connect to a method for settings

        top_bar_layout.addWidget(self.settings_button)
        main_layout.addLayout(top_bar_layout)

        # Script List
        self.script_list = QListWidget()
        self.load_scripts()
        main_layout.addWidget(self.script_list)

        # Log viewer for script output
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        main_layout.addWidget(self.log_viewer)

        # Button layout
        button_layout = QHBoxLayout()

        # Add Script Button
        self.add_button = QPushButton("Add New Script")
        self.add_button.clicked.connect(self.add_script)
        button_layout.addWidget(self.add_button)

        # Manage Users Button (Visible only for Admins)
        if self.current_user['role'] == "Admin":
            self.manage_users_button = QPushButton("Manage Users")
            self.manage_users_button.clicked.connect(self.open_user_management)
            button_layout.addWidget(self.manage_users_button)


        # Edit Script Button
        self.edit_button = QPushButton("Edit Selected Script")
        self.edit_button.clicked.connect(self.edit_script)
        button_layout.addWidget(self.edit_button)

        # Show Script Button
        self.show_button = QPushButton("Show Script")
        self.show_button.clicked.connect(lambda: self.open_script_detail_screen(self.script_list.currentItem()))
        button_layout.addWidget(self.show_button)

        main_layout.addLayout(button_layout)

        # Add the main screen to the stacked widget
        self.stacked_widget.addWidget(main_screen)



    def init_script_detail_screen(self):
        """Initialize the script detail screen and add it to the stacked widget."""
        detail_screen = QWidget()
        detail_layout = QVBoxLayout(detail_screen)

        # Script detail view
        self.script_detail_view = QTextEdit()
        self.script_detail_view.setReadOnly(True)
        detail_layout.addWidget(self.script_detail_view)

        # Mini log viewer for script output
        self.mini_log_viewer = QTextEdit()
        self.mini_log_viewer.setReadOnly(True)
        detail_layout.addWidget(self.mini_log_viewer)

        # Back button to return to the main screen
        back_button = QPushButton("Back to Main Screen")
        back_button.clicked.connect(self.show_main_screen)
        detail_layout.addWidget(back_button)

        # Add the script detail screen to the stacked widget
        self.script_detail_screen = detail_screen
        self.stacked_widget.addWidget(self.script_detail_screen)


    def load_scripts(self):
        try:
            print(f"Loading scripts for user: {self.current_user}")  # Debugging
            allowed_scripts = database.get_allowed_scripts_for_user(self.current_user["role"])
            print(f"Allowed scripts: {allowed_scripts}")  # Debugging
            ...
        except KeyError as e:
            print(f"KeyError: {e}")
            QMessageBox.critical(self, "Error", "User data is incomplete or invalid.")
            sys.exit()
        except Exception as e:
            print(f"Unexpected error: {e}")
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
            sys.exit()

    
    def add_script_to_list(self, script_data):
        item = QListWidgetItem(script_data['name'])
        item.setData(Qt.UserRole, script_data)
        item.setData(Qt.UserRole + 1, "idle")  # Initial status is 'idle'
        self.update_script_status(item, "idle")
        self.script_list.addItem(item)
    
    def open_user_management(self):
        """Open the User Management dialog."""
        from user_manager import UserManagerDialog  # Ensure the correct class is imported
        dialog = UserManagerDialog(self)  # Initialize the UserManagerDialog
        dialog.exec_()  # Display the dialog



    def open_settings(self):
        """Open the Settings dialog."""
        QMessageBox.information(self, "Settings", "Settings functionality coming soon!")

    def add_script(self):
        dialog = ScriptDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            script_data = dialog.get_script_data()
            database.add_script(script_data['name'], script_data['path'], script_data['description'])
            self.add_script_to_list(script_data)

    def edit_script(self):
        selected_item = self.script_list.currentItem()
        if selected_item:
            script_data = selected_item.data(Qt.UserRole)
            dialog = ScriptDialog(script_data, self)
            if dialog.exec_() == QDialog.Accepted:
                updated_script_data = dialog.get_script_data()
                database.update_script(
                    script_data['name'],
                    updated_script_data['name'],
                    updated_script_data['path'],
                    updated_script_data['description']
                )
                selected_item.setText(updated_script_data['name'])
                selected_item.setData(Qt.UserRole, updated_script_data)

    def open_script_detail_screen(self, item):
        """Switch to the script detail screen and display details for the selected script."""
        if item:
            script_data = item.data(Qt.UserRole)
            # Clear and display script details
            self.script_detail_view.setText(f"Script Name: {script_data['name']}\n"
                                            f"Path: {script_data['path']}\n"
                                            f"Description: {script_data['description']}")
            self.mini_log_viewer.clear()
            print("Navigating to Script Detail Screen")
            self.stacked_widget.setCurrentWidget(self.script_detail_screen)  # Correctly point to the script detail screen
        if not item:
            QMessageBox.warning(self, "No Script Selected", "Please select a script to view its details.")
            return



    def show_main_screen(self):
        """Switch back to the main screen."""
        self.stacked_widget.setCurrentIndex(0)

    

    # Define the missing `run_script` method
    def run_script(self):
        """Run the currently selected script and display output in the mini log viewer."""
        selected_item = self.script_list.currentItem()
        if selected_item:
            script_data = selected_item.data(Qt.UserRole)
            self.mini_log_viewer.clear()  # Clear mini log viewer before starting
            self.update_script_status(selected_item, "running")
            self.script_runner.start_script(script_data['path'])

    # Define the `stop_script` method
    def stop_script(self):
        """Stop the currently running script."""
        self.script_runner.stop_script()
        self.update_script_status(self.script_list.currentItem(), "error")
        self.mini_log_viewer.append("Script stopped.")

    # Other methods like `handle_stdout`, `handle_stderr`, etc.
    def handle_stdout(self, output):
        """Handle standard output from the running script."""
        self.mini_log_viewer.append(output)  # Display in the mini log viewer

    def handle_stderr(self, error):
        """Handle error output from the running script."""
        self.mini_log_viewer.append(f"ERROR: {error}")
        self.update_script_status(self.script_list.currentItem(), "error")

    def process_finished(self):
        """Update UI when the script finishes."""
        selected_item = self.script_list.currentItem()
        self.mini_log_viewer.append("Script finished.")
        self.update_script_status(selected_item, "finished")
        self.reset_timer.start(20000)  # Set timer for 20 seconds to reset status to idle

    def update_script_status(self, item, status):
        """Update the item's display based on its status."""
        item.setData(Qt.UserRole + 1, status)
        if status == "running":
            item.setBackground(QColor("lightgreen"))  # Green for running
        elif status == "error":
            item.setBackground(QColor("yellow"))  # Yellow for error
        elif status == "finished":
            item.setBackground(QColor("lightblue"))  # Blue for finished
        elif status == "idle":
            item.setBackground(QColor("white"))  # White for idle

    def reset_script_status(self):
        """Reset script status to idle after the 20-second timer."""
        selected_item = self.script_list.currentItem()
        if selected_item and selected_item.data(Qt.UserRole + 1) == "finished":
            self.update_script_status(selected_item, "idle")

    def toggle_dark_mode(self):
        """Toggle between dark mode and light mode based on the checkbox state."""
        if self.dark_mode_toggle.isChecked():
            self.setStyleSheet(get_dark_mode_stylesheet())
            for i in range(self.script_list.count()):
                item = self.script_list.item(i)
                item.setForeground(QColor("white"))
        else:
            self.setStyleSheet(get_light_mode_stylesheet())
            for i in range(self.script_list.count()):
                item = self.script_list.item(i)
                item.setForeground(QColor("black"))
    def init_settings_screen(self):
        """Initialize the settings screen and add it to the stacked widget."""
        self.settings_screen = SettingsScreen(self.stacked_widget)
        self.settings_screen.setStyleSheet(self.styleSheet())  # Apply global styles
        self.stacked_widget.addWidget(self.settings_screen)


    def open_settings(self):
        """Switch to the settings screen."""
        print("Navigating to Settings Screen")
        self.stacked_widget.setCurrentWidget(self.settings_screen) 
    
    def get_available_scripts(self):
        """Fetch a list of all available scripts."""
        return [script['name'] for script in database.get_all_scripts()]





app = QApplication(sys.argv)
window = ControlPanel()
window.show()
sys.exit(app.exec_())
