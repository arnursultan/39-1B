import sys

from PyQt6.QtWidgets import QApplication

from database import Database
from login_window import LoginWindow
from styles import STYLE

app = QApplication(sys.argv)

app.setStyleSheet(STYLE)

db = Database()

window = LoginWindow(db)

window.show()

sys.exit(app.exec())