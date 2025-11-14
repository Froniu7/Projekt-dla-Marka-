# csv_files = [
#             "dlawiki1fazowe_dobre.csv",
#             "dlawiki1fazowe_zle.csv",
#             "dlawiki3fazowe_dobre.csv",
#             "dlawiki3fazowe_zle.csv",
#             "kondensatory1fazowe_dobre.csv",
#             "kondensatory1fazowe_zle.csv",
#             "kondensatory3fazowe_dobre.csv",
#             "kondensatory3fazowe_zle.csv"
#         ]

import sys
import csv
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import QTimer, Qt


class CsvTab(QWidget):
    """Zakładka wyświetlająca zawartość pliku CSV i umożliwiająca usuwanie oraz automatyczne odświeżanie."""
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file
        self.last_modified = None

        layout = QVBoxLayout()

        # Tabela
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Przycisk "Usuń zaznaczony wiersz"
        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Usuń zaznaczony wiersz")
        self.delete_button.clicked.connect(self.delete_selected_row)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Wczytanie danych po uruchomieniu
        self.load_csv()
        self.table.cellClicked.connect(self.highlight_selected_row)

        # Timer do monitorowania zmian
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_file_update)
        self.timer.start(1000)  # co 1 sek.

    def load_csv(self):
        """Wczytuje dane z pliku CSV do tabeli (bez kolumny Lp.)."""
        try:
            with open(self.csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if not rows:
                return

            headers = rows[0]
            data = rows[1:]

            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(data))

            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    item.setFont(QFont("Arial", 10))
                    self.table.setItem(row_index, col_index, item)

            self.table.resizeColumnsToContents()
            self.last_modified = os.path.getmtime(self.csv_file)

        except FileNotFoundError:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["Błąd"])
            self.table.setItem(0, 0, QTableWidgetItem(f"Nie znaleziono pliku: {self.csv_file}"))

    def delete_selected_row(self):
        """Usuwa zaznaczony wiersz i zapisuje zmiany do pliku CSV."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        self.table.removeRow(selected_row)
        self.save_csv()

    def save_csv(self):
        """Zapisuje aktualny stan tabeli z powrotem do pliku CSV (bez kolumny Lp.)."""
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()

        headers = [self.table.horizontalHeaderItem(i).text() for i in range(col_count)]

        data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        with open(self.csv_file, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

        self.last_modified = os.path.getmtime(self.csv_file)

    def check_file_update(self):
        """Sprawdza, czy plik został zmodyfikowany z zewnątrz."""
        if not os.path.exists(self.csv_file):
            return
        try:
            current_mtime = os.path.getmtime(self.csv_file)
            if self.last_modified is None:
                self.last_modified = current_mtime
            elif current_mtime != self.last_modified:
                self.load_csv()
        except Exception:
            pass

    def highlight_selected_row(self, row, column):
        """Podświetla cały wiersz, na który kliknięto."""
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.item(r, c).setBackground(Qt.white)

        for c in range(self.table.columnCount()):
            self.table.item(row, c).setBackground(QColor(255, 255, 180))


class CsvViewer(QWidget):
    """Główne okno aplikacji z 8 zakładkami."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Podgląd CSV – autoaktualizacja co 1 sek.")
        self.setGeometry(50, 500, 1400, 500)

        layout = QVBoxLayout()
        tabs = QTabWidget()

        csv_files = [
            "dlawiki1fazowe_dobre.csv",
            "dlawiki1fazowe_zle.csv",
            "dlawiki3fazowe_dobre.csv",
            "dlawiki3fazowe_zle.csv",
            "kondensatory1fazowe_dobre.csv",
            "kondensatory1fazowe_zle.csv",
            "kondensatory3fazowe_dobre.csv",
            "kondensatory3fazowe_zle.csv"
        ]

        for file in csv_files:
            tab = CsvTab(file)
            tabs.addTab(tab, file)

        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())

