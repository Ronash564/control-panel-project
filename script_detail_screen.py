# script_detail_screen.py

print("script_detail_screen.py is being imported")

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QApplication

class ScriptDetailScreen(QWidget):
    def __init__(self, parent=None):  # Allow `parent` to be optional
        super().__init__(parent)
        self.init_script_detail_screen()

    def init_script_detail_screen(self):
        """Initialize the script detail screen for displaying script information."""
        detail_layout = QVBoxLayout(self)
        
        # Script detail view
        self.script_detail_view = QTextEdit()
        self.script_detail_view.setReadOnly(True)
        detail_layout.addWidget(self.script_detail_view)

        # Run and Stop buttons in the top right
        top_right_buttons_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("background-color: green; color: white;")
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: red; color: white;")

        top_right_buttons_layout.addWidget(self.run_button)
        top_right_buttons_layout.addWidget(self.stop_button)
        detail_layout.addLayout(top_right_buttons_layout)

        # Mini log viewer for script output in the bottom right
        self.mini_log_viewer = QTextEdit()
        self.mini_log_viewer.setReadOnly(True)
        detail_layout.addWidget(self.mini_log_viewer)

        # Back button to return to the main screen
        back_button = QPushButton("Back to Main Screen")
        detail_layout.addWidget(back_button)

# This block allows the script to run independently for testing
if __name__ == "__main__":
    print("Testing ScriptDetailScreen as a standalone script")
    app = QApplication([])
    window = ScriptDetailScreen()  # Create an instance without a parent
    window.show()
    app.exec_()
