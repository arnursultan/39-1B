import sys
import sqlite3

from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget
)

db = sqlite3.connect("students.db")
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course INTEGER,
        debt INTEGER,
        reason TEXT
    )   
""")
db.commit()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База должников")
        self.resize(700, 700)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Добавить студента"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Курс")

        self.debt_input = QLineEdit()
        self.debt_input.setPlaceholderText("Долг")

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("Причина долга")

        self.add_btn = QPushButton("Добавить")

        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.course_input)
        layout.addWidget(self.debt_input)
        layout.addWidget(self.reason_input)
        layout.addWidget(self.add_btn)

        layout.addWidget(QLabel("Поиск по имени"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите имя")

        self.search_btn = QPushButton("Найти")

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)

        layout.addWidget(QLabel("Изменить долг"))

        self.update_name = QLineEdit()
        self.update_name.setPlaceholderText("Имя")

        self.new_debt = QLineEdit()
        self.new_debt.setPlaceholderText("Новый долг")

        self.update_btn = QPushButton("Изменить долг")

        layout.addWidget(self.update_name)
        layout.addWidget(self.new_debt)
        layout.addWidget(self.update_btn)

        layout.addWidget(QLabel("Удалить студента"))

        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("Имя")

        self.delete_btn = QPushButton("Удалить")

        layout.addWidget(self.delete_input)
        layout.addWidget(self.delete_btn)

        layout.addWidget(QLabel("Список студентов"))

        self.list_widget = QListWidget()

        self.refresh_btn = QPushButton("Обновить список")

        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_student)
        self.search_btn.clicked.connect(self.search_student)
        self.update_btn.clicked.connect(self.update_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.refresh_btn.clicked.connect(self.load_students)

        self.load_students()

    def add_student(self):
        cursor.execute("""
        INSERT INTO students ( 
            name, 
            age, 
            course, 
            debt, 
            reason
        )
        VALUES ( ?, ?, ?, ?, ? )
        """, (
            self.name_input.text(),
            self.age_input.text(),
            self.course_input.text(),
            self.debt_input.text(),
            self.reason_input.text()
        ))
        db.commit()

        self.name_input.clear()
        self.age_input.clear()
        self.course_input.clear()
        self.debt_input.clear()
        self.reason_input.clear()

        self.load_students()
