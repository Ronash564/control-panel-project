# dialog_manager.py
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QFileDialog

class ScriptDialog(QDialog):
    def __init__(self, script_data=None, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Edit Script" if script_data else "Add New Script")
        self.setGeometry(400, 200, 300, 200)
        
        # Layout
        layout = QFormLayout(self)
        
        # Fields
        self.name_input = QLineEdit(self)
        self.path_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        
        layout.addRow("Script Name:", self.name_input)
        layout.addRow("Script Path:", self.path_input)
        layout.addRow("Description:", self.description_input)
        
        # Browse button to select file path
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_path)
        layout.addRow(browse_button)
        
        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        # Pre-fill with existing data if editing
        if script_data:
            self.name_input.setText(script_data['name'])
            self.path_input.setText(script_data['path'])
            self.description_input.setText(script_data['description'])
        
    def browse_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Script File", "", "Python Files (*.py)")
        if file_path:
            self.path_input.setText(file_path)
    
    def get_script_data(self):
        return {
            "name": self.name_input.text(),
            "path": self.path_input.text(),
            "description": self.description_input.text()
        }
