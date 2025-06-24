import sys, os, json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
)
from funkcje import generuj_plik_docx, generuj_grafiki_do_schematu, generowanie_schematu_jednokreskowego, generowanie_schematu_podlaczenia

import sys, os, argparse

nazwa_pliku_json = ""

def argumenty():
    parser = argparse.ArgumentParser(description="Generator pliku JSON z wyborem parametrów.")
    parser.add_argument("output", nargs="?", help="Nazwa wyjściowego pliku JSON (np. dane.json)")
    args = parser.parse_args()
    return args.output  # może być None!


def get_sciezka_do_katalogu(nazwa_katalogu):
    # Jeśli to aplikacja .exe spakowana PyInstallerem
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Normalne uruchomienie z .py
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Wejdź poziom wyżej
    nadrzedny_katalog = os.path.dirname(base_path)

    # Dodaj nową końcówkę ścieżki
    sciezka_docelowa = os.path.join(nadrzedny_katalog, nazwa_katalogu)

    return sciezka_docelowa

def wczytaj_csv(nazwa_pliku, start_from=0, ile_kolumn=1, separator=" | "):
    import csv
    katalog_dane = get_sciezka_do_katalogu("dane")
    sciezka = os.path.join(katalog_dane, nazwa_pliku)
    dane = []
    with open(sciezka, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < start_from:
                continue  # pomiń nagłówki
            if not row or all(cell.strip() == "" for cell in row):
                continue  # pomiń puste wiersze

            # Uzupełnij brakujące kolumny pustymi stringami, jeśli ich brakuje
            row += [""] * (ile_kolumn - len(row))

            # Połącz kolumny w jeden string
            row_str = separator.join(row[:ile_kolumn])

            dane.append(row_str)
    return dane

class CableSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wybór przekrojów przewodów")
        #sterowniki
        self.sterowniki = wczytaj_csv("sterowniki.csv", 1)

        # Dane - przekroje przewodów
        self.cable_cross_sections = wczytaj_csv("Przekroje_zasilajace.csv", 1, ile_kolumn=1)

        self.control_cross_sections = wczytaj_csv("przewody_sterownicze.csv", 1, ile_kolumn=3)

        self.przekladniki = wczytaj_csv("przekladniki.csv", 1, ile_kolumn=4)

        self.rodzaj_zabezpieczenia = wczytaj_csv("Rodzaje zabezpieczenia głównego zew.csv", 1)

        self.zabezpiecznia_gG = ["2A", "6A", "10A"]

        # Tworzenie widżetów
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Sterownik:"))

        self.sterownik_combo = QComboBox()
        self.sterownik_combo.addItem("-- wybierz --")
        self.sterownik_combo.addItems(self.sterowniki)
        self.sterownik_combo.setStyleSheet("color: red;")
        self.sterownik_combo.currentIndexChanged.connect(lambda i: self.update_combo_style(self.sterownik_combo, i))
        layout.addWidget(self.sterownik_combo)

        layout.addWidget(QLabel("Przekrój przewodu kablowego:"))

        self.cable_combo = QComboBox()
        self.cable_combo.addItem("-- wybierz --")
        self.cable_combo.addItems(self.cable_cross_sections)
        self.cable_combo.setStyleSheet("color: red;")
        self.cable_combo.currentIndexChanged.connect(lambda i: self.update_combo_style(self.cable_combo, i))
        layout.addWidget(self.cable_combo)

        layout.addWidget(QLabel("Przekrój przewodu sterowniczego:"))
        self.control_combo = QComboBox()
        self.control_combo.addItem("-- wybierz --")
        self.control_combo.addItems(self.control_cross_sections)
        self.control_combo.setStyleSheet("color: red;")
        self.control_combo.currentIndexChanged.connect(lambda i: self.update_combo_style(self.control_combo, i))
        layout.addWidget(self.control_combo)

        layout.addWidget(QLabel("Przekładniki:"))
        self.przekladniki_combo = QComboBox()
        self.przekladniki_combo.addItem("-- wybierz --")
        self.przekladniki_combo.addItems(self.przekladniki)
        self.przekladniki_combo.setStyleSheet("color: red;")
        self.przekladniki_combo.currentIndexChanged.connect(lambda i: self.update_combo_style(self.przekladniki_combo, i))
        layout.addWidget(self.przekladniki_combo)

        layout.addWidget(QLabel("Rodzaj zabezpieczenia:"))
        self.zab_rodzaj_combo = QComboBox()
        self.zab_rodzaj_combo.addItem("-- wybierz --")
        self.zab_rodzaj_combo.addItems(self.rodzaj_zabezpieczenia)
        self.zab_rodzaj_combo.setStyleSheet("color: red;")
        self.zab_rodzaj_combo.currentIndexChanged.connect(
            lambda i: self.update_combo_style(self.zab_rodzaj_combo, i))
        layout.addWidget(self.zab_rodzaj_combo)

        layout.addWidget(QLabel("Zabezpieczenia:"))
        self.zabezpieczenie_combo = QComboBox()
        self.zabezpieczenie_combo.addItem("-- wybierz --")
        self.zabezpieczenie_combo.addItems(self.zabezpiecznia_gG)
        self.zabezpieczenie_combo.setStyleSheet("color: red;")
        self.zabezpieczenie_combo.currentIndexChanged.connect(lambda i: self.update_combo_style(self.zabezpieczenie_combo, i))
        layout.addWidget(self.zabezpieczenie_combo)

        # 🔘 Przycisk "Generuj"
        self.generate_button = QPushButton("Generuj")
        self.generate_button.clicked.connect(self.show_selected_values)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def update_combo_style(self, combo, index):
        if index == 0:
            combo.setStyleSheet("color: red;")
        else:
            combo.setStyleSheet("color: green;")

 # 🧠 Funkcja uruchamiana po kliknięciu "Generuj"
    def show_selected_values(self):
        cable = self.cable_combo.currentText()
        control = self.control_combo.currentText()
        control = "7x"+control
        przekladnik = self.przekladniki_combo.currentText()
        zabezpieczenie = self.zabezpieczenie_combo.currentText()
        sterownik = self.sterownik_combo.currentText()

        rodzaj_zab=self.zab_rodzaj_combo.currentText()

        print("=== Wybrane opcje ===")
        print(f"Przewód kablowy: {cable}")
        print(f"Przewód sterowniczy: {control}")
        print(f"Przekładnik: {przekladnik}")
        print(f"Rodzaj zabezpieczenia {rodzaj_zab}")
        print(f"Zabezpieczenie: {zabezpieczenie}")
        print("=====================")

        generuj_grafiki_do_schematu(cable=cable,control=control,przekladnik=przekladnik,zabezpieczenie=zabezpieczenie)
        generowanie_schematu_jednokreskowego(rodzaj_zab)
        generowanie_schematu_podlaczenia(rodzaj_zab,sterownik)
        generuj_plik_docx("schemat_jednokreskowy.png","schemat_ogolny.png","dokument_schematy.docx", przekladnik, cable, control, rodzaj_zab=rodzaj_zab, ampery=zabezpieczenie)
        self.zapisz_wybor_do_json("dane_wejsciowe.json")  # 💾 zapis do json

    def zapisz_wybor_do_json(self, sciezka_pliku=nazwa_pliku_json):
        dane = {
            "przewod_kablowy": self.cable_combo.currentText(),
            "przewod_sterowniczy": "7x" + self.control_combo.currentText(),
            "przekladnik": self.przekladniki_combo.currentText(),
            "rodzaj_zabezpieczenia": self.zab_rodzaj_combo.currentText(),
            "zabezpieczenie": self.zabezpieczenie_combo.currentText(),
            "sterownik": self.sterownik_combo.currentText()
        }

        with open(sciezka_pliku, "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=4, ensure_ascii=False)

        print(f"🔧 Zapisano dane do pliku: {os.path.abspath(sciezka_pliku)}")

if __name__ == "__main__":

    nazwa_pliku_json = argumenty()

    if not nazwa_pliku_json:
        # Tu możesz wygenerować np. nazwę z datą
        print(f"📄 Przekazana nazwa dla pliku json: {nazwa_pliku_json}")
    else:
        print(f"📄 Przekazana nazwa dla pliku json: {nazwa_pliku_json}")

    app = QApplication(sys.argv)
    window = CableSelector()
    window.show()
    sys.exit(app.exec())
