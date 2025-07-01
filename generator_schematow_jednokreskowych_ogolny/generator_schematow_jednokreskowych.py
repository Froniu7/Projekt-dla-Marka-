import sys, os, json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog
)
from funkcje import konwertuj_docx_na_pdf, resource_path_all, generuj_plik_docx, generuj_grafiki_do_schematu, generowanie_schematu_jednokreskowego, generowanie_schematu_podlaczenia

import sys, os, argparse, subprocess

nazwa_pliku_json = ""
wygeneruj_schemat = 0

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


def wczytaj_csv(nazwa_pliku, start_from=0, ile_kolumn=1, separator=" | ", dodatki=None, separatory=None):
    import csv
    import os

    if dodatki is None:
        dodatki = [""] * 10  # domyślnie puste dopiski

    # Jeśli nie podano separatorów, użyj domyślnych: jeden na początek + między kolumnami
    if separatory is None:
        separatory = [""] + [separator] * (ile_kolumn - 1)
    else:
        # Uzupełnij listę do długości ile_kolumn (1 na początek, reszta między kolumnami)
        separatory += [separator] * (ile_kolumn - len(separatory))

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

            # Uzupełnij brakujące kolumny pustymi stringami
            row += [""] * (ile_kolumn - len(row))

            # Dopisz dodatki do kolumn
            kolumny_z_dodatkami = []
            for idx in range(ile_kolumn):
                dopisek = dodatki[idx] if idx < len(dodatki) else ""
                kolumny_z_dodatkami.append(row[idx] + dopisek)

            # Połącz kolumny z indywidualnymi separatorami (z prefixem)
            row_str = separatory[0]  # separator przed pierwszą kolumną
            for idx, wartosc in enumerate(kolumny_z_dodatkami):
                row_str += wartosc
                if idx < ile_kolumn - 1:
                    row_str += separatory[idx + 1]
            dane.append(row_str)

    return dane



class CableSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wybór przekrojów przewodów")
        #sterowniki
        self.sterowniki = wczytaj_csv("sterowniki.csv", 1)

        # Dane - przekroje przewodów
        self.cable_cross_sections = wczytaj_csv("Uzuwane_przewody_kablowe_zasilajace.csv", 1, ile_kolumn=1)

        self.control_cross_sections = wczytaj_csv("przewody_sterownicze.csv", 1, ile_kolumn=3, separatory=[""," "," ",""])

        self.przekladniki = wczytaj_csv("przekladniki.csv", 1, ile_kolumn=4, dodatki=["","","","VA"], separatory=["", " ", "/", " "])

        self.rodzaj_zabezpieczenia = wczytaj_csv("Rodzaje zabezpieczenia głównego zew.csv", 1)

        #self.zabezpiecznia_gG = ["2A", "6A", "10A"]
        self.zabezpiecznia_gG = wczytaj_csv("zabezpieczenia_C_gG.csv", 1, ile_kolumn=1, dodatki=[" A"])

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

        self.generate_button = QPushButton("Podglad")
        self.generate_button.clicked.connect(self.show_pdf)
        layout.addWidget(self.generate_button)

        self.btn_zapisz_png = QPushButton("Zapisz PNG")
        self.btn_zapisz_png.clicked.connect(lambda: self.zapisz_plik("schemat_ogolny.png"))
        self.btn_zapisz_png.clicked.connect(lambda: self.zapisz_plik("schemat_jednokreskowy.png"))
        layout.addWidget(self.btn_zapisz_png)

        self.btn_zapisz_docx = QPushButton("Zapisz DOCX")
        self.btn_zapisz_docx.clicked.connect(lambda: self.zapisz_plik("dokument_schematy.docx"))
        layout.addWidget(self.btn_zapisz_docx)

        self.btn_zapisz_pdf = QPushButton("Zapisz PDF")
        self.btn_zapisz_pdf.clicked.connect(lambda: self.zapisz_plik("dokument_schematy.pdf"))
        layout.addWidget(self.btn_zapisz_pdf)

        self.setLayout(layout)

    def update_combo_style(self, combo, index):
        if index == 0:
            combo.setStyleSheet("color: red;")
        else:
            combo.setStyleSheet("color: green;")

 # 🧠 Funkcja uruchamiana po kliknięciu "Generuj"
    def show_selected_values(self):
        global wygeneruj_schemat
        wygeneruj_schemat = 1

        cable = self.cable_combo.currentText()
        control = self.control_combo.currentText()
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
        konwertuj_docx_na_pdf("dokument_schematy.docx")
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

    def show_pdf(self):

        global wygeneruj_schemat


        sciezka2 = resource_path_all(r'przegladarka_pdf\podglad_pdf.py')

        sciezka1 = resource_path_all(r'przegladarka_pdf')
        sciezka_do_pliku = resource_path_all(r"generator_schematow_jednokreskowych_ogolny\dokument_schematy.pdf")
        print(f"sciezka do otwieranego pliku : {sciezka_do_pliku}")
        if wygeneruj_schemat == 1:

            print("zostanie przekazany argument że schemat jest juz gotowy")
            subprocess.Popen( ["python",sciezka2, "--sciezka", sciezka_do_pliku, "--schemat_ready", "1"], cwd=sciezka1)


        else:
            print("otwieranie podgladu pdf bez schematu")
            subprocess.Popen( ["python",sciezka2, "--sciezka", sciezka_do_pliku], cwd=sciezka1)

    def zapisz_plik(self, plik_zrodlowy):
        from PySide6.QtWidgets import QFileDialog
        import shutil
        import os

        domyslna_nazwa = os.path.basename(plik_zrodlowy)

        sciezka_docelowa, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik jako",
            domyslna_nazwa,
            "",  # brak filtra
            options=QFileDialog.Options()
        )

        if sciezka_docelowa:
            try:
                shutil.copyfile(plik_zrodlowy, sciezka_docelowa)
                print(f"✅ Zapisano plik do: {sciezka_docelowa}")
            except Exception as e:
                print(f"❌ Błąd podczas zapisu: {e}")


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
