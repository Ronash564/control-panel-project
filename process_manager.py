# process_manager.py
from PyQt5.QtCore import QProcess

class ScriptRunner:
    def __init__(self, stdout_callback, stderr_callback, finished_callback):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(lambda: stdout_callback(self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')))
        self.process.readyReadStandardError.connect(lambda: stderr_callback(self.process.readAllStandardError().data().decode('utf-8', errors='ignore')))
        self.process.finished.connect(finished_callback)

    def start_script(self, script_path):
        """Start a script given its path."""
        self.process.start("python", [script_path])

    def stop_script(self):
        """Stop the running script."""
        if self.process.state() == QProcess.Running:
            self.process.kill()

