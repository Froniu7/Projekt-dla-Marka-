import sys, os, json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
)
from funkcje import generuj_plik_docx, generuj_grafiki_do_schematu, generowanie_schematu_jednokreskowego, generowanie_schematu_podlaczenia

class CableSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wybór przekrojów przewodów")
        #sterowniki
        self.sterowniki = ["Novar", "Tense"]

        # Dane - przekroje przewodów
        self.cable_cross_sections = [
            "1.5 mm²", "2.5 mm²", "4 mm²", "6 mm²", "10 mm²", "16 mm²", "25 mm²"
        ]
        self.control_cross_sections = [
            "0.22 mm²", "0.34 mm²", "0.5 mm²", "0.75 mm²", "1 mm²", "1.5 mm²"
        ]

        self.przekladniki = ["100/5, okno 36, moc 1 VA", "100/5, okno 24, moc 1 VA", "50/5, okno 24, moc 1 VA"]

        self.rodzaj_zabezpieczenia = ["typ S Cx A", "wkładki gG", "brak zab. głównego zewnętrznego"]

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

    def zapisz_wybor_do_json(self, sciezka_pliku="wynik.json"):
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
    app = QApplication(sys.argv)
    window = CableSelector()
    window.show()
    sys.exit(app.exec())
