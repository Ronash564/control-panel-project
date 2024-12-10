# utils.py

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt



def update_script_status(item, status):
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
