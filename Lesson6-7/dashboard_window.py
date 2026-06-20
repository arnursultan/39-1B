import random

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar
)

from PyQt6.QtCore import QPropertyAnimation

class DashboardWindow(QWidget):
    def __init__(self, db, user):
        super().__init__()

        self.db = db
        self.user = user

        self.setWindowTitle("☕️ Dashboard")
        self.resize(1200, 700)

        self.init_ui()
        self.load_students()
        self.animate()

    def animate(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_label = QLabel(f"Пользователь:{self.user[1]} | Роль:{self.user[3]}")

        layout.addWidget(self.user_label)

        top = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя студента")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск")

        top.addWidget(self.name_input)
        top.addWidget(self.search_input)

        layout.addLayout(top)

        btns = QHBoxLayout

        self.add_btn = QPushButton("➕ Добавить")
        self.delete_btn = QPushButton("❌ Удалить")
        self.search_btn = QPushButton("🔍 Найти")
        self.refresh_btn = QPushButton("🔄 Обновить")

        btns.addWidget(self.add_btn)
        btns.addWidget(self.delete_btn)
        btns.addWidget(self.search_btn)
        btns.addWidget(self.refresh_btn)

        layout.addLayout(btns)

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Имя",
            "☕️",
            "🔥",
            "🐛",
            "⭐️ XP",
            "🏆 LVL",
            "💰"
        ])
