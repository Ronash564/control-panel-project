# main_screen.py
print("main_screen.py is being imported")
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("MainScreen instance is being initialized")
        self.init_main_screen()

    def init_main_screen(self):
        """Initialize the main screen with script list and controls."""
        main_layout = QVBoxLayout(self)
        
        # Script List
        self.script_list = QListWidget()
        main_layout.addWidget(self.script_list)

        # Log viewer for script output
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        main_layout.addWidget(self.log_viewer)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Add, Edit, and Show Script buttons
        self.add_button = QPushButton("Add New Script")
        self.add_button.setIcon(QIcon("icons/plus.png"))  # Path to your plus icon
        self.add_button.setIconSize(QSize(24, 24))  # Set icon size
        button_layout.addWidget(self.add_button)
       
        
        self.edit_button = QPushButton("Edit Selected Script")
        button_layout.addWidget(self.edit_button)

        self.show_button = QPushButton("Show Script")
        button_layout.addWidget(self.show_button)

        main_layout.addLayout(button_layout)

    def load_scripts(self, database):
        """Load scripts from the database and add them to the list."""
        scripts = database.get_all_scripts()
        for script_data in scripts:
            self.add_script_to_list(script_data)

    def add_script_to_list(self, script_data):
        item = QListWidgetItem(script_data['name'])
        item.setData(Qt.UserRole, script_data)
        item.setData(Qt.UserRole + 1, "idle")  # Initial status is 'idle'
        self.script_list.addItem(item)
