import sys
from PyQt6.QtWidgets import QApplication
from ui import GameVaultWindow
import database

def main():
    database.init_db()
    app = QApplication(sys.argv)
    window = GameVaultWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()