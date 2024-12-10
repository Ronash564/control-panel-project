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
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #3E3E3E;
        border: 1px solid #5A5A5A;
        padding: 5px;
        color: #FFFFFF;
    }
    QPushButton:hover {
        background-color: #4E4E4E;
    }
    QCheckBox {
        color: #FFFFFF;
    }
    QListWidget {
        background-color: #3E3E3E;
        color: #FFFFFF;
        border: 1px solid #5A5A5A;
    }
    QTextEdit {
        background-color: #3E3E3E;
        color: #FFFFFF;
        border: 1px solid #5A5A5A;
    }
    """
