from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QCheckBox,
    QPushButton, QTextEdit, QLabel, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
import database


class GameVaultWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameVault")
        self.setMinimumSize(700, 600)
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(16)
        root.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🎮 GameVault")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        root.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название игры")
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
        form.addRow("Год:", self.year_spin)

        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 10)
        self.rating_spin.setValue(5)
        form.addRow("Рейтинг:", self.rating_spin)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание...")
        self.desc_input.setMaximumHeight(80)
        form.addRow("Описание:", self.desc_input)

        self.fav_check = QCheckBox("В избранном")
        form.addRow("", self.fav_check)

        root.addLayout(form)

        self.preview_label = QLabel("Превью: —")
        self.preview_label.setStyleSheet(
            "color: gray; font-style: italic;"
        )
        root.addWidget(self.preview_label)

        btn_row = QHBoxLayout()

        self.add_btn = QPushButton("➕ Добавить")
        self.add_btn.setFixedHeight(36)
        self.add_btn.setStyleSheet(
            "background:#4CAF50; color:white; border-radius:6px; font-size:14px;"
        )

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setFixedHeight(36)

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.clear_btn)

        root.addLayout(btn_row)

        line = QLabel("─" * 80)
        line.setStyleSheet("color: #ccc;")
        root.addWidget(line)

        table_label = QLabel("Список игр в библиотеке:")
        table_label.setStyleSheet("font-weight: bold;")
        root.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Название", "Жанр", "Год", "Рейтинг", "⭐"]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.verticalHeader().setVisible(False)

        root.addWidget(self.table)

        self.delete_btn = QPushButton("🗑 Удалить выбранную")
        self.delete_btn.setFixedHeight(34)
        self.delete_btn.setStyleSheet(
            "background:#e53935; color:white; border-radius:6px;"
        )

        root.addWidget(self.delete_btn)

        self.add_btn.clicked.connect(self._on_add)
        self.clear_btn.clicked.connect(self._on_clear)
        self.delete_btn.clicked.connect(self._on_delete)

        self.name_input.textChanged.connect(self._update_preview)
        self.genre_box.currentTextChanged.connect(self._update_preview)
        self.rating_spin.valueChanged.connect(self._update_preview)

    def _on_add(self):
        name = self.name_input.text().strip()
        genre = self.genre_box.currentText()
        year = self.year_spin.value()
        rating = self.rating_spin.value()
        desc = self.desc_input.toPlainText().strip()
        fav = self.fav_check.isChecked()

        if not name:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите название игры!"
            )
            return

        if genre == "Выберите жанр":
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите жанр!"
            )
            return

        game_id = database.add_game(
            name,
            genre,
            year,
            rating,
            desc,
            fav
        )

        QMessageBox.information(
            self,
            "Готово",
            f"Игра «{name}» добавлена (ID: {game_id})"
        )

        self._on_clear()
        self._load_table()

    def _on_clear(self):
        self.name_input.clear()
        self.genre_box.setCurrentIndex(0)
        self.year_spin.setValue(2024)
        self.rating_spin.setValue(5)
        self.desc_input.clear()
        self.fav_check.setChecked(False)
        self.preview_label.setText("Превью: —")

    def _on_delete(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите игру для удаления!"
            )
            return

        game_id = int(self.table.item(row, 0).text())
        game_name = self.table.item(row, 1).text()

        confirm = QMessageBox.question(
            self,
            "Удалить?",
            f"Удалить «{game_name}»?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            database.delete_game(game_id)
            self._load_table()

    def _load_table(self):
        games = database.get_all_games()

        self.table.setRowCount(len(games))

        for row_idx, game in enumerate(games):
            self.table.setItem(
                row_idx,
                0,
                QTableWidgetItem(str(game["id"]))
            )

            self.table.setItem(
                row_idx,
                1,
                QTableWidgetItem(game["name"])
            )

            self.table.setItem(
                row_idx,
                2,
                QTableWidgetItem(game["genre"])
            )

            self.table.setItem(
                row_idx,
                3,
                QTableWidgetItem(str(game["year"]))
            )

            self.table.setItem(
                row_idx,
                4,
                QTableWidgetItem(str(game["rating"]))
            )

            fav_item = QTableWidgetItem(
                "⭐" if game["favorite"] else ""
            )

            fav_item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.table.setItem(
                row_idx,
                5,
                fav_item
            )

    def _update_preview(self):
        name = self.name_input.text().strip() or "..."
        genre = self.genre_box.currentText()
        rating = self.rating_spin.value()

        self.preview_label.setText(
            f"Превью: {name} | {genre} | ⭐ {rating}/10"
        )