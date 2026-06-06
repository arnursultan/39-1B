from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QCheckBox,
    QPushButton, QTextEdit, QLabel, QMessageBox,
    QHBoxLayout
)


class GameVaultWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameVault — Добавить игру")
        self.setMinimumWidth(500)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setSpacing(16)
        root_layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🎮 Новая игра")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        root_layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Например: Cyberpunk 2077")
        form.addRow("Название:", self.name_input)

        self.genre_box = QComboBox()
        self.genre_box.addItems([
            "Выберите жанр", "RPG", "Action", "Strategy",
            "Simulation", "Horror", "Indie", "Sport"
        ])
        form.addRow("Жанр:", self.genre_box)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(1970, 2030)
        self.year_spin.setValue(2024)
        form.addRow("Год выпуска:", self.year_spin)

        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 10)
        self.rating_spin.setValue(5)
        form.addRow("Рейтинг (1–10):", self.rating_spin)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Краткое описание игры...")
        self.desc_input.setMaximumHeight(100)
        form.addRow("Описание:", self.desc_input)

        self.fav_check = QCheckBox("Добавить в избранное")
        form.addRow("", self.fav_check)

        root_layout.addLayout(form)

        self.preview_label = QLabel("Превью: —")
        self.preview_label.setStyleSheet("color: gray; font-style: italic;")
        root_layout.addWidget(self.preview_label)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить игру")
        self.add_btn.setFixedHeight(38)
        self.add_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 6px; font-size: 14px;"
        )

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setFixedHeight(38)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        root_layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self._on_add)
        self.clear_btn.clicked.connect(self._on_clear)

        self.name_input.textChanged.connect(self._update_preview)
        self.genre_box.currentTextChanged.connect(self._update_preview)
        self.rating_spin.valueChanged.connect(self._update_preview)

    def _on_add(self):
        name   = self.name_input.text().strip()
        genre  = self.genre_box.currentText()
        year   = self.year_spin.value()
        rating = self.rating_spin.value()
        desc   = self.desc_input.toPlainText().strip()
        fav    = self.fav_check.isChecked()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название игры!")
            return
        if genre == "Выберите жанр":
            QMessageBox.warning(self, "Ошибка", "Выберите жанр!")
            return

        result = (
            f"✅ Игра добавлена!\n\n"
            f"Название : {name}\n"
            f"Жанр     : {genre}\n"
            f"Год      : {year}\n"
            f"Рейтинг  : {rating}/10\n"
            f"Описание : {desc or '—'}\n"
            f"Избранное: {'⭐ Да' if fav else 'Нет'}"
        )
        QMessageBox.information(self, "GameVault", result)

    def _on_clear(self):
        self.name_input.clear()
        self.genre_box.setCurrentIndex(0)
        self.year_spin.setValue(2024)
        self.rating_spin.setValue(5)
        self.desc_input.clear()
        self.fav_check.setChecked(False)
        self.preview_label.setText("Превью: —")

    def _update_preview(self):
        name   = self.name_input.text().strip() or "..."
        genre  = self.genre_box.currentText()
        rating = self.rating_spin.value()
        self.preview_label.setText(
            f"Превью: {name} | {genre} | ⭐ {rating}/10"
        )