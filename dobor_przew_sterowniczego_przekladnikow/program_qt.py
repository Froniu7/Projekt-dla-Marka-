import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parametry sieci")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Górny pasek przycisków
        top_button_layout = QHBoxLayout()
        for i in range(1, 6):
            button = QPushButton(f"Przycisk {i}")
            top_button_layout.addWidget(button)
        layout.addLayout(top_button_layout)

        # Pole: moc w sieci
        self.power_label = QLabel("Podaj wartosc mocy wystepujacej w sieci:\n(mozesz podac wartosc zamowiona badz wartosc max wystepujaca))")
        self.power_input = QLineEdit()
        layout.addWidget(self.power_label)
        layout.addWidget(self.power_input)

        # Pole: wybór przekładnika
        self.ct_label = QLabel("Wybierz przekładnik:")
        self.ct_combo = QComboBox()
        self.ct_combo.addItems(["100/5", "200/5", "400/5"])  # przykładowe dane
        layout.addWidget(self.ct_label)
        layout.addWidget(self.ct_combo)

        # Pole: wybór przewodu
        self.cable_label = QLabel("Wybierz przewod:")
        self.cable_combo = QComboBox()
        self.cable_combo.addItems(["YKY 3x2.5", "YKY 3x4", "YKY 3x6"])  # przykładowe dane
        layout.addWidget(self.cable_label)
        layout.addWidget(self.cable_combo)

        # Pole: długość przewodu
        self.length_label = QLabel("Podaj dlugosc przewodu kablowego ( zmienna typu float ):")
        self.length_input = QLineEdit()
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
