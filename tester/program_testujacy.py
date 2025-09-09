import sys
import csv
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QFrame

# Funkcja do wczytywania CSV jako lista
def load_csv(file_path):
    items = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    items.append(row[0])
    except FileNotFoundError:
        print(f"Plik {file_path} nie znaleziony!")
    return items

class TesterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tester Podzespołów")

        # Layout główny poziomy (po lewej: lista podzespołów, po prawej: COM)
        main_layout = QHBoxLayout()

        # --- Lewa część: podzespoły ---
        left_layout = QVBoxLayout()

        # Główny label pokazujący wybrany podzespół i listę
        self.selected_label = QLabel("Brak wybranego podzespołu")
        left_layout.addWidget(self.selected_label)

        # ComboBoxy podzespołów
        self.combo_cond_1f = QComboBox()
        self.combo_cond_1f.addItems(load_csv("cond_1f.csv"))
        left_layout.addWidget(QLabel("Kondensatory 1-fazowe:"))
        left_layout.addWidget(self.combo_cond_1f)

        self.combo_cond_3f = QComboBox()
        self.combo_cond_3f.addItems(load_csv("cond_3f.csv"))
        left_layout.addWidget(QLabel("Kondensatory 3-fazowe:"))
        left_layout.addWidget(self.combo_cond_3f)

        self.combo_ind_1f = QComboBox()
        self.combo_ind_1f.addItems(load_csv("ind_1f.csv"))
        left_layout.addWidget(QLabel("Dławiki 1-fazowe:"))
        left_layout.addWidget(self.combo_ind_1f)

        self.combo_ind_3f = QComboBox()
        self.combo_ind_3f.addItems(load_csv("ind_3f.csv"))
        left_layout.addWidget(QLabel("Dławiki 3-fazowe:"))
        left_layout.addWidget(self.combo_ind_3f)

        # Połączenie sygnałów do wyświetlania wybranego podzespołu
        self.combo_cond_1f.currentTextChanged.connect(lambda text: self.show_selected(text, "Kondensatory 1-fazowe"))
        self.combo_cond_3f.currentTextChanged.connect(lambda text: self.show_selected(text, "Kondensatory 3-fazowe"))
        self.combo_ind_1f.currentTextChanged.connect(lambda text: self.show_selected(text, "Dławiki 1-fazowe"))
        self.combo_ind_3f.currentTextChanged.connect(lambda text: self.show_selected(text, "Dławiki 3-fazowe"))

        # --- Linia pionowa ---
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        # --- Prawa część: porty COM ---
        right_layout = QVBoxLayout()

        self.com_selected_label = QLabel('Wybrano port dla Analizatora sieci: brak')
        right_layout.addWidget(self.com_selected_label)

        self.combo_com = QComboBox()
        # Pobieranie dostępnych portów COM
        self.combo_com.addItem("brak")
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.combo_com.addItems(ports)
        right_layout.addWidget(QLabel("Wybierz port COM:"))
        right_layout.addWidget(self.combo_com)

        self.combo_com.currentTextChanged.connect(self.show_com_selected)

        # Dodanie części do layoutu głównego
        main_layout.addLayout(left_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def show_selected(self, text, list_name):
        if text:
            self.selected_label.setText(f"Wybrano: {text} z listy: {list_name}")
        else:
            self.selected_label.setText("Brak wybranego podzespołu")

    def show_com_selected(self, text):
        if text:
            self.com_selected_label.setText(f'Wybrano port dla Analizatora sieci: {text}')
        else:
            self.com_selected_label.setText('Wybrano port dla Analizatora sieci: brak')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TesterGUI()
    window.show()
    sys.exit(app.exec())
