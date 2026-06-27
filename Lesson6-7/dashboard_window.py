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

from PyQt6.QtCore import (
    QPropertyAnimation
)


class DashboardWindow(QWidget):

    def __init__(self, db, user):
        super().__init__()

        self.db = db
        self.user = user

        self.setWindowTitle(
            "☕ Backend Simulator"
        )

        self.resize(1200, 700)

        self.init_ui()
        self.load_students()
        self.animate()

    def animate(self):
        self.anim = QPropertyAnimation(
            self,
            b"windowOpacity"
        )

        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def init_ui(self):

        layout = QVBoxLayout()

        self.user_label = QLabel(
            f"Пользователь: {self.user[1]} | Роль: {self.user[3]}"
        )

        layout.addWidget(self.user_label)

        top = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Имя студента"
        )

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Поиск"
        )

        top.addWidget(self.name_input)
        top.addWidget(self.search_input)

        layout.addLayout(top)

        btns = QHBoxLayout()

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
            "☕",
            "🔥",
            "🐛",
            "⭐ XP",
            "🏆 LVL",
            "💰"
        ])

        layout.addWidget(self.table)

        self.progress = QProgressBar()
        self.progress.setValue(100)

        layout.addWidget(self.progress)

        game_buttons = QHBoxLayout()

        self.coffee_btn = QPushButton(
            "☕ Выпить кофе"
        )

        self.code_btn = QPushButton(
            "💻 Написать код"
        )

        self.homework_btn = QPushButton(
            "📚 Проверить ДЗ"
        )

        self.offer_btn = QPushButton(
            "💰 Получить оффер"
        )

        game_buttons.addWidget(
            self.coffee_btn
        )

        game_buttons.addWidget(
            self.code_btn
        )

        game_buttons.addWidget(
            self.homework_btn
        )

        game_buttons.addWidget(
            self.offer_btn
        )

        layout.addLayout(
            game_buttons
        )

        self.setLayout(layout)

        self.add_btn.clicked.connect(
            self.add_student
        )

        self.delete_btn.clicked.connect(
            self.delete_student
        )

        self.search_btn.clicked.connect(
            self.search_student
        )

        self.refresh_btn.clicked.connect(
            self.load_students
        )

        self.coffee_btn.clicked.connect(
            self.drink_coffee
        )

        self.code_btn.clicked.connect(
            self.write_code
        )

        self.homework_btn.clicked.connect(
            self.check_homework
        )

        self.offer_btn.clicked.connect(
            self.get_offer
        )

        if self.user[3] == "student":
            self.add_btn.hide()
            self.delete_btn.hide()

    def selected_id(self):

        row = self.table.currentRow()

        if row == -1:
            return None

        return int(
            self.table.item(row, 0).text()
        )

    def load_students(self):

        students = self.db.get_students()

        self.table.setRowCount(
            len(students)
        )

        for row, student in enumerate(students):

            for col, value in enumerate(student):
                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )

    def add_student(self):

        name = self.name_input.text()

        if not name:
            return

        self.db.add_student(name)

        self.name_input.clear()

        self.load_students()

    def delete_student(self):

        student_id = self.selected_id()

        if not student_id:
            return

        self.db.delete_student(
            student_id
        )

        self.load_students()

    def search_student(self):

        text = self.search_input.text()

        students = self.db.search_student(
            text
        )

        self.table.setRowCount(
            len(students)
        )

        for row, student in enumerate(students):

            for col, value in enumerate(student):
                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )

    def drink_coffee(self):

        student_id = self.selected_id()

        if not student_id:
            return

        student = self.db.get_student(
            student_id
        )

        coffee = student[2] + 1
        motivation = min(
            student[3] + 10,
            100
        )

        self.db.update_student(
            student_id,
            "coffee",
            coffee
        )

        self.db.update_student(
            student_id,
            "motivation",
            motivation
        )

        self.progress.setValue(
            motivation
        )

        self.load_students()

    def check_homework(self):

        student_id = self.selected_id()

        if not student_id:
            return

        student = self.db.get_student(
            student_id
        )

        motivation = max(
            student[3] - 20,
            0
        )

        self.db.update_student(
            student_id,
            "motivation",
            motivation
        )

        self.progress.setValue(
            motivation
        )

        self.load_students()

    def write_code(self):

        student_id = self.selected_id()

        if not student_id:
            return

        student = self.db.get_student(
            student_id
        )

        bugs = student[4]
        xp = student[5]
        level = student[6]

        event = random.randint(
            1,
            3
        )

        if event == 1:
            bugs = max(
                bugs - 1,
                0
            )
            text = "Код заработал"

        elif event == 2:
            bugs += 5
            text = "Исправил баг и создал ещё 5"

        else:
            text = "StackOverflow не помог"

        xp += random.randint(
            10,
            25
        )

        if xp >= 100:
            level += 1
            xp = 0

        self.db.update_student(
            student_id,
            "bugs",
            bugs
        )

        self.db.update_student(
            student_id,
            "xp",
            xp
        )

        self.db.update_student(
            student_id,
            "level",
            level
        )

        QMessageBox.information(
            self,
            "Результат",
            text
        )

        self.load_students()

    def get_offer(self):

        student_id = self.selected_id()

        if not student_id:
            return

        salary = random.choice([
            500,
            800,
            1200,
            2500,
            4000
        ])

        self.db.update_student(
            student_id,
            "salary",
            salary
        )

        QMessageBox.information(
            self,
            "Оффер",
            f"Получен оффер на {salary}$"
        )

        self.load_students()