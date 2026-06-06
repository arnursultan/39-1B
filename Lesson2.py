# Code #1
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget
#
# app = QApplication(sys.argv)
#
# window = QWidget()
# window.setWindowTitle("Моё первое окно")
# window.resize(400, 300)
#
# window.show()
#
# sys.exit(app.exec())

# Code #2
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setup_ui()
#
#     def setup_ui(self):
#         self.setWindowTitle("PyQt6")
#         self.resize(450, 350)
#
#         self.label = QLabel("Привет", self)
#         self.label.move(50, 50)
#
#         self.button = QPushButton("Нажми", self)
#         self.button.move(50, 100)
#
# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
#
# sys.exit(app.exec())

# Code #3
# from PyQt6.QtWidgets import *
#
# app = QApplication([])
#
# window = QWidget()
#
# layout = QVBoxLayout()
#
# num1 = QLineEdit()
# num2 = QLineEdit()
#
# button = QPushButton("Сложить")
#
# result = QLabel("0")
#
# layout.addWidget(num1)
# layout.addWidget(num2)
# layout.addWidget(button)
# layout.addWidget(result)
#
# window.setLayout(layout)
#
# def calculate():
#     try:
#         a = int(num1.text())
#         b = int(num2.text())
#
#         result.setText(str(a+b))
#     except:
#         result.setText("Ошибка")
#
# button.clicked.connect(calculate)
#
# window.show()
# app.exec()

# Code 4
import sys
from PyQt6.QtWidgets import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.resize(500, 300)

        self.input_name = QLineEdit(self)
        self.input_name.move(50, 50)

        self.button = QPushButton("Поздороваться", self)
        self.button.move(50, 100)

        self.label = QLabel("", self)
        self.label.move(50, 150)
        self.label.resize(300, 30)

        self.button.clicked.connect(self.say_hello)

    def say_hello(self):
        name = self.input_name.text()

        if name:
            self.label.setText(f"Привет, {name}!")
        else:
            self.label.setText("Введите имя")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
