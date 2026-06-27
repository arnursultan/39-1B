from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QMessageBox,
    QPushButton
)

from PyQt6.QtCore import QPropertyAnimation

from register_window import RegisterWindow
from dashboard_window import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setWindowTitle("Backend Login")
        self.resize(400, 300)

        self.init_ui()
        self.animate()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🔐 Backend Login")
        title.setStyleSheet("font-size:22px;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Войти")
        self.register_btn = QPushButton("Регистрация")

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.open_register)

    def animate(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")

        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def login(self):
        username = self.username.text()
        password = self.password.text()

        user = self.db.login_user(username, password)

        if user:
            self.dashboard = DashboardWindow(self.db, user)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_register(self):
        self.register = RegisterWindow(self.db)
        self.register.show()
