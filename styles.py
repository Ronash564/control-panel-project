# styles.py
print("styles.py is being imported")


def get_light_mode_stylesheet():
    return """
    QWidget {
        background-color: #FFFFFF;
        color: #000000;
    }
    QPushButton {
        background-color: #E0E0E0;
        border: 1px solid #A0A0A0;
        padding: 5px;
        color: #000000;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    }
    QCheckBox {
        color: #000000;
    }
    QListWidget {
        background-color: #F5F5F5;
        color: #000000;
        border: 1px solid #A0A0A0;
    }
    QTextEdit {
        background-color: #F5F5F5;
        color: #000000;
        border: 1px solid #A0A0A0;
    }
    """

def get_dark_mode_stylesheet():
    return """
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLineEdit, QTextEdit {
            background-color: #3c3f41;
            color: #ffffff;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLabel {
            color: #ffffff;
        }
    """

