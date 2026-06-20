from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox
)

class RegisterWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setWindowTitle("Регистрация")
        self.resize(400, 350)

        layout = QVBoxLayout()

        title = QLabel("📝 Регистрация")
        title.setStyleSheet("font-size:20px;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.role = QComboBox()
        self.role.addItem(["teacher", "student"])

        self.register_btn = QPushButton("Создать аккаунт")

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.role)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

        self.register_btn.clicked.connect(self.register)

    def register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните поля")
            return

        success = self.db.register_user(username, password, role)

        if success:
            QMessageBox.information(self, "Успех", "Аккаунт создан")
            self.close()

        else:
            QMessageBox.warning(self, "Ошибка", "Логин уже существует")