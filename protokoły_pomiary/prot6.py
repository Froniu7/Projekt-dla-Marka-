import sys
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class ProtocolGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generator Protokołów Pomiaru Impedancji Pętli Zwarcia")
        self.setGeometry(100, 100, 700, 750)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- Tytuł aplikacji ---
        title_label = QLabel("Generator Protokołów Pomiaru Impedancji Pętli Zwarcia")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)

        # --- Sekcja wprowadzania danych ---
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        self.add_input_field(input_layout, "Lokalizacja pomiaru:", "location_input",
                             "np. Gniazdo 1, Oświetlenie Kuchnia")

        # QComboBox dla Rodzaju sieci
        self.add_label_to_layout(input_layout, "Rodzaj sieci:")
        self.network_type_combo = QComboBox()
        self.network_type_combo.addItems(["TN-C-S", "TN-S", "TN-C", "TT"])
        input_layout.addWidget(self.network_type_combo)

        # QComboBox dla Typu pomiaru
        self.add_label_to_layout(input_layout, "Typ pomiaru:")
        self.measurement_type_combo = QComboBox()
        input_layout.addWidget(self.measurement_type_combo)

        # Połączenie sygnału ze slotem
        self.network_type_combo.currentTextChanged.connect(self.update_measurement_types)

        self.add_input_field(input_layout, "Typ zabezpieczenia:", "security_type_input", "np. C16, B10, gG10")
        self.add_input_field(input_layout, "Zmierzona impedancja Zz [Ω]:", "impedance_input", "np. 0.9", numeric=True)

        main_layout.addLayout(input_layout)
        main_layout.addSpacing(20)

        # --- Przycisk generowania protokołu ---
        generate_button = QPushButton("Generuj Protokół")
        generate_button.setFont(QFont("Arial", 12, QFont.Bold))
        generate_button.setFixedSize(200, 40)
        generate_button.clicked.connect(self.generate_protocol)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(generate_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(30)

        # --- Sekcja wyników ---
        results_layout = QVBoxLayout()
        results_layout.setSpacing(8)

        self.add_result_field(results_layout, "Prąd zadziałania Ia:", "ia_result_label", " A")
        self.add_result_field(results_layout, "Dopuszczalny czas wyłączenia Ta:", "ta_result_label", " s")
        self.add_result_field(results_layout, "Impedancja dopuszczalna Zd:", "zd_result_label", " Ω")
        self.add_result_field(results_layout, "Obliczeniowy prąd zwarcia Isc:", "isc_result_label", " A")
        self.add_result_field(results_layout, "Pomiar pomyślny?:", "evaluation_result_label", "", bold=True)
        self.add_result_field(results_layout, "Uwagi:", "remarks_label", "", bold=True)

        main_layout.addLayout(results_layout)
        main_layout.addStretch()

        # Ustawienie początkowego stanu
        self.update_measurement_types()

    def add_input_field(self, layout, label_text, attr_name, placeholder_text, numeric=False):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(200)
        h_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        if numeric:
            line_edit.setValidator(self.create_float_validator())
        setattr(self, attr_name, line_edit)
        h_layout.addWidget(line_edit)
        layout.addLayout(h_layout)

    def add_label_to_layout(self, layout, text):
        h_layout = QHBoxLayout()
        label = QLabel(text)
        label.setFixedWidth(200)
        h_layout.addWidget(label)
        h_layout.addStretch()
        layout.addLayout(h_layout)

    def add_result_field(self, layout, label_text, attr_name, unit="", bold=False):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(250)
        if bold:
            label.setFont(QFont("Arial", 10, QFont.Bold))
        h_layout.addWidget(label)

        value_label = QLabel("N/A" + unit)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        if bold:
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
        setattr(self, attr_name, value_label)
        h_layout.addWidget(value_label)
        h_layout.addStretch()
        layout.addLayout(h_layout)

    def create_float_validator(self):
        return None

    def update_measurement_types(self):
        """Aktualizuje dostępne typy pomiarów w zależności od wybranego rodzaju sieci."""
        selected_network_type = self.network_type_combo.currentText()

        self.measurement_type_combo.clear()

        if selected_network_type == "TN-C":
            self.measurement_type_combo.addItems(["L-PEN"])
        elif selected_network_type in ["TN-S", "TN-C-S", "TT"]:
            self.measurement_type_combo.addItems(["L-PE", "L-N"])

    def calculate_ia(self, typ_zabezpieczenia, prad_znamionowy):
        """Oblicza prąd zadziałania Ia na podstawie typu zabezpieczenia."""
        charakterystyka = typ_zabezpieczenia[0].upper()

        if charakterystyka == 'B':
            ia = 5 * prad_znamionowy
        elif charakterystyka == 'C':
            ia = 10 * prad_znamionowy
        elif charakterystyka == 'G':
            ia = 5 * prad_znamionowy
        else:
            return None, "Nieobsługiwana charakterystyka zabezpieczenia (obsługiwane: B, C, gG)."
        return ia, None

    def generate_protocol(self):
        lokalizacja = self.location_input.text().strip()
        rodzaj_sieci = self.network_type_combo.currentText().strip()
        typ_pomiaru = self.measurement_type_combo.currentText().strip()
        typ_zabezpieczenia = self.security_type_input.text().strip()
        impedancja_text = self.impedance_input.text().strip()

        if not lokalizacja or not typ_zabezpieczenia or not impedancja_text:
            QMessageBox.warning(self, "Błąd", "Wszystkie pola muszą być wypełnione.")
            self.reset_results()
            return

        try:
            impedancja_zmierzona = float(impedancja_text)
            if impedancja_zmierzona <= 0:
                QMessageBox.warning(self, "Błąd", "Impedancja zmierzona musi być liczbą dodatnią.")
                self.reset_results()
                return
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Wartość impedancji musi być liczbą.")
            self.reset_results()
            return

        try:
            prad_znamionowy = int(''.join(filter(str.isdigit, typ_zabezpieczenia)))
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Niepoprawny format typu zabezpieczenia (np. C16, B10, gG10).")
            self.reset_results()
            return

        prad_zadzialania_Ia, blad = self.calculate_ia(typ_zabezpieczenia, prad_znamionowy)

        if blad:
            QMessageBox.warning(self, "Błąd", blad)
            self.reset_results()
            return

        if rodzaj_sieci in ['TN-C-S', 'TN-S', 'TN-C']:
            czas_wylaczenia_Ta = 0.4
        elif rodzaj_sieci == 'TT':
            czas_wylaczenia_Ta = 0.2
        else:
            QMessageBox.warning(self, "Błąd", "Nieobsługiwany rodzaj sieci (obsługiwane: TN-C-S, TN-S, TN-C, TT).")
            self.reset_results()
            return

        # Weryfikacja typu pomiaru w zależności od rodzaju sieci
        ocena_typ_pomiaru_str = "Pomiar zgodny z układem sieci."
        uwagi_str = "Pomiar poprawny."

        if typ_pomiaru == 'L-N':
            ocena_typ_pomiaru_str = "Weryfikacja spadków napięcia. Nie jest to pomiar pętli zwarcia."
            uwagi_str = "Pomiar nie służy do oceny skuteczności ochrony przeciwporażeniowej."
        elif rodzaj_sieci == 'TN-C' and typ_pomiaru != 'L-PEN':
            ocena_typ_pomiaru_str = "Błąd: W układzie TN-C należy wykonywać pomiar L-PEN."
            uwagi_str = "Wymagana weryfikacja pomiaru. Pomiar niezgodny z układem sieci."
        elif rodzaj_sieci in ['TN-S', 'TN-C-S', 'TT'] and typ_pomiaru != 'L-PE':
            ocena_typ_pomiaru_str = f"Błąd: W układzie {rodzaj_sieci} należy wykonywać pomiar L-PE."
            uwagi_str = "Wymagana weryfikacja pomiaru. Pomiar niezgodny z układem sieci."

        # Automatyczne obliczenia
        napiecie_znamionowe = 230.0  # V

        if prad_zadzialania_Ia == 0:
            QMessageBox.warning(self, "Błąd", "Prąd zadziałania Ia nie może być zerowy.")
            self.reset_results()
            return

        impedancja_dopuszczalna = napiecie_znamionowe / prad_zadzialania_Ia
        prad_zwarcia_Isc = napiecie_znamionowe / impedancja_zmierzona

        # Ocena pomiaru pod kątem wartości
        ocena_str = "TAK"
        if prad_zwarcia_Isc < prad_zadzialania_Ia:
            ocena_str = "NIE"
            uwagi_str = "Niska wartość obliczeniowego prądu zwarcia (Isc). Możliwa błędna instalacja, luźne połączenie lub błąd w pomiarze."

        # Aktualizacja wyników w GUI
        self.ia_result_label.setText(f"{prad_zadzialania_Ia:.2f} A")
        self.ta_result_label.setText(f"{czas_wylaczenia_Ta:.1f} s")
        self.zd_result_label.setText(f"{impedancja_dopuszczalna:.2f} Ω")
        self.isc_result_label.setText(f"{prad_zwarcia_Isc:.2f} A")
        self.evaluation_result_label.setText(ocena_str)
        self.measurement_type_verification_label.setText(ocena_typ_pomiaru_str)
        self.remarks_label.setText(uwagi_str)

        # Generowanie treści protokołu do pliku
        tresc_protokolu = f"""
==================================================
        PROTOKÓŁ Z POMIARU IMPEDANCJI PĘTLI ZWARCIA
==================================================
Data wykonania: {datetime.date.today()}
Lokalizacja pomiaru: {lokalizacja}
Rodzaj sieci: {rodzaj_sieci}
Typ pomiaru: {typ_pomiaru}

--- Dane zabezpieczenia ---
Typ zabezpieczenia: {typ_zabezpieczenia.upper()}
Prąd znamionowy In: {prad_znamionowy} A
Prąd zadziałania Ia: {prad_zadzialania_Ia} A
Dopuszczalny czas wyłączenia Ta: {czas_wylaczenia_Ta} s

--- Wyniki pomiaru ---
Impedancja zmierzona Zz: {impedancja_zmierzona:.2f} Ω
Impedancja dopuszczalna Zd: {impedancja_dopuszczalna:.2f} Ω
Obliczeniowy prąd zwarcia Isc: {prad_zwarcia_Isc:.2f} A
(wymagana wartość >= {prad_zadzialania_Ia} A)

--- Ocena ---
Pomiar pomyślny? {ocena_str}
Uwagi: {uwagi_str}

--- Weryfikacja ---
Weryfikacja typu pomiaru: {ocena_typ_pomiaru_str}

"""
        # Zapis do pliku
        nazwa_pliku = "protokol_pomiaru.txt"
        try:
            with open(nazwa_pliku, "w", encoding='utf-8') as plik:
                plik.write(tresc_protokolu)
            QMessageBox.information(self, "Sukces",
                                    f"Protokół został wygenerowany i zapisany do pliku '{nazwa_pliku}'.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd zapisu", f"Wystąpił błąd podczas zapisu pliku: {e}")

    def reset_results(self):
        self.ia_result_label.setText("N/A A")
        self.ta_result_label.setText("N/A s")
        self.zd_result_label.setText("N/A Ω")
        self.isc_result_label.setText("N/A A")
        self.evaluation_result_label.setText("N/A")
        self.measurement_type_verification_label.setText("N/A")
        self.remarks_label.setText("N/A")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProtocolGeneratorApp()
    window.show()
    sys.exit(app.exec())