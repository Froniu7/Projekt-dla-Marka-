import sys
import datetime
import csv
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox,
    QGridLayout, QGroupBox, QFrame, QTextEdit,
    QCalendarWidget, QDialog, QDialogButtonBox, QRadioButton
)
from PySide6.QtGui import QFont, QDoubleValidator, QIcon, QPixmap
from PySide6.QtCore import Qt, QLocale, QDate, Signal

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.platypus import Image
import os
import re
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QLabel, QPushButton, QMessageBox
)
from reportlab.platypus import PageBreak
from PySide6.QtWidgets import QFileDialog

# Rejestracja czcionki z obsługą polskich znaków
# Upewnij się, że plik DejaVuSans.ttf znajduje się w tym samym katalogu co ten skrypt
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
except Exception as e:
    print(f"Błąd podczas ładowania czcionki: {e}")


class CalendarWindow(QDialog):
    date_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wybierz datę")
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setLocale(QLocale(QLocale.Polish, QLocale.Poland))
        layout.addWidget(self.calendar)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept_date)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept_date(self):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        self.date_selected.emit(selected_date)
        self.accept()


class ProtocolGeneratorApp(QMainWindow):
    # Słownik przechowujący dane zabezpieczeń
    ZABEZPIECZENIA = {
        "B10": {"symbol": "S301", "charakterystyka": "B", "prad_znamionowy": 10, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 5},
        "B16": {"symbol": "S301", "charakterystyka": "B", "prad_znamionowy": 16, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 5},
        "C6": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 6, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C10": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 10, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C16": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 16, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C20": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 20, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C25": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 25, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C32": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 32, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C40": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 40, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C63": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 63, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "C80": {"symbol": "S303", "charakterystyka": "C", "prad_znamionowy": 80, "czas_dzialania": 0.4,
                "krotnosc_pradu_zwarcia": 10},
        "D02 gG10": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 10, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "D02 gG16": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 16, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "D02 gG20": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 20, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "D02 gG32": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 20, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "D02 gG40": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 40, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "D02 gG63": {"symbol": "D02 gG", "charakterystyka": "gG", "prad_znamionowy": 63, "czas_dzialania": 0.4,
                 "krotnosc_pradu_zwarcia": 5},
        "NH00 gG10": {"symbol": "NH00 gG", "charakterystyka": "gG", "prad_znamionowy": 10, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH00 gG16": {"symbol": "NH00 gG", "charakterystyka": "gG", "prad_znamionowy": 16, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH00 gG20": {"symbol": "NH00 gG", "charakterystyka": "gG", "prad_znamionowy": 20, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH00 gG25": {"symbol": "NH00 gG", "charakterystyka": "gG", "prad_znamionowy": 25, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH00 gG32": {"symbol": "NH00 gG", "charakterystyka": "gG", "prad_znamionowy": 32, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},

        # NH01 – długość 70 mm, średnica 14 mm
        "NH01 gG40": {"symbol": "NH01 gG", "charakterystyka": "gG", "prad_znamionowy": 40, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH01 gG50": {"symbol": "NH01 gG", "charakterystyka": "gG", "prad_znamionowy": 50, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH01 gG63": {"symbol": "NH01 gG", "charakterystyka": "gG", "prad_znamionowy": 63, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH01 gG80": {"symbol": "NH01 gG", "charakterystyka": "gG", "prad_znamionowy": 80, "czas_dzialania": 0.4,
                      "krotnosc_pradu_zwarcia": 5},
        "NH01 gG100": {"symbol": "NH01 gG", "charakterystyka": "gG", "prad_znamionowy": 100, "czas_dzialania": 0.4,
                       "krotnosc_pradu_zwarcia": 5},

        # NH03 – długość 100 mm, średnica 14 mm
        "NH03 gG125": {"symbol": "NH03 gG", "charakterystyka": "gG", "prad_znamionowy": 125, "czas_dzialania": 0.4,
                       "krotnosc_pradu_zwarcia": 5},
        "NH03 gG160": {"symbol": "NH03 gG", "charakterystyka": "gG", "prad_znamionowy": 160, "czas_dzialania": 0.4,
                       "krotnosc_pradu_zwarcia": 5},
        "NH03 gG200": {"symbol": "NH03 gG", "charakterystyka": "gG", "prad_znamionowy": 200, "czas_dzialania": 0.4,
                       "krotnosc_pradu_zwarcia": 5},
        "NH03 gG250": {"symbol": "NH03 gG", "charakterystyka": "gG", "prad_znamionowy": 250, "czas_dzialania": 0.4,
                       "krotnosc_pradu_zwarcia": 5}

    }

    PRZEWODY = {
        "2.5 mm²": 7.41,
        "4 mm²": 4.61,
        "6 mm²": 3.08,
        "10 mm²": 1.83,
        "16 mm²": 1.15,
        "25 mm²": 0.727,
        "35 mm²": 0.524,
        "50 mm²": 0.387,
        "70 mm²": 0.268,
        "95 mm²": 0.193,
        "120 mm²": 0.153,
        "150 mm²": 0.124,
        "185 mm²": 0.0991,
        "240 mm²": 0.075,
    }

    # Wymagane minimalne wartości rezystancji izolacji [MΩ]
    MIN_R_ISO = 500
    # Wymagana minimalna wartość rezystancji uzwojenia [MΩ]
    MIN_R_W = 1



    def __init__(self):
        super().__init__()
        self.device_name = None
        self.setWindowTitle("Generator Protokołów Pomiaru Impedancji Pętli Zwarcia")
        self.setGeometry(100, 100, 1200, 750)
        self.measurement_fields = {}
        self.measurement_groups = {}
        self.electricians_data = self.load_data_from_csv("elektrycy.csv")
        self.devices_data = self.load_data_from_csv("przyrzady.csv")
        self.init_ui()


    def load_data_from_csv(self, filename):
        """Wczytuje dane z pliku CSV."""
        data = []
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            QMessageBox.critical(self, "Błąd pliku",
                                 f"Nie znaleziono pliku: {filename}\nUpewnij się, że plik istnieje w tym samym folderze co program.")
            return []
        except Exception as e:
            QMessageBox.critical(self, "Błąd wczytywania", f"Wystąpił błąd podczas wczytywania pliku CSV: {e}")
            return []
        return data

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- Przycisk generowania PDF w lewym górnym rogu ---
        top_bar_layout = QHBoxLayout()
        self.generate_pdf_button = QPushButton("Generuj PDF")
        self.generate_pdf_button.setFixedSize(120, 30)
        self.generate_pdf_button.clicked.connect(self.generate_pdf_protocol)

        # Ustawienie stylu, aby przycisk był bardziej widoczny
        self.generate_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        top_bar_layout.addWidget(self.generate_pdf_button)
        top_bar_layout.addStretch(1)  # Spycha przycisk do lewej
        main_layout.addLayout(top_bar_layout)
        main_layout.addSpacing(10)

        # --- Przycisk zapisu PDF obok generowania ---
        self.save_pdf_button = QPushButton("Zapisz PDF")
        self.save_pdf_button.setFixedSize(120, 30)
        self.save_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.save_pdf_button.clicked.connect(self.save_pdf)

        top_bar_layout.addWidget(self.save_pdf_button)

        # --- Główne dane ogólne + Rezystancja Izolacji w dwóch kolumnach ---
        top_layout = QGridLayout()
        main_layout.addLayout(top_layout)

        # Lewa kolumna - dane ogólne
        general_groupbox = QGroupBox("1. Dane ogólne")
        general_layout = QVBoxLayout()
        general_groupbox.setLayout(general_layout)

        # Lokalizacja pomiaru
        self.add_multiline_field(general_layout, "Lokalizacja pomiaru:", "location_input",
                                 "np. Gniazdo 1, Oświetlenie Kuchnia", label_on_top=True)

        # Napięcie probiercze Riso i Temperatura obok siebie
        voltage_temp_layout = QHBoxLayout()
        self.add_input_field(voltage_temp_layout, "Napięcie probiercze Riso [V]:", "voltage_Riso_input", "np. 500",
                             numeric=True)
        # Dodana linijka kodu do ustawienia domyślnej wartości
        self.voltage_Riso_input.setText("500")
        self.add_input_field(voltage_temp_layout, "Temperatura otoczenia [°C]:", "temp_input", "np. 20", numeric=True)
        general_layout.addLayout(voltage_temp_layout)

        # Data wykonania pomiarów i Przyrząd pomiarowy obok siebie
        date_device_layout = QHBoxLayout()
        date_layout = QHBoxLayout()
        date_label = QLabel("Data wykonania pomiarów:")
        date_label.setFixedWidth(200)
        date_layout.addWidget(date_label)
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText(QDate.currentDate().toString(Qt.ISODate))
        self.date_input.setReadOnly(True)
        date_layout.addWidget(self.date_input)
        select_date_button = QPushButton("Wybierz datę")
        select_date_button.clicked.connect(self.show_calendar)
        date_layout.addWidget(select_date_button)
        date_device_layout.addLayout(date_layout)

        device_layout = QHBoxLayout()
        device_label = QLabel("Przyrząd pomiarowy:")
        device_label.setFixedWidth(200)
        device_layout.addWidget(device_label)
        self.device_combo = QComboBox()
        self.populate_device_combo(self.device_combo)
        device_layout.addWidget(self.device_combo)
        date_device_layout.addLayout(device_layout)

        general_layout.addLayout(date_device_layout)

        # Rodzaj sieci i Typ zabezpieczenia obok siebie
        network_security_layout = QHBoxLayout()

        network_layout = QVBoxLayout()
        self.add_label_to_layout(network_layout, "Rodzaj sieci:")
        self.network_type_combo = QComboBox()
        self.network_type_combo.addItems(["TN-C-S", "TN-S", "TN-C", "TT"])
        network_layout.addWidget(self.network_type_combo)
        network_security_layout.addLayout(network_layout)

        security_layout = QVBoxLayout()
        self.add_label_to_layout(security_layout, "Typ zabezpieczenia:")
        self.security_type_combo = QComboBox()
        self.security_type_combo.addItems(self.ZABEZPIECZENIA.keys())
        security_layout.addWidget(self.security_type_combo)
        network_security_layout.addLayout(security_layout)

        general_layout.addLayout(network_security_layout)

        # Wykonawca i Sprawdzający w układzie siatki
        electricians_layout = QGridLayout()

        # Sprawdzający
        electricians_layout.addWidget(QLabel("Sprawdzający:"), 0, 0)
        self.reviewer_combo = QComboBox()
        self.reviewer_combo.setFixedWidth(250)
        self.populate_electrician_combo(self.reviewer_combo, 'nr_uprawnien_D')
        electricians_layout.addWidget(self.reviewer_combo, 1, 0)

        # Radio-buttony dla podpisu
        signature_radio_layout = QHBoxLayout()
        signature_label = QLabel("Podpis:")
        self.signature_radio_button = QRadioButton("Tak")
        self.no_signature_radio_button = QRadioButton("Brak")
        self.signature_radio_button.setChecked(True)  # Domyślnie zaznaczony
        signature_radio_layout.addWidget(signature_label)
        signature_radio_layout.addWidget(self.signature_radio_button)
        signature_radio_layout.addWidget(self.no_signature_radio_button)
        signature_radio_layout.addStretch()
        electricians_layout.addLayout(signature_radio_layout, 2, 0)

        # Wykonawca
        electricians_layout.addWidget(QLabel("Wykonawca:"), 0, 1)
        self.executor_combo = QComboBox()
        self.executor_combo.setFixedWidth(250)
        self.populate_electrician_combo(self.executor_combo, 'nr_uprawnien_E')
        electricians_layout.addWidget(self.executor_combo, 1, 1)

        # Nowe pole dla nazwy urządzenia (w miejscu, gdzie chcesz je dodać)
        device_name_layout = QHBoxLayout()

        device_label = QLabel("Nazwa urządzenia:")
        device_label.setFixedWidth(200)  # dopasuj jeśli potrzebujesz
        device_name_layout.addWidget(device_label)

        self.device_name_input = QLineEdit()
        self.device_name_input.setPlaceholderText("np. Kompensator mocy")
        self.device_name_input.setText("EkoRedux")  # prefill (opcjonalne)
        self.device_name_input.setFixedWidth(250)

        # Aktualizuj self.device_name przy każdej zmianie tekstu
        self.device_name_input.textChanged.connect(self.on_device_name_changed)

        device_name_layout.addWidget(self.device_name_input)
        device_name_layout.addStretch()
        electricians_layout.addLayout(device_name_layout, 2, 1)

        general_layout.addLayout(electricians_layout)

        top_layout.addWidget(general_groupbox, 0, 0)

        # Prawa kolumna - pomiar rezystancji izolacji
        insulation_groupbox = QGroupBox("2. Pomiar rezystancji izolacji")
        insulation_layout = QVBoxLayout()
        insulation_groupbox.setLayout(insulation_layout)

        iso_grid_layout = QGridLayout()

        # Ustawienie nagłówków
        iso_grid_layout.addWidget(QLabel("Pomiar"), 0, 0, Qt.AlignCenter)
        iso_grid_layout.addWidget(QLabel("Wartość [MΩ]"), 0, 1, Qt.AlignCenter)

        # Słownik do przechowywania referencji do pól
        self.iso_fields = {}

        # Dodanie pól wprowadzania do siatki
        row_num = 1
        for name in ["L1-PE", "L2-PE", "L3-PE", "L1-N", "L2-N", "L3-N", "L1-L2", "L1-L3", "L2-L3", "N-PE", "RW"]:
            label = QLabel(name)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("MΩ")
            line_edit.setValidator(QDoubleValidator())

            # Dodanie pola do słownika i przypisanie do obiektu
            self.iso_fields[name] = line_edit
            setattr(self, f"iso_{name.lower().replace('-', '')}", line_edit)

            iso_grid_layout.addWidget(label, row_num, 0)
            iso_grid_layout.addWidget(line_edit, row_num, 1)
            row_num += 1

        insulation_layout.addLayout(iso_grid_layout)

        # Dodanie przycisków w poziomie
        iso_buttons_layout = QHBoxLayout()

        autofill_iso_button = QPushButton("Uzupełnij automatycznie")
        autofill_iso_button.clicked.connect(self.autofill_insulation_fields)
        iso_buttons_layout.addWidget(autofill_iso_button)

        verify_iso_button = QPushButton("Weryfikacja")
        verify_iso_button.clicked.connect(self.verify_insulation_all)
        iso_buttons_layout.addWidget(verify_iso_button)

        insulation_layout.addLayout(iso_buttons_layout)

        self.iso_result_label = QLabel("")
        insulation_layout.addWidget(self.iso_result_label)

        top_layout.addWidget(insulation_groupbox, 0, 1)

        main_layout.addSpacing(20)

        # ... (pozostała część kodu) ...

        # --- Sekcje dla pomiarów impedancji według faz ---
        measurement_groupbox = QGroupBox("3. Pomiar impedancji pętli zwarcia")
        measurement_layout = QVBoxLayout()
        measurement_groupbox.setLayout(measurement_layout)

        phases_layout = QHBoxLayout()
        self.measurement_groups["L1"] = self.create_phase_groupbox("Faza L1", "l1", ["L1-N", "L1-PE"])
        phases_layout.addWidget(self.measurement_groups["L1"])
        self.measurement_groups["L2"] = self.create_phase_groupbox("Faza L2", "l2", ["L2-N", "L2-PE"])
        phases_layout.addWidget(self.measurement_groups["L2"])
        self.measurement_groups["L3"] = self.create_phase_groupbox("Faza L3", "l3", ["L3-N", "L3-PE"])
        phases_layout.addWidget(self.measurement_groups["L3"])

        measurement_layout.addLayout(phases_layout)

        # Prawidłowa, jednokrotna deklaracja układu, do którego dodamy wszystkie elementy
        impedance_verification_layout = QHBoxLayout()

        # Dodanie nowego przycisku "Oblicz Zz"
        self.calculate_impedance_button = QPushButton("Oblicz Zz")
        self.calculate_impedance_button.clicked.connect(self.show_impedance_calculator)
        impedance_verification_layout.addWidget(self.calculate_impedance_button)

        # Dodanie przycisku "Weryfikacja"
        self.verify_all_impedance_button = QPushButton("Weryfikacja")
        self.verify_all_impedance_button.clicked.connect(self.log_impedance_values)
        impedance_verification_layout.addWidget(self.verify_all_impedance_button)

        # Dodanie etykiety z oceną
        self.verification_result_label = QLabel("Ocena: ")
        self.verification_result_label.setStyleSheet("font-weight: bold;")
        impedance_verification_layout.addWidget(self.verification_result_label)

        impedance_verification_layout.addStretch()

        measurement_layout.addLayout(impedance_verification_layout)

        main_layout.addWidget(measurement_groupbox)
        main_layout.addSpacing(20)

        # ... (pozostała część kodu) ...

        # --- Sekcja pomiarów ciągłości połączeń wyrównawczych ---
        continuity_groupbox = QGroupBox("4. Pomiar ciągłości połączeń wyrównawczych")
        continuity_layout = QHBoxLayout()  # Zmiana na układ poziomy
        continuity_groupbox.setLayout(continuity_layout)

        # Wszystkie pola w jednym wierszu
        self.add_input_field(continuity_layout, "Zmierzone R [Ω]:", "continuity_measured_input", "np. 0.07",
                             numeric=True)

        continuity_layout.addWidget(QLabel("Typ przewodu:"))
        self.continuity_cable_combo = QComboBox()
        self.continuity_cable_combo.addItems(self.PRZEWODY.keys())
        continuity_layout.addWidget(self.continuity_cable_combo)

        self.add_input_field(continuity_layout, "Długość przewodu [m]:", "continuity_length_input", "np. 10",
                             numeric=True)

        self.continuity_verify_button = QPushButton("Weryfikacja")
        self.continuity_verify_button.clicked.connect(self.verify_continuity)
        continuity_layout.addWidget(self.continuity_verify_button)

        continuity_layout.addStretch()

        continuity_result_layout = QVBoxLayout()
        self.continuity_result_label = QLabel("")
        continuity_result_layout.addWidget(self.continuity_result_label)
        continuity_layout.addLayout(continuity_result_layout)

        main_layout.addWidget(continuity_groupbox)

        # --- Nowy kwadrat 5: Uwagi ---
        notes_groupbox = QGroupBox("5. Uwagi")
        notes_layout = QVBoxLayout()
        notes_groupbox.setLayout(notes_layout)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Wpisz tutaj uwagi...")
        self.notes_input.setMinimumHeight(100)
        notes_layout.addWidget(self.notes_input)

        # Przyciski do automatycznego wstawiania tekstu
        notes_buttons_layout = QHBoxLayout()

        btn_brak = QPushButton("Brak")
        btn_brak.clicked.connect(lambda: self.notes_input.setText("Brak"))
        notes_buttons_layout.addWidget(btn_brak)

        btn_napięcia = QPushButton("info-Napięcia")
        btn_napięcia.clicked.connect(self.insert_voltage_info)
        notes_buttons_layout.addWidget(btn_napięcia)

        btn_normy = QPushButton("info-Normy")
        btn_normy.clicked.connect(self.insert_norm_info)
        notes_buttons_layout.addWidget(btn_normy)

        # Nowy przycisk "info-Wszystko"
        btn_all = QPushButton("info-Wszystko")
        btn_all.clicked.connect(self.insert_all_info)
        notes_buttons_layout.addWidget(btn_all)

        notes_buttons_layout.addStretch()
        notes_layout.addLayout(notes_buttons_layout)

        main_layout.addWidget(notes_groupbox)
        main_layout.addSpacing(20)

    import re
    from PySide6.QtWidgets import QFileDialog, QMessageBox

    def save_pdf(self):
        # Pobranie tekstu z pola wieloliniowego
        full_text = self.location_input.toPlainText()
        lines = full_text.splitlines()

        # Pobranie pierwszych trzech linii i połączenie w jeden ciąg
        file_name_base = "_".join(lines[:3]) if lines else "protokol_pomiaru"

        # Usunięcie niedozwolonych znaków w nazwie pliku
        file_name_base = re.sub(r'[\\/*?:"<>|]', "", file_name_base)

        # Dodanie rozszerzenia PDF
        default_file = f"{file_name_base}.pdf"

        # Okno dialogowe do wyboru lokalizacji zapisu
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz PDF jako...",
            default_file,
            "Pliki PDF (*.pdf)"
        )

        if file_path:
            try:
                import shutil
                shutil.copy("protokol_pomiaru.pdf", file_path)
                QMessageBox.information(self, "Zapisano", f"Plik zapisano jako:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać pliku:\n{e}")

    def on_device_name_changed(self, text: str):
        """Aktualizuje zmienną self.device_name przy każdej zmianie pola."""
        self.device_name = text.strip() or None
        # Opcjonalnie debug:
        # print(f"[DEBUG] device_name = {self.device_name}")

    def log_impedance_values(self):
        """
        Zbiera wartości z pól impedancji i napięcia, a następnie wyświetla je w konsoli.
        Przechowuje je w zmiennych float i wyświetla na końcu funkcji.
        """
        print("--- Rozpoczynam weryfikację impedancji ---")

        # Deklaracja zmiennych float z wartościami domyślnymi
        prad_znamionowy = 0.0
        krotnosc_pradu = 0.0
        Zz_L1_N = 0.0
        Zz_L1_PE = 0.0
        Zz_L2_N = 0.0
        Zz_L2_PE = 0.0
        Zz_L3_N = 0.0
        Zz_L3_PE = 0.0

        # 1. Pobranie danych zabezpieczenia i konwersja na float
        selected_security = self.security_type_combo.currentText().strip()
        security_data = self.ZABEZPIECZENIA.get(selected_security)

        if security_data:
            prad_znamionowy = float(security_data.get('prad_znamionowy', 0))
            krotnosc_pradu = float(security_data.get('krotnosc_pradu_zwarcia', 0))
        else:
            print("Błąd: Nie znaleziono danych dla wybranego zabezpieczenia.")

        # 2. Pobranie danych pomiarowych i konwersja na float
        try:
            if self.l1n_impedance_input.text().strip():
                Zz_L1_N = float(self.l1n_impedance_input.text().strip())
            if self.l1pe_impedance_input.text().strip():
                Zz_L1_PE = float(self.l1pe_impedance_input.text().strip())

            if self.l2n_impedance_input.text().strip():
                Zz_L2_N = float(self.l2n_impedance_input.text().strip())
            if self.l2pe_impedance_input.text().strip():
                Zz_L2_PE = float(self.l2pe_impedance_input.text().strip())

            if self.l3n_impedance_input.text().strip():
                Zz_L3_N = float(self.l3n_impedance_input.text().strip())
            if self.l3pe_impedance_input.text().strip():
                Zz_L3_PE = float(self.l3pe_impedance_input.text().strip())

        except (ValueError, AttributeError) as e:
            print(f"Wystąpił błąd podczas konwersji danych: {e}")
            # Wartości pozostaną 0.0, co jest pożądane w przypadku błędu

        # 3. Wypisanie wszystkich zmiennych float na końcu funkcji
        print("\n--- Wartości wszystkich zmiennych ---")
        print(f"wartość zmiennej prad_znamionowy: {prad_znamionowy}")
        print(f"wartość zmiennej krotnosc_pradu: {krotnosc_pradu}")
        print(f"wartość zmiennej Zz_L1_N: {Zz_L1_N}")
        print(f"wartość zmiennej Zz_L1_PE: {Zz_L1_PE}")
        print(f"wartość zmiennej Zz_L2_N: {Zz_L2_N}")
        print(f"wartość zmiennej Zz_L2_PE: {Zz_L2_PE}")
        print(f"wartość zmiennej Zz_L3_N: {Zz_L3_N}")
        print(f"wartość zmiennej Zz_L3_PE: {Zz_L3_PE}")
        print("--- Koniec weryfikacji ---")

        impedancja_Zz_granica = (230/(prad_znamionowy*krotnosc_pradu))
        print(f"Przedział dla Zz: od 0.1 Ω do {impedancja_Zz_granica} Ω")

        # Wyliczanie granicznej impedancji (Zd) na podstawie danych zabezpieczenia
        # Napięcie fazowe U = 230 V
        if prad_znamionowy > 0 and krotnosc_pradu > 0:
            impedancja_Zz_granica = 230 / (prad_znamionowy * krotnosc_pradu)
        else:
            impedancja_Zz_granica = 0

        # Słownik do przechowywania ocen
        oceny = {}

        # Sprawdzanie i ocenianie poszczególnych pomiarów
        # Pomiar L1-N
        if Zz_L1_N >= 0.1 and Zz_L1_N <= impedancja_Zz_granica:
            oceny['L1-N'] = 'TAK'
        else:
            oceny['L1-N'] = 'NIE'

        # Pomiar L1-PE
        if Zz_L1_PE >= 0.1 and Zz_L1_PE <= impedancja_Zz_granica:
            oceny['L1-PE'] = 'TAK'
        else:
            oceny['L1-PE'] = 'NIE'

        # Pomiar L2-N
        if Zz_L2_N >= 0.1 and Zz_L2_N <= impedancja_Zz_granica:
            oceny['L2-N'] = 'TAK'
        else:
            oceny['L2-N'] = 'NIE'

        # Pomiar L2-PE
        if Zz_L2_PE >= 0.1 and Zz_L2_PE <= impedancja_Zz_granica:
            oceny['L2-PE'] = 'TAK'
        else:
            oceny['L2-PE'] = 'NIE'

        # Pomiar L3-N
        if Zz_L3_N >= 0.1 and Zz_L3_N <= impedancja_Zz_granica:
            oceny['L3-N'] = 'TAK'
        else:
            oceny['L3-N'] = 'NIE'

        # Pomiar L3-PE
        if Zz_L3_PE >= 0.1 and Zz_L3_PE <= impedancja_Zz_granica:
            oceny['L3-PE'] = 'TAK'
        else:
            oceny['L3-PE'] = 'NIE'

        # Wypisanie ocen w konsoli
        print(f"Ocena L1-N: {oceny['L1-N']}")
        print(f"Ocena L1-PE: {oceny['L1-PE']}")
        print(f"Ocena L2-N: {oceny['L2-N']}")
        print(f"Ocena L2-PE: {oceny['L2-PE']}")
        print(f"Ocena L3-N: {oceny['L3-N']}")
        print(f"Ocena L3-PE: {oceny['L3-PE']}")

        #  Aktualizacja GUI
        wszystkie_poprawne = all(ocena == 'TAK' for ocena in oceny.values())

        if wszystkie_poprawne:
            self.verification_result_label.setText("Ocena: TAK (Wszystkie pomiary poprawne)")
            self.verification_result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.verification_result_label.setText("Ocena: NIE (Wystąpiły błędy)")
            self.verification_result_label.setStyleSheet("color: red; font-weight: bold;")

        # Utworzenie szczegółowego tekstu do wyświetlenia w oknie dialogowym
        details_text = f"Przedział dla Zz: od 0.1 Ω do {impedancja_Zz_granica:.2f} Ω.\n"
        for key, ocena in oceny.items():
            details_text += f"Ocena {key}: {ocena}\n"

        # Wyświetlenie okna dialogowego z wynikami
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Wyniki Weryfikacji")
        msg_box.setText(self.verification_result_label.text())
        msg_box.setInformativeText(details_text)
        msg_box.exec_()

    def show_impedance_calculator(self):
        calculator = ImpedanceCalculator(self)
        calculator.exec()

    def add_iso_field(self, layout, label_text, attr_name):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("MΩ")
        line_edit.setValidator(QDoubleValidator())
        setattr(self, attr_name, line_edit)
        v_layout.addWidget(label)
        v_layout.addWidget(line_edit)
        layout.addLayout(v_layout)

    def populate_electrician_combo(self, combo_box, permission_key):
        """Wypełnia QComboBox elektrykami z odpowiednimi uprawnieniami."""
        for electrician in self.electricians_data:
            if electrician.get(permission_key):
                text_to_display = f"{electrician['imie_nazwisko']} ({electrician[permission_key]})"
                combo_box.addItem(text_to_display)

    def populate_device_combo(self, combo_box):
        """Wypełnia QComboBox danymi z pliku przyrzady.csv."""
        for device in self.devices_data:
            # Sprawdzenie, czy pola 'data_wzorcowania' i 'numer_swiadectwa' są puste
            if device.get('data_wzorcowania') and device.get('numer_swiadectwa'):
                # Jeśli dane są, wyświetlamy pełny format
                text_to_display = f"{device['model']} (Nr seryjny: {device['nr_seryjny']}, Wzorcowanie : {device['data_wzorcowania']}, Nr świadectwa : {device['numer_swiadectwa']})"
            else:
                # Jeśli brakuje danych, wyświetlamy skrócony format
                text_to_display = f"{device['model']} (Nr seryjny: {device['nr_seryjny']})"

            combo_box.addItem(text_to_display)

    def create_phase_groupbox(self, group_label, phase_short_name, field_labels):
        group_box = QGroupBox(group_label)
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        # Dodanie pola na napięcie dla całej fazy
        self.add_input_field_without_voltage(group_layout, "Napięcie U [V]:", f"{phase_short_name}_voltage_input",
                                             "np. 238.7",
                                             numeric=True)

        for i, label in enumerate(field_labels):
            if i > 0:
                # Dodanie poziomej linii
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                group_layout.addWidget(line)

            sub_group_box = QGroupBox(label)
            sub_group_layout = QVBoxLayout()
            sub_group_box.setLayout(sub_group_layout)

            self.add_input_field_without_voltage(sub_group_layout, "Impedancja Zz [Ω]:",
                                                 f"{label.replace('-', '').lower()}_impedance_input", "np. 0.9",
                                                 numeric=True)

            # Przechowujemy tylko referencję do pola impedancji
            self.measurement_fields[label.replace('-', '').lower()] = {
                "impedance": getattr(self, f"{label.replace('-', '').lower()}_impedance_input")
            }
            group_layout.addWidget(sub_group_box)

        return group_box

    # Nowa metoda do dodawania pól bez etykiety napięcia
    def add_input_field_without_voltage(self, layout, label_text, attr_name, placeholder_text, numeric=False):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(130)
        h_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        if numeric:
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
            line_edit.setValidator(validator)

        setattr(self, attr_name, line_edit)
        h_layout.addWidget(line_edit)
        layout.addLayout(h_layout)

    def add_input_field(self, layout, label_text, attr_name, placeholder_text, numeric=False):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(200)
        h_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        if numeric:
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
            line_edit.setValidator(validator)

        setattr(self, attr_name, line_edit)
        h_layout.addWidget(line_edit)
        layout.addLayout(h_layout)

    def add_multiline_field(self, layout, label_text, attr_name, placeholder_text, label_on_top=False):
        if label_on_top:
            label = QLabel(label_text)
            layout.addWidget(label)
            text_edit = QTextEdit()
            text_edit.setPlaceholderText(placeholder_text)
            text_edit.setMinimumHeight(100)
            setattr(self, attr_name, text_edit)
            layout.addWidget(text_edit)
        else:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(200)
            h_layout.addWidget(label)
            text_edit = QTextEdit()
            text_edit.setPlaceholderText(placeholder_text)
            text_edit.setMinimumHeight(100)
            setattr(self, attr_name, text_edit)
            h_layout.addWidget(text_edit)
            layout.addLayout(h_layout)

    def add_label_to_layout(self, layout, text):
        h_layout = QHBoxLayout()
        label = QLabel(text)
        label.setFixedWidth(200)
        h_layout.addWidget(label)
        h_layout.addStretch()
        layout.addLayout(h_layout)

    def show_calendar(self):
        self.calendar_window = CalendarWindow(self)
        self.calendar_window.date_selected.connect(self.update_date_field)
        self.calendar_window.exec()

    def update_date_field(self, date_str):
        self.date_input.setText(date_str)

    def autofill_insulation_fields(self):
        """Wypełnia pola rezystancji izolacji wartościami minimalnymi."""
        for name, field in self.iso_fields.items():
            if name == "RW":
                field.setText(str(self.MIN_R_W))
            else:
                field.setText(str(self.MIN_R_ISO))

    def verify_insulation_all(self):
        """Weryfikuje wszystkie zmierzone rezystancje izolacji."""
        iso_fields = {
            "L1-PE": getattr(self, "iso_l1pe"), "L2-PE": getattr(self, "iso_l2pe"), "L3-PE": getattr(self, "iso_l3pe"),
            "L1-N": getattr(self, "iso_l1n"), "L2-N": getattr(self, "iso_l2n"), "L3-N": getattr(self, "iso_l3n"),
            "L1-L2": getattr(self, "iso_l1l2"), "L1-L3": getattr(self, "iso_l1l3"), "L2-L3": getattr(self, "iso_l2l3"),
            "N-PE": getattr(self, "iso_npe"), "RW": getattr(self, "iso_rw")
        }

        all_ok = True

        for name, field in iso_fields.items():
            value_text = field.text().strip()
            if not value_text:
                self.iso_result_label.setText(f"Błąd: Wartość dla {name} jest pusta.")
                all_ok = False
                break

            try:
                measured_value = float(value_text)
                if name == "RW":
                    if measured_value < self.MIN_R_W:
                        self.iso_result_label.setText(
                            f"Błąd: Zmierzona wartość dla {name} jest za niska (min. {self.MIN_R_W} MΩ).")
                        all_ok = False
                        break
                else:
                    if measured_value < self.MIN_R_ISO:
                        self.iso_result_label.setText(
                            f"Błąd: Zmierzona wartość dla {name} jest za niska (min. {self.MIN_R_ISO} MΩ).")
                        all_ok = False
                        break

            except ValueError:
                self.iso_result_label.setText(f"Błąd: Wartość dla {name} musi być liczbą.")
                all_ok = False
                break

        if all_ok:
            self.iso_result_label.setText("Ocena: TAK (Wszystkie pomiary izolacji poprawne)")

    def verify_continuity(self):
        """Weryfikuje zmierzoną rezystancję ciągłości z obliczoną wartością referencyjną."""
        try:
            continuity_measured = self.continuity_measured_input.text().strip()
            if not continuity_measured:
                self.continuity_result_label.setText("Wprowadź zmierzoną wartość.")
                return

            measured_value = float(continuity_measured)

            selected_cable = self.continuity_cable_combo.currentText().strip()
            cable_length_text = self.continuity_length_input.text().strip()

            if not cable_length_text:
                self.continuity_result_label.setText("Wprowadź długość przewodu.")
                return

            cable_length_m = float(cable_length_text)

            if cable_length_m <= 0:
                self.continuity_result_label.setText("Długość musi być dodatnia.")
                return

            resistivity = self.PRZEWODY.get(selected_cable) / 1000  # z Ω/km na Ω/m
            resistance_contacts = 0.05  # Rezystancja styków, stała wartość

            # Obliczenie wartości referencyjnej
            reference_value = resistivity * cable_length_m + resistance_contacts

            # Weryfikacja
            if measured_value <= reference_value * 1.25:  # Tolerancja 25%
                self.continuity_result_label.setText(f"Ocena: TAK (Wartość referencyjna: {reference_value:.3f} Ω)")
            else:
                self.continuity_result_label.setText(f"Ocena: NIE (Wartość referencyjna: {reference_value:.3f} Ω)")

        except ValueError:
            self.continuity_result_label.setText("Wprowadź prawidłowe liczby.")

    def insert_voltage_info(self):
        """Wstawia do pola Uwagi informacje o napięciach."""
        l1_voltage = self.l1_voltage_input.text().strip()
        l2_voltage = self.l2_voltage_input.text().strip()
        l3_voltage = self.l3_voltage_input.text().strip()

        notes_text = "Napięcia w sieci:\n"
        notes_text += f"L1-N {l1_voltage}V\n"
        notes_text += f"L2-N {l2_voltage}V\n"
        notes_text += f"L3-N {l3_voltage}V\n"

        self.notes_input.setText(notes_text)

    def insert_norm_info(self):
        """Wstawia do pola Uwagi informację o normach."""
        norm_text = """Po montażu urządzenia przeprowadzono badanie rezystancji izolacji przewodów zasilających kompensator oraz skuteczność ochrony przeciwporażeniowej zgodnie z normą: PN-HD 60364-4-41:2017-09. Dobrane zabezpieczenie nadprądowe spełnia warunki ochrony przeciwporażeniowej realizowanej poprzez samoczynne wyłączenie zasilania."""
        self.notes_input.setText(norm_text)

    def insert_all_info(self):
        """Wstawia do pola Uwagi informację o napięciach i normach."""
        l1_voltage = self.l1_voltage_input.text().strip()
        l2_voltage = self.l2_voltage_input.text().strip()
        l3_voltage = self.l3_voltage_input.text().strip()

        voltage_text = "Napięcia w sieci:\n"
        voltage_text += f"L1-N {l1_voltage}V\n"
        voltage_text += f"L2-N {l2_voltage}V\n"
        voltage_text += f"L3-N {l3_voltage}V\n\n"

        norm_text = """Po montażu urządzenia przeprowadzono badanie rezystancji izolacji przewodów zasilających kompensator oraz skuteczność ochrony przeciwporażeniowej zgodnie z normą: PN-HD 60364-4-41:2017-09. Dobrane zabezpieczenie nadprądowe spełnia warunki ochrony przeciwporażeniowej realizowanej poprzez samoczynne wyłączenie zasilania."""

        combined_text = voltage_text + norm_text
        self.notes_input.setText(combined_text)

    def generate_pdf_protocol(self):
        try:
            # Pobranie danych z pól wejściowych
            lokalizacja = self.location_input.toPlainText().strip()
            rodzaj_sieci = self.network_type_combo.currentText().strip()
            executor = self.executor_combo.currentText().strip()
            reviewer = self.reviewer_combo.currentText().strip()
            napiecie_probiercze = self.voltage_Riso_input.text().strip()
            temp_otoczenia = self.temp_input.text().strip()
            data_pomiarow = self.date_input.text().strip()
            przyrzad_pomiarowy = self.device_combo.currentText().strip()
            continuity_measured = self.continuity_measured_input.text().strip()
            notes = self.notes_input.toPlainText().strip()
            podpis_sprawdzajacego = self.signature_radio_button.isChecked()

            # Weryfikacja danych (uproszczona)
            if not all(
                    [lokalizacja, rodzaj_sieci, executor, reviewer, napiecie_probiercze, temp_otoczenia, data_pomiarow,
                     przyrzad_pomiarowy, continuity_measured]):
                QMessageBox.warning(self, "Błąd", "Wypełnij wszystkie wymagane pola w sekcjach 1 i 4.")
                return

            # Sprawdzenie pól izolacji
            iso_values = {}
            iso_evaluation = "TAK"
            for name, field in self.iso_fields.items():
                value = field.text().strip()
                if not value:
                    QMessageBox.warning(self, "Błąd",
                                        f"Wartość dla pomiaru {name} w sekcji 2. Pomiar rezystancji izolacji nie może być pusta.")
                    return
                iso_values[name] = value
                try:
                    measured_value = float(value)
                    min_val = self.MIN_R_W if name == "RW" else self.MIN_R_ISO
                    if measured_value < min_val:
                        iso_evaluation = "NIE"
                except ValueError:
                    iso_evaluation = "NIE"

            # Sprawdzenie pól impedancji i zebranie danych
            impedance_data = []
            typ_zabezpieczenia_nazwa = self.security_type_combo.currentText()
            dane_zabezpieczenia = self.ZABEZPIECZENIA[typ_zabezpieczenia_nazwa]
            prad_znamionowy = dane_zabezpieczenia["prad_znamionowy"]
            czas_dzialania = dane_zabezpieczenia["czas_dzialania"]
            krotnosc = dane_zabezpieczenia["krotnosc_pradu_zwarcia"]
            prad_zwarciowy_Ia_dla_zadzialania = krotnosc * prad_znamionowy

            lp = 1
            has_impedance_data = False

            phases_to_process = [("Faza L1", "l1", ["L1-N", "L1-PE"]), ("Faza L2", "l2", ["L2-N", "L2-PE"]),
                                 ("Faza L3", "l3", ["L3-N", "L3-PE"])]
            for phase, phase_short, labels in phases_to_process:
                voltage_text = getattr(self, f"{phase_short}_voltage_input").text().strip()
                # Pomijamy puste grupy faz, jeśli napięcie nie jest wypełnione
                if not voltage_text:
                    continue
                try:
                    napiecie_znamionowe = float(voltage_text)
                    if napiecie_znamionowe == 0:
                        QMessageBox.warning(self, "Błąd", f"Napięcie dla '{phase}' nie może być zerowe.")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Błąd", f"Napięcie dla '{phase}' musi być liczbą.")
                    return

                for label_key_full in labels:
                    label_key = label_key_full.replace('-', '').lower()
                    fields = self.measurement_fields.get(label_key)
                    impedance_text = fields["impedance"].text().strip()
                    if not impedance_text:
                        continue

                    has_impedance_data = True
                    try:
                        impedancja_zmierzona = float(impedance_text)

                        # Dodano sprawdzenie, czy impedancja nie jest zerem, aby uniknąć błędu "float division by zero"
                        if impedancja_zmierzona == 0:
                            QMessageBox.warning(self, "Błąd",
                                                f"Wartość impedancji dla '{label_key_full}' nie może być zerowa.")
                            return

                        impedancja_dopuszczalna = round(napiecie_znamionowe / prad_zwarciowy_Ia_dla_zadzialania, 2)
                        prad_zwarcia_Isc = round(napiecie_znamionowe / impedancja_zmierzona, 2)

                        ocena_str = "TAK"
                        if prad_zwarcia_Isc < prad_zwarciowy_Ia_dla_zadzialania:
                            ocena_str = "NIE"

                        impedance_data.append([
                            lp,
                            label_key_full,
                            f"{dane_zabezpieczenia['symbol']} {typ_zabezpieczenia_nazwa}",
                            f"{prad_znamionowy} A",
                            f"{czas_dzialania} s",
                            f"{prad_zwarciowy_Ia_dla_zadzialania} A",
                            f"{prad_zwarcia_Isc / 1000:.2f} kA",
                            f"{impedancja_dopuszczalna:.2f} Ω",
                            f"{impedancja_zmierzona:.2f} Ω",
                            ocena_str
                        ])
                        lp += 1
                    except (ValueError, KeyError) as e:
                        QMessageBox.warning(self, "Błąd danych",
                                            f"Sprawdź poprawność danych w sekcji {label_key_full}. Błąd: {e}")
                        return

            if not has_impedance_data:
                QMessageBox.warning(self, "Błąd", "Żadne pola pomiarowe impedancji nie zostały wypełnione.")
                return

            # Ocena dla pomiaru ciągłości
            continuity_evaluation = "NIE"
            try:
                measured_value = float(continuity_measured)
                selected_cable = self.continuity_cable_combo.currentText().strip()
                cable_length_text = self.continuity_length_input.text().strip()
                if cable_length_text and float(cable_length_text) > 0:
                    cable_length_m = float(cable_length_text)
                    resistivity = self.PRZEWODY.get(selected_cable) / 1000
                    resistance_contacts = 0.05
                    reference_value = resistivity * cable_length_m + resistance_contacts
                    if measured_value <= reference_value * 1.25:
                        continuity_evaluation = "TAK"
            except (ValueError, KeyError):
                pass

            # Przygotowanie danych do PDF
            elements = []
            styles = getSampleStyleSheet()

            # Styl dla tytułu
            title_style = ParagraphStyle('Title', parent=styles['Normal'])
            title_style.fontName = 'DejaVuSans-Bold'
            title_style.alignment = 1
            title_style.fontSize = 16

            # Styl dla nagłówków sekcji
            heading_style = ParagraphStyle('Heading', parent=styles['Normal'])
            heading_style.fontSize = 12
            heading_style.fontName = 'DejaVuSans-Bold'
            heading_style.spaceAfter = 10

            # Styl dla normalnego tekstu
            normal_style = ParagraphStyle('Normal', parent=styles['Normal'])
            normal_style.fontName = 'DejaVuSans'

            # Styl dla podtytułu
            subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'])
            subtitle_style.fontName = 'DejaVuSans-Bold'
            subtitle_style.fontSize = 12

            # Ustawienie szerokości tabeli na całą stronę (z marginesami)
            page_width = 17 * cm

            # Tytuł (przesunięty wyżej)
            elements.append(Spacer(1, -1.0 * cm))
            elements.append(Paragraph("Protokół pomiarów elektrycznych", title_style))
            elements.append(Spacer(1, 0.5 * cm))

            elements.append(Paragraph(" ", normal_style))

            # przed użyciem styles:
            device_name = getattr(self, "device_name", None)
            # jako dodatkowy fallback można odczytać bezpośrednio z widgetu:
            if not device_name and hasattr(self, "device_name_input"):
                device_name = self.device_name_input.text().strip() or None
            if device_name:
                device_style = ParagraphStyle('Device', parent=styles['Normal'], fontName='DejaVuSans',  fontSize=12, spaceAfter=6)
                elements.append(Paragraph(f"<b>Urządzenia:</b> {device_name}", device_style))


            # Dane wykonawców
            elements.append(Paragraph("<b>                      </b>", heading_style))
            elements.append(Spacer(1, 0.5 * cm))

            # Lokalizacja pomiaru
            elements.append(Paragraph("Lokalizacja pomiaru:", normal_style))
            elements.append(Paragraph(lokalizacja.replace('\n', '<br/>'), normal_style))
            elements.append(Spacer(1, 0.5 * cm))

            # Poprawiony blok dla "Badania:"
            badania_text = """<b>Badania:</b><br/>1.  Oględziny montażu urządzenia<br/>2.  Wyniki pomiarów rezystancji izolacji<br/>3.  Wyniki pomiarów impedancji pętli zwarcia<br/>4.  Wyniki pomiarów ciągłości połączeń wyrównawczych<br/>5.  Uwagi."""
            badania_paragraph = Paragraph(badania_text, normal_style)
            elements.append(badania_paragraph)
            elements.append(Spacer(1, 0.5 * cm))

            # Tabela z danymi ogólnymi - ZMODYFIKOWANY NAGŁÓWEK
            elements.append(Paragraph("<b>Dane ogólne</b>", heading_style))

            # Rozdzielenie tekstu na podstawie przecinków
            # Użycie maxsplit=2 zapewnia, że podział nastąpi tylko 2 razy
            nowa_zmienna = przyrzad_pomiarowy
            split_parts = nowa_zmienna.split(',', 2)

            # Złożenie tekstu z podziałem na linie
            # Użycie <br/> w ReportLab tworzy nową linię
            processed_text = ""
            if len(split_parts) > 0:
                processed_text += split_parts[0].strip()
            if len(split_parts) > 1:
                processed_text += "<br/>" + split_parts[1].strip()
            if len(split_parts) > 2:
                processed_text += "<br/>" + split_parts[2].strip()

            # Nowy styl dla wyśrodkowanego tekstu w tabeli
            centered_table_style = ParagraphStyle('CenteredTableText', parent=normal_style)
            centered_table_style.alignment = 1  # 1 = CENTER

            # Utworzenie nowej tabeli z przetworzoną wartością
            general_data_table = [
                ['Napięcie probiercze Riso [V]', napiecie_probiercze],
                ['Temperatura otoczenia [°C]', temp_otoczenia],
                ['Data wykonania pomiarów', data_pomiarow],
                ['Przyrząd pomiarowy', Paragraph(processed_text, centered_table_style)],
                # Użycie Paragraph do renderowania tekstu z <br/>
                ['Rodzaj sieci', rodzaj_sieci]
            ]
            general_table = Table(general_data_table, colWidths=[8.5 * cm, 8.5 * cm])
            general_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER', 'MIDDLE'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (0, -1), 'DejaVuSans-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'DejaVuSans'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            elements.append(general_table)
            elements.append(Spacer(1, 0.5 * cm))

            # Tabela 1. Oględziny montażu urządzenia
            elements.append(Paragraph("<b>1. Oględziny montażu urządzenia</b>", heading_style))
            oględziny_data_control = [
                ['Lp.', 'Przedmiot oględzin', 'Ocena (Tak/Nie)'],
                ['1', Paragraph("Spełniono wymagania bezpieczeństwa zgodnie z wymaganiami przepisów", normal_style),
                 'TAK'],
                ['2', Paragraph("Brak uszkodzeń pogarszających bezpieczeństwo", normal_style), 'TAK'],
                ['3',
                 Paragraph("Zastosowano właściwy sposób ochrony przed porażeniem prądem elektrycznym", normal_style),
                 'TAK'],
                ['4', Paragraph("Właściwie dobrano i oznaczono przewody ochronne, neutralne i fazowe", normal_style),
                 'TAK'],
                ['5', Paragraph("Właściwie dobrano i oznaczono zabezpieczenia i aparaturę", normal_style), 'TAK'],
                ['6',
                 Paragraph("Zapewniono dostęp do urządzeń dla wygodnej obsługi, konserwacji i napraw", normal_style),
                 'TAK']
            ]
            oględziny_table_control = Table(oględziny_data_control, colWidths=[1.5 * cm, 11.5 * cm, 4 * cm])
            oględziny_table_control.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER', 'MIDDLE'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
                ('FONTNAME', (0, 1), (0, -1), 'DejaVuSans'),
                ('FONTNAME', (2, 1), (2, -1), 'DejaVuSans'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('ALIGN', (1, 1), (1, -1), 'LEFT', 'MIDDLE'),
            ]))
            elements.append(oględziny_table_control)
            elements.append(Spacer(1, 0.5 * cm))

            # Pomiar rezystancji izolacji - ZMODYFIKOWANA TABELA
            elements.append(Paragraph("<b>2. Pomiar rezystancji izolacji</b>", heading_style))

            # Definicja szerokości kolumn (razem ~22.5 cm, więc dobrze dopasować do doc.width)
            iso_data = [
                [Paragraph("<b>Obwody trójfazowe:</b>", normal_style)],
                ['Lp.', 'L1-PE\n[MΩ]', 'L2-PE\n[MΩ]', 'L3-PE\n[MΩ]', 'L1-N\n[MΩ]', 'L2-N\n[MΩ]', 'L3-N\n[MΩ]',
                 'L1-L2\n[MΩ]', 'L1-L3\n[MΩ]', 'L2-L3\n[MΩ]', 'N-PE\n[MΩ]', 'RW\n[MΩ]', 'Ocena \n(Tak/Nie)'],
                ['1'] + [f">{v}" for v in iso_values.values()] + [f"{iso_evaluation}"]
            ]

            col_widths = [
                0.8 * cm,  # Lp.
                1.4 * cm, 1.4 * cm, 1.4 * cm,  # L1-PE, L2-PE, L3-PE
                1.4 * cm, 1.4 * cm, 1.4 * cm,  # L1-N, L2-N, L3-N
                1.4 * cm, 1.4 * cm, 1.4 * cm,  # L1-L2, L1-L3, L2-L3
                1.4 * cm,  # N-PE
                1.3 * cm,  # RW
                1.9 * cm  # Ocena
            ]

            iso_table = Table(iso_data, colWidths=col_widths)

            iso_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('GRID', (0, 1), (-1, -1), 0.25, colors.black),  # kratki dopiero od 2. wiersza
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                # scalanie pierwszego wiersza na wszystkie 13 kolumn
                ('SPAN', (0, 0), (12, 0)),

                # czcionki i rozmiar
                ('FONTNAME', (0, 0), (-1, 1), 'DejaVuSans-Bold'),
                ('FONTNAME', (0, 2), (-1, 2), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, -1), 8)
            ]))

            elements.append(iso_table)
            elements.append(Spacer(1, 0.5 * cm))

            # Pomiar impedancji pętli zwarcia
            elements.append(PageBreak())  # <<< DODANE – wymusza przejście na nową stronę
            elements.append(Paragraph("<b>3. Pomiar impedancji pętli zwarcia</b>", heading_style))


            # Zmodyfikowane nagłówki i szerokości kolumn
            impedance_headers = [
                'Lp.', 'Symbol', 'Typ zabezpieczenia', 'In [A]', 'Ta [s]', 'Ia [A]', 'Isc [kA]', 'Zd [Ω]', 'Zz [Ω]',
                'Ocena'
            ]
            impedance_table_data = [impedance_headers] + impedance_data

            # Zwiększona szerokość kolumny "Typ zabezpieczenia"
            col_widths = [
                0.7 * cm,  # Lp
                1.5 * cm,  # Symbol
                3.5 * cm,  # Typ zabezpieczenia (zwiększone z 3.0)
                1.5 * cm,  # In
                1.5 * cm,  # Ta
                2.0 * cm,  # Ia
                2.0 * cm,  # Isc
                2.0 * cm,  # Zd
                2.0 * cm,  # Zz
                1.5 * cm  # Ocena
            ]

            impedance_table = Table(impedance_table_data, colWidths=col_widths)

            impedance_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER', 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
            elements.append(impedance_table)

            elements.append(Spacer(1, 0.5 * cm))

            descriptions = [
                "In – Prąd znamionowy zabezpieczenia",
                "Ta – Czas zadziałania",
                "Ia – Prąd zwarciowy wyliczony z charakterystyki zabezpieczenia",
                "Isc – Obliczeniowy prąd zwarciowy",
                "Zd – Impedancja dopuszczalna",
                "Zz – Impedancja zmierzona"
            ]
            for desc in descriptions:
                elements.append(Paragraph(desc, normal_style))
            elements.append(Spacer(1, 0.5 * cm))

            # Pomiar ciągłości
            elements.append(Paragraph("<b>4. Pomiar ciągłości połączeń wyrównawczych</b>", heading_style))
            continuity_data = [
                ["Lp.", "Symbol", "Zmierzona rezystancja", "Ocena"],
                ["1", "Połączenia wyrównawcze", f"{continuity_measured} Ω", continuity_evaluation]
            ]

            # Zwiększona szerokość kolumny "Symbol"
            continuity_col_widths = [
                1.5 * cm,  # Lp.
                7.5 * cm,  # Symbol (zwiększone, aby zmieścić tekst)
                5 * cm,  # Zmierzona rezystancja
                3.0 * cm  # Ocena
            ]

            continuity_table = Table(continuity_data, colWidths=continuity_col_widths)

            continuity_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER', 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
            elements.append(continuity_table)
            elements.append(Spacer(1, 0.5 * cm))

            # Sekcja Uwagi
            elements.append(Paragraph("<b>5. Uwagi</b>", heading_style))
            elements.append(Paragraph(notes, normal_style))
            elements.append(Spacer(1, 0.5 * cm))

            # Dane wykonawców
            elements.append(Paragraph("<b>                      </b>", heading_style))
            elements.append(Spacer(1, 0.5 * cm))

            # Układ tabeli dla wykonawcy i sprawdzającego (po lewej i prawej)
            signatures_data = [
                [
                    Paragraph(f"Badania wykonał:<br/>{executor}", normal_style),
                    Paragraph(f"Sprawdził:<br/>{reviewer}", normal_style)
                ]
            ] if podpis_sprawdzajacego else [
                [
                    Paragraph(f"Badania wykonał:<br/>{executor}", normal_style),
                    Paragraph(f"Sprawdził: {reviewer}", normal_style)
                ]
            ]

            signatures_table = Table(signatures_data, colWidths=[8.5 * cm, 8.5 * cm])
            signatures_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Wykonawca po lewej
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Sprawdzający po prawej
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (1, 0), (1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
            ]))
            elements.append(signatures_table)
            elements.append(Spacer(1, 0.5 * cm))

            # Dodanie podpisu sprawdzającego, jeśli jest zaznaczone
            if podpis_sprawdzajacego:
                # Użycie re, aby znaleźć imię i nazwisko (dwóch słów przed drugą spacją)
                reviewer_name_match = re.search(r'^(\S+\s\S+)', reviewer)
                if reviewer_name_match:
                    reviewer_name = reviewer_name_match.group(1)
                else:
                    # Jeśli standardowy format nie pasuje, użyj całości
                    reviewer_name = reviewer

                signature_path = f"{reviewer_name}.png"

                # Sprawdzenie, czy plik podpisu istnieje, aby uniknąć błędów
                if os.path.exists(signature_path):
                    # Stworzenie obiektu obrazka
                    signature_image = Image(signature_path, width=5 * cm, height=5 * cm)

                    # Ustawienie obrazka do wyświetlenia w prawej części strony
                    signature_image.hAlign = 'RIGHT'
                    elements.append(signature_image)
                else:
                    QMessageBox.warning(self, "Brak pliku", f"Plik podpisu '{signature_path}' nie został znaleziony.")

            # Tworzenie dokumentu i obsługa błędów zapisu
            try:
                doc = SimpleDocTemplate("protokol_pomiaru.pdf", pagesize=A4)
                doc.build(elements)
                QMessageBox.information(self, "Sukces",
                                        "Protokół w formacie PDF został wygenerowany pomyślnie i zapisany w katalogu z programem.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd",
                                     f"Wystąpił błąd podczas generowania protokołu: {e}\nSprawdź, czy masz uprawnienia do zapisu w tym katalogu.")

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas generowania protokołu: {e}")

    def verify_continuity_evaluation(self):
        """Pomocnicza metoda do oceny ciągłości dla PDF."""
        try:
            measured_value = float(self.continuity_measured_input.text().strip())
            selected_cable = self.continuity_cable_combo.currentText().strip()
            cable_length_text = self.continuity_length_input.text().strip()
            if not cable_length_text or not selected_cable or measured_value < 0:
                return False
            cable_length_m = float(cable_length_text)
            resistivity = self.PRZEWODY.get(selected_cable) / 1000
            resistance_contacts = 0.05
            reference_value = resistivity * cable_length_m + resistance_contacts
            return measured_value <= reference_value * 1.25
        except (ValueError, KeyError):
            return False

class ImpedanceCalculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kalkulator impedancji pętli zwarcia")
        #self.setGeometry(200, 200, 400, 300)
        #self.setFixedSize(400, 300)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Pola do wprowadzania danych
        self.transformer_length_input = QLineEdit()
        self.transformer_cross_section_input = QLineEdit()
        self.material_combo = QComboBox()
        self.material_combo.addItems(["Miedź", "Aluminium"])
        self.device_length_input = QLineEdit()
        self.device_cross_section_input = QLineEdit()
        self.contact_resistance_input = QLineEdit()

        # Dodanie pól do layoutu
        self.form_layout.addRow("Długość od transformatora\ndo rozdzielni\przyłącza [m]:", self.transformer_length_input)
        self.form_layout.addRow("Przekrój od przewodów kablowych\n od transformatora[mm²]:", self.transformer_cross_section_input)
        self.form_layout.addRow("Rodzaj materiału przewodów kablowych w sieci:", self.material_combo)
        self.form_layout.addRow("Długość przewodów kablowych od urządzenia [m]:", self.device_length_input)
        self.form_layout.addRow("Przekrój przewodów kablowych od urządzenia [mm²]:", self.device_cross_section_input)
        self.form_layout.addRow("Rezystancja styków , zazwyczaj od 0.001 do 0.1 [Ω]:", self.contact_resistance_input)

        self.layout.addLayout(self.form_layout)

        # Przycisk "Licz"
        self.calculate_button = QPushButton("Licz")
        self.calculate_button.clicked.connect(self.calculate_Zz)
        self.layout.addWidget(self.calculate_button)

        # Etykieta do wyświetlania wyniku
        self.result_label = QLabel("Impedancja pętli zwarcia: ")
        self.layout.addWidget(self.result_label)

    def calculate_Zz(self):
        try:
            # Stałe
            rho_copper = 0.01724  # Ω·mm²/m
            rho_aluminium = 0.0282  # Ω·mm²/m
            xl_unit = 0.08 / 1000 # mΩ/m na Ω/m

            # Pobranie danych
            L1 = float(self.transformer_length_input.text())
            S1 = float(self.transformer_cross_section_input.text())
            L2 = float(self.device_length_input.text())
            S2 = float(self.device_cross_section_input.text())
            R_contacts = float(self.contact_resistance_input.text())
            material = self.material_combo.currentText()

            # Wybór rezystywności dla kabla od transformatora
            rho1 = rho_copper if material == "Miedź" else rho_aluminium

            # Obliczenie rezystancji i reaktancji dla pierwszego odcinka
            R1 = (rho1 * L1) / S1
            X1 = xl_unit * L1

            # Obliczenie rezystancji i reaktancji dla drugiego odcinka (zawsze miedź)
            R2 = (rho_copper * L2) / S2
            X2 = xl_unit * L2

            # Całkowita impedancja pętli
            # Zz = sqrt((2 * (R1 + R2) + R_contacts)^2 + (2 * (X1 + X2))^2)
            R_total = 2 * (R1 + R2) + R_contacts
            X_total = 2 * (X1 + X2)
            Zz_calculated = (R_total**2 + X_total**2)**0.5

            # Wyświetlenie wyniku
            self.result_label.setText(f"Impedancja pętli zwarcia: {Zz_calculated:.4f} Ω")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")

        except ValueError:
            QMessageBox.warning(self, "Błąd danych", "Wprowadź poprawne wartości liczbowe.")
            self.result_label.setText("Impedancja pętli zwarcia: Błąd")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

        except ValueError:
            QMessageBox.warning(self, "Błąd danych", "Wprowadź poprawne wartości liczbowe.")
            self.result_label.setText("Impedancja pętli zwarcia: Błąd")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProtocolGeneratorApp()
    window.show()
    sys.exit(app.exec())