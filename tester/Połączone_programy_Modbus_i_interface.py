import sys
import csv
import serial.tools.list_ports
import math
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QFrame, QGridLayout, \
    QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QAbstractItemView, QRadioButton, \
    QButtonGroup, QLineEdit, QDialog, QTextEdit, QMessageBox
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
from pymodbus.client.sync import ModbusSerialClient
import struct
import time
from PySide6.QtCore import QTimer
import sys
import serial
import serial.tools.list_ports

# Stałe używane do obliczeń
VOLTAGE_1_PHASE = 230  # V
FREQUENCY = 50  # Hz

#zmienne globalne
global_u1 = 0.0
global_u2 = 0.0
global_u3 = 0.0
global_u12 = 0.0
global_u23 = 0.0
global_u31 = 0.0
global_u_avg = 0.0

# Zmienna globalna dla COM drugiego urządzenia
COM = None
polaczono_z_Novar = None



# Funkcja do wczytywania CSV
def load_csv(file_path):
    items = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True)
            for row in reader:
                if row:
                    items.append(row)
    except FileNotFoundError:
        print(f"Plik {file_path} nie znaleziony!")
    return items


# Funkcja do zapisywania listy do CSV
def save_csv(file_path, items):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for item in items:
                writer.writerow(item)
    except IOError as e:
        print(f"Błąd zapisu do pliku {file_path}: {e}")


# Funkcja do zaokrąglania do najbliższej wartości ze standardowej listy
def find_nearest_standard_value(calculated_value, standard_values):
    """
    Znajduje najbliższą wartość z listy standardowych wartości.
    W przypadku równych odległości, wybiera wartość wyższą.
    """
    if not standard_values:
        return calculated_value

    # Sortowanie listy, aby ułatwić wyszukiwanie
    standard_values.sort()

    nearest_value = standard_values[0]
    min_difference = abs(calculated_value - nearest_value)

    for value in standard_values:
        difference = abs(calculated_value - value)
        if difference < min_difference:
            min_difference = difference
            nearest_value = value
        elif difference == min_difference:
            # W przypadku równych odległości, wybieramy wartość wyższą
            nearest_value = max(nearest_value, value)

    return nearest_value


# --- KLASA DO ODCZYTU MODBUS W OSOBNYM WĄTKU ---
class ModbusReader(QThread):
    data_ready = Signal(dict)
    connection_status = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True
        self.client = None
        self.slave_id = 1
        # Rejestry dla wartości aktualnych
        self.volt_regs = {"U1": 4352, "U2": 4354, "U3": 4356}
        self.curr_regs = {"I1": 4608, "I2": 4610, "I3": 4612}
        self.reactive_regs = {"Q1": 4868, "Q2": 4870, "Q3": 4872}

    def run(self):
        global polaczono_z_Novar
        self.client = ModbusSerialClient(
            method="rtu",
            port=self.port,
            baudrate=9600,
            stopbits=1,
            bytesize=8,
            parity="N",
            timeout=1
        )
        if self.client.connect():
            self.connection_status.emit("Połączono z Novar 2700")
            polaczono_z_Novar = "connected"
            print(f"zapis do zmiennej : polaczono_z_Novar={polaczono_z_Novar}")
            while self.running:
                try:
                    data = {}
                    for name, addr in self.volt_regs.items():
                        data[name] = self.read_float(addr)
                    for name, addr in self.curr_regs.items():
                        data[name] = self.read_float(addr)
                    for name, addr in self.reactive_regs.items():
                        data[name] = self.read_float(addr)
                    self.data_ready.emit(data)
                except Exception as e:
                    print(f"Błąd odczytu: {e}")
                    self.connection_status.emit("Błąd odczytu danych!")
                    break
                time.sleep(1)
            self.client.close()
            self.connection_status.emit("Rozłączono")
            polaczono_z_Novar = "noconnected"
            print(f"zapis do zmiennej : polaczono_z_Novar={polaczono_z_Novar}")
        else:
            self.connection_status.emit("❌ Błąd połączenia!")
            polaczono_z_Novar = "noconnected"
            print(f"zapis do zmiennej : polaczono_z_Novar={polaczono_z_Novar}")

    def stop(self):
        self.running = False
        self.wait()

    def read_float(self, address):
        try:
            rr = self.client.read_input_registers(address=address, count=2, unit=self.slave_id)
            if rr.isError():
                return None
            return struct.unpack('>f', struct.pack('>HH', rr.registers[0], rr.registers[1]))[0]
        except Exception:
            return None

class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proces Testowania")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        label = QLabel("Start testowanie podzespołu")
        layout.addWidget(label)

        # Pole do wyświetlania logów (wysyłane i odbierane komendy)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Przyciski do wysyłania komend
        self.btn_start1 = QPushButton("Wyślij 'start1'")
        self.btn_start1.clicked.connect(lambda: self.send_command("start1"))
        layout.addWidget(self.btn_start1)

        self.btn_stop1 = QPushButton("Wyślij 'stop1'")
        self.btn_stop1.clicked.connect(lambda: self.send_command("stop1"))
        layout.addWidget(self.btn_stop1)

        self.btn_start2 = QPushButton("Wyślij 'start2'")
        self.btn_start2.clicked.connect(lambda: self.send_command("start2"))
        layout.addWidget(self.btn_start2)

        self.btn_stop2 = QPushButton("Wyślij 'stop2'")
        self.btn_stop2.clicked.connect(lambda: self.send_command("stop2"))
        layout.addWidget(self.btn_stop2)

        self.setLayout(layout)

        # Serial
        self.ser = None
        self.open_serial()

        # Timer do odbioru danych
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)  # co 100 ms sprawdzaj port

    def open_serial(self):
        global COM
        try:
            self.ser = serial.Serial(COM, 9600, timeout=0.1)
            self.log_text.append(f"Połączono z portem {COM}")
        except Exception as e:
            self.log_text.append(f"Nie udało się otworzyć portu {COM}: {e}")

    def send_command(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())  # wysyłanie z końcem linii
            self.log_text.append(f"Wysłano komendę: {cmd}")
        else:
            self.log_text.append("Port nieotwarty!")

    def read_serial(self):
        if self.ser and self.ser.in_waiting:
            try:
                data = self.ser.readline().decode().strip()
                if data:
                    self.log_text.append(f"Odebrano: {data}")
            except Exception as e:
                self.log_text.append(f"Błąd odczytu: {e}")

# --- KLASA DEDYKOWANA DLA OKNA DODAWANIA NOWEGO ELEMENTU ---
class AddElementWindow(QDialog):
    # Lista standardowych wartości mocy w kvar dla dławików 1-fazowych
    STANDARD_KVAR_VALUES_1P = sorted(list(set([
        0.02, 0.04, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.33, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9,
        1.0, 1.25, 1.3, 1.5, 1.66, 1.75, 2.0, 2.25, 2.5, 3.0, 3.25, 3.33, 3.5, 4.0, 5.0, 6.66, 10.0
    ])))

    # Lista standardowych wartości mocy w kvar dla dławików 3-fazowych
    STANDARD_KVAR_VALUES_3P = sorted(list(set([
        0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 75.0,
        100.0, 125.0, 150.0, 200.0, 250.0, 300.0
    ])))

    # Lista standardowych wartości mocy w kvar dla kondensatorów 1-fazowych
    STANDARD_KVAR_VALUES_CAP_1P = sorted(list(set([
        0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0
    ])))

    # Nowa lista z parami wartości (400V, 440V)
    STANDARD_KVAR_VALUES_CAP_3P = sorted(
        [[1, 1.25], [2, 2.5], [2.5, 3], [3, 3.75], [4, 5], [5.0, 6.25], [6.25, 7.5], [8, 10], [10.0, 12.5],
         [12.5, 15.0], [15.0, 18.2], [16, 20], [20.0, 25], [23, 28], [25.0, 30.0], [32, 40.0], [40.0, 50.0]],
        key=lambda x: x[0]
    )

    # Mapowanie producentów dla każdego typu komponentu
    MANUFACTURERS_MAP = {
        "dławik 1 fazowy": ["ABB", "Siemens", "Schneider"],
        "dławik 3 fazowy": ["ABB", "Schneider", "Eaton"],
        "kondensator 1 fazowy": ["Wima", "EPCOS", "Kemet"],
        "kondensator 3 fazowy": ["EPCOS", "Kemet", "Legrand"]
    }

    def __init__(self, parent=None, tab_name=""):
        super().__init__(parent)
        self.setWindowTitle("Dodaj nowy element")
        self.setGeometry(100, 100, 400, 300)
        self.tab_name = tab_name
        self.input_fields = {}
        self.radio_buttons = {}

        main_layout = QVBoxLayout(self)

        # Sekcja Radio Buttons
        radio_group_box = QGroupBox("Wybierz typ komponentu:")
        radio_layout = QVBoxLayout(radio_group_box)

        self.radio_buttons_map = {
            "dławik 1 fazowy": "1-fazowe_dławiki",
            "dławik 3 fazowy": "3-fazowe_dławiki",
            "kondensator 1 fazowy": "1-fazowe_kondensatory",
            "kondensator 3 fazowy": "3-fazowe_kondensatory"
        }

        button_group = QButtonGroup(self)

        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_container)

        def update_fields(button):
            self.clear_fields_layout()
            if button.isChecked():
                self.create_input_fields(button.text())

        for name, file_name in self.radio_buttons_map.items():
            radio_button = QRadioButton(name)
            radio_layout.addWidget(radio_button)
            button_group.addButton(radio_button)
            self.radio_buttons[name] = radio_button
            if file_name == self.tab_name:
                radio_button.setChecked(True)
            radio_button.toggled.connect(lambda state, btn=radio_button: update_fields(btn) if state else None)

        main_layout.addWidget(radio_group_box)
        main_layout.addWidget(self.fields_container)

        # Przycisk "Dodaj element do listy"
        add_to_list_button = QPushButton("Dodaj element do listy")
        add_to_list_button.setDefault(False)
        add_to_list_button.setAutoDefault(False)
        add_to_list_button.clicked.connect(self.add_item_to_list)
        main_layout.addWidget(add_to_list_button)

        # Inicjalne wstawienie pól na podstawie domyślnie zaznaczonego przycisku
        initial_component_type = list(self.radio_buttons_map.keys())[
            list(self.radio_buttons_map.values()).index(self.tab_name)]
        self.create_input_fields(initial_component_type)

    def add_item_to_list(self):
        print("Funkcja 'add_item_to_list' została wywołana.")

        # Dławik 1-fazowy
        if self.radio_buttons["dławik 1 fazowy"].isChecked():
            try:
                # Pobierz producenta
                manufacturer_name = self.input_fields["Producent"].currentText()

                # Pobierz wartości z pól tekstowych
                calculated_power = self.input_fields["Moc obliczona"].text()
                manufacturer_power = self.input_fields["Moc podana przez producenta"].text()
                inductance = self.input_fields["Indukcyjność"].text()


                # Sprawdź, czy wartości są poprawne
                if not calculated_power or not manufacturer_power or not inductance or "Błąd" in calculated_power:
                    print("Nie można dodać elementu: brak danych lub błąd w obliczeniach.")
                    return

                # Utwórz listę wartości do zapisania w pliku CSV
                new_item = [manufacturer_power, inductance, calculated_power,manufacturer_name]

                # Zapisz do pliku i odśwież widoki
                file_path = "ind_1f.csv"
                self.parent().add_and_refresh(file_path, new_item)

            except KeyError:
                print("Błąd: Prawdopodobnie brak wymaganych pól do pobrania.")

        # Dławik 3-fazowy
        elif self.radio_buttons["dławik 3 fazowy"].isChecked():
            try:

                # Pobierz producenta
                manufacturer_name = self.input_fields["Producent"].currentText()

                # Pobierz wartości z pól tekstowych
                calculated_power = self.input_fields["Moc obliczona"].text()
                manufacturer_power = self.input_fields["Moc podana przez producenta"].text()
                inductance = self.input_fields["Indukcyjność"].text()

                # Sprawdź, czy wartości są poprawne
                if not calculated_power or not manufacturer_power or not inductance or "Błąd" in calculated_power:
                    print("Nie można dodać elementu: brak danych lub błąd w obliczeniach.")
                    return

                # Utwórz listę wartości do zapisania w pliku CSV
                new_item = [manufacturer_power, inductance, calculated_power, manufacturer_name]

                # Zapisz do pliku i odśwież widoki
                file_path = "ind_3f.csv"
                self.parent().add_and_refresh(file_path, new_item)

            except KeyError:
                print("Błąd: Prawdopodobnie brak wymaganych pól do pobrania.")

        # Kondensator 1-fazowy
        elif self.radio_buttons["kondensator 1 fazowy"].isChecked():
            try:

                # Pobierz producenta
                manufacturer_name = self.input_fields["Producent"].currentText()

                # Pobierz wartości z pól tekstowych
                calculated_power = self.input_fields["Moc obliczona"].text()
                manufacturer_power = self.input_fields["Moc podana przez producenta"].text()
                capacitance = self.input_fields["Pojemność"].text()

                # Sprawdź, czy wartości są poprawne
                if not calculated_power or not manufacturer_power or not capacitance or "Błąd" in calculated_power:
                    print("Nie można dodać elementu: brak danych lub błąd w obliczeniach.")
                    return

                # Utwórz listę wartości do zapisania w pliku CSV
                new_item = [manufacturer_power, capacitance, calculated_power, manufacturer_name]

                # Zapisz do pliku i odśwież widoki
                file_path = "cond_1f.csv"
                self.parent().add_and_refresh(file_path, new_item)

            except KeyError:
                print("Błąd: Prawdopodobnie brak wymaganych pól do pobrania.")

        # Kondensator 3-fazowy
        elif self.radio_buttons["kondensator 3 fazowy"].isChecked():
            try:

                # Pobierz producenta
                manufacturer_name = self.input_fields["Producent"].currentText()

                # Pobierz wartości z pól tekstowych
                capacitance = self.input_fields["Pojemność"].text()
                manufacturer_power_400V = self.input_fields["Moc podana przez producenta przy 400V"].text()
                calculated_power_400V = self.input_fields["Moc obliczona przy 400V"].text()
                manufacturer_power_440V = self.input_fields["Moc podana przez producenta przy 440V"].text()
                calculated_power_440V = self.input_fields["Moc obliczona przy 440V"].text()

                # Sprawdź, czy wartości są poprawne
                if not capacitance or "Błąd" in calculated_power_400V or "Błąd" in calculated_power_440V:
                    print("Nie można dodać elementu: brak danych lub błąd w obliczeniach.")
                    return

                # Utwórz listę wartości do zapisania w pliku CSV w zmienionej kolejności
                new_item = [manufacturer_power_440V, manufacturer_power_400V, capacitance, calculated_power_400V,
                            calculated_power_440V, manufacturer_name]

                # Zapisz do pliku i odśwież widoki
                file_path = "cond_3f.csv"
                self.parent().add_and_refresh(file_path, new_item)

            except KeyError:
                print("Błąd: Prawdopodobnie brak wymaganych pól do pobrania.")

    def clear_fields_layout(self):
        self.input_fields = {}
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def create_input_fields(self, component_type):
        fields_map = {
            "dławik 1 fazowy": ["Indukcyjność", "Moc obliczona", "Moc podana przez producenta"],
            "dławik 3 fazowy": ["Indukcyjność", "Moc obliczona", "Moc podana przez producenta"],
            "kondensator 1 fazowy": ["Pojemność", "Moc obliczona", "Moc podana przez producenta"],
            "kondensator 3 fazowy": ["Pojemność", "Moc obliczona przy 400V", "Moc podana przez producenta przy 400V",
                                     "Moc obliczona przy 440V", "Moc podana przez producenta przy 440V"]
        }

        if component_type in fields_map:
            for field_name in fields_map[component_type]:
                h_layout = QHBoxLayout()
                h_layout.addWidget(QLabel(f"{field_name}:"))
                line_edit = QLineEdit()
                h_layout.addWidget(line_edit)
                self.input_fields[field_name] = line_edit
                self.fields_layout.addLayout(h_layout)

            # Utworzenie pola wyboru producenta
            manufacturer_label = QLabel("Producent:")
            manufacturer_combo = QComboBox()
            manufacturer_combo.addItems(self.MANUFACTURERS_MAP.get(component_type, []))
            self.input_fields["Producent"] = manufacturer_combo

            h_layout = QHBoxLayout()
            h_layout.addWidget(manufacturer_label)
            h_layout.addWidget(manufacturer_combo)
            self.fields_layout.addLayout(h_layout)

            # Połączenie sygnałów
            if component_type == "dławik 1 fazowy":
                self.input_fields["Indukcyjność"].returnPressed.connect(self.calculate_power_from_inductance)
                self.input_fields["Moc obliczona"].returnPressed.connect(self.calculate_inductance_from_power)
            elif component_type == "dławik 3 fazowy":
                self.input_fields["Indukcyjność"].returnPressed.connect(self.calculate_power_from_3phase_inductor)
                self.input_fields["Moc obliczona"].returnPressed.connect(self.calculate_inductance_from_3phase_power)
            elif component_type == "kondensator 1 fazowy":
                self.input_fields["Pojemność"].returnPressed.connect(self.calculate_power_from_capacitance)
                self.input_fields["Moc obliczona"].returnPressed.connect(self.calculate_capacitance_from_power)
            elif component_type == "kondensator 3 fazowy":
                self.input_fields["Pojemność"].returnPressed.connect(self.calculate_all_3phase_capacitor_powers)
                self.input_fields["Moc obliczona przy 400V"].returnPressed.connect(
                    self.calculate_all_3phase_capacitor_capacitances_from_400V)
                self.input_fields["Moc obliczona przy 440V"].returnPressed.connect(
                    self.calculate_all_3phase_capacitor_capacitances_from_440V)

    def calculate_three_phase_inductor_power(self, L_mH, U, fn):
        """
        Oblicza całkowitą moc bierną dławika trójfazowego,
        zakładając połączenie w gwiazdę.
        """
        # Przeliczenie indukcyjności z mH na H
        L_H = L_mH * 1e-3

        # Obliczenie reaktancji na fazę
        XL = 2 * math.pi * fn * L_H

        # Obliczenie napięcia fazowego (dla połączenia w gwiazdę)
        U_phase = U / math.sqrt(3)

        # Obliczenie mocy na fazę
        Q_phase = (U_phase ** 2) / XL

        # Obliczenie całkowitej mocy (razy 3 fazy)
        Q_total = 3 * Q_phase

        # Przeliczenie na kVar
        Q_total_kvar = Q_total / 1000

        return Q_total_kvar

    def calculate_three_phase_capacitor_power(self, C_uF, U, fn):
        """
        Oblicza całkowitą moc kondensatora w połączeniu w trójkąt, przyjmując pojemność w µF.
        Zgodnie z wzorem podanym przez użytkownika, który jest z książki o kompensacji mocy biernej.

        Args:
          C_uF (float): Pojemność pojedynczego kondensatora w mikrofaradach (µF).
          U (float): Napięcie międzyfazowe w woltach (V).
          fn (float): Częstotliwość w hercach (Hz).

        Returns:
          float: Całkowita moc kondensatora w kilovoltamperach reaktywnych (kVar).
        """
        C_F = C_uF * 1e-6
        Qc = 3 * C_F * (U ** 2) * 2 * math.pi * fn
        Qc_kvar = Qc / 1000
        return Qc_kvar

    def calculate_all_3phase_capacitor_powers(self):
        try:
            C_uF = float(self.input_fields["Pojemność"].text().replace(',', '.'))

            Qc_400V_kvar = self.calculate_three_phase_capacitor_power(C_uF, 400, FREQUENCY)
            Qc_440V_kvar = self.calculate_three_phase_capacitor_power(C_uF, 440, FREQUENCY)

            # Szukanie najbliższej wartości z par na podstawie mocy 440V
            closest_pair = min(self.STANDARD_KVAR_VALUES_CAP_3P, key=lambda x: abs(x[1] - Qc_440V_kvar))

            rounded_kvar_400V = closest_pair[0]
            rounded_kvar_440V = closest_pair[1]

            self.input_fields["Moc obliczona przy 400V"].setText(f"{Qc_400V_kvar:.2f}")
            self.input_fields["Moc podana przez producenta przy 400V"].setText(f"{rounded_kvar_400V}")
            self.input_fields["Moc obliczona przy 440V"].setText(f"{Qc_440V_kvar:.2f}")
            self.input_fields["Moc podana przez producenta przy 440V"].setText(f"{rounded_kvar_440V}")

        except ValueError:
            self.input_fields["Moc obliczona przy 400V"].setText("Błąd!")
            self.input_fields["Moc obliczona przy 440V"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Moc obliczona przy 400V"].setText("0")
            self.input_fields["Moc obliczona przy 440V"].setText("0")

    def calculate_capacitance_from_3phase_power(self, Qc_kvar, U, fn):
        """
        Oblicza pojemność kondensatora 3-fazowego na podstawie mocy,
        używając wzoru odwrotnego do podanego przez użytkownika.
        """
        Qc = Qc_kvar * 1000
        C_F = Qc / (3 * (U ** 2) * 2 * math.pi * fn)
        C_uF = C_F * 1e6
        return C_uF

    def calculate_all_3phase_capacitor_capacitances_from_400V(self):
        try:
            Qc_400V_kvar = float(self.input_fields["Moc obliczona przy 400V"].text().replace(',', '.'))
            C_uF = self.calculate_capacitance_from_3phase_power(Qc_400V_kvar, 400, FREQUENCY)

            Qc_440V_kvar = self.calculate_three_phase_capacitor_power(C_uF, 440, FREQUENCY)

            # Szukanie najbliższej pary na podstawie mocy 400V
            closest_pair = min(self.STANDARD_KVAR_VALUES_CAP_3P, key=lambda x: abs(x[0] - Qc_400V_kvar))
            rounded_kvar_400V = closest_pair[0]
            rounded_kvar_440V = closest_pair[1]

            self.input_fields["Pojemność"].setText(f"{C_uF:.2f}")
            self.input_fields["Moc podana przez producenta przy 400V"].setText(f"{rounded_kvar_400V}")
            self.input_fields["Moc obliczona przy 440V"].setText(f"{Qc_440V_kvar:.2f}")
            self.input_fields["Moc podana przez producenta przy 440V"].setText(f"{rounded_kvar_440V}")

        except ValueError:
            self.input_fields["Pojemność"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta przy 400V"].setText("Błąd!")
            self.input_fields["Moc obliczona przy 440V"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta przy 440V"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Pojemność"].setText("0")
            self.input_fields["Moc podana przez producenta przy 400V"].setText("0")
            self.input_fields["Moc obliczona przy 440V"].setText("0")
            self.input_fields["Moc podana przez producenta przy 440V"].setText("0")

    def calculate_all_3phase_capacitor_capacitances_from_440V(self):
        try:
            Qc_440V_kvar = float(self.input_fields["Moc obliczona przy 440V"].text().replace(',', '.'))
            C_uF = self.calculate_capacitance_from_3phase_power(Qc_440V_kvar, 440, FREQUENCY)

            Qc_400V_kvar = self.calculate_three_phase_capacitor_power(C_uF, 400, FREQUENCY)

            # Szukanie najbliższej pary na podstawie mocy 440V
            closest_pair = min(self.STANDARD_KVAR_VALUES_CAP_3P, key=lambda x: abs(x[1] - Qc_440V_kvar))
            rounded_kvar_400V = closest_pair[0]
            rounded_kvar_440V = closest_pair[1]

            self.input_fields["Pojemność"].setText(f"{C_uF:.2f}")
            self.input_fields["Moc obliczona przy 400V"].setText(f"{Qc_400V_kvar:.2f}")
            self.input_fields["Moc podana przez producenta przy 400V"].setText(f"{rounded_kvar_400V}")
            self.input_fields["Moc podana przez producenta przy 440V"].setText(f"{rounded_kvar_440V}")

        except ValueError:
            self.input_fields["Pojemność"].setText("Błąd!")
            self.input_fields["Moc obliczona przy 400V"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta przy 400V"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta przy 440V"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Pojemność"].setText("0")
            self.input_fields["Moc obliczona przy 400V"].setText("0")
            self.input_fields["Moc podana przez producenta przy 400V"].setText("0")
            self.input_fields["Moc podana przez producenta przy 440V"].setText("0")

    def calculate_power_from_capacitance(self):
        """Oblicza moc kondensatora jednofazowego na podstawie pojemności."""
        try:
            C_uF = float(self.input_fields["Pojemność"].text().replace(',', '.'))

            C_F = C_uF * 1e-6
            Qc = C_F * (VOLTAGE_1_PHASE ** 2) * 2 * math.pi * FREQUENCY
            Qc_kvar = Qc / 1000

            rounded_kvar = find_nearest_standard_value(Qc_kvar, self.STANDARD_KVAR_VALUES_CAP_1P)

            self.input_fields["Moc obliczona"].setText(f"{Qc_kvar:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Moc obliczona"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Moc obliczona"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")

    def calculate_capacitance_from_power(self):
        """Oblicza pojemność kondensatora jednofazowego na podstawie mocy."""
        try:
            Qc_kvar = float(self.input_fields["Moc obliczona"].text().replace(',', '.'))

            Qc = Qc_kvar * 1000
            C_F = Qc / ((VOLTAGE_1_PHASE ** 2) * 2 * math.pi * FREQUENCY)
            C_uF = C_F * 1e6

            rounded_kvar = find_nearest_standard_value(Qc_kvar, self.STANDARD_KVAR_VALUES_CAP_1P)

            self.input_fields["Pojemność"].setText(f"{C_uF:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Pojemność"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Pojemność"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")

    def calculate_power_from_inductance(self):
        try:
            L_mH = float(self.input_fields["Indukcyjność"].text().replace(',', '.'))

            # Wzór na moc
            L_H = L_mH * 1e-3
            XL = 2 * math.pi * FREQUENCY * L_H
            QL = (VOLTAGE_1_PHASE ** 2) / XL
            QL_kvar = QL / 1000

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES_1P)

            self.input_fields["Moc obliczona"].setText(f"{QL_kvar:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Moc obliczona"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Moc obliczona"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")

    def calculate_power_from_3phase_inductor(self):
        try:
            L_mH = float(self.input_fields["Indukcyjność"].text().replace(',', '.'))

            # Parametry obliczeniowe dla dławika 3-fazowego
            U_LINE = 400  # Napięcie międzyfazowe 400V

            # Wykorzystanie twojej funkcji
            QL_kvar = self.calculate_three_phase_inductor_power(L_mH, U_LINE, FREQUENCY)

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES_3P)

            self.input_fields["Moc obliczona"].setText(f"{QL_kvar:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Moc obliczona"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Moc obliczona"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")

    def calculate_inductance_from_power(self):
        try:
            QL_kvar = float(self.input_fields["Moc obliczona"].text().replace(',', '.'))

            # Wzór na indukcyjność
            QL = QL_kvar * 1000
            L_H = (VOLTAGE_1_PHASE ** 2) / (2 * math.pi * FREQUENCY * QL)
            L_mH = L_H * 1000

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES_1P)

            self.input_fields["Indukcyjność"].setText(f"{L_mH:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Indukcyjność"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Indukcyjność"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")

    def calculate_inductance_from_3phase_power(self):
        try:
            QL_kvar = float(self.input_fields["Moc obliczona"].text().replace(',', '.'))

            # Parametry obliczeniowe dla dławika 3-fazowego
            U_LINE = 400  # Napięcie międzyfazowe 400V
            QL = QL_kvar * 1000

            # Przeliczenie napięcia fazowego (dla połączenia w gwiazdę)
            U_phase = U_LINE / math.sqrt(3)

            # Obliczenie mocy na fazę
            Q_phase = QL / 3

            # Wzór na reaktancję: XL = U^2 / Q
            XL = (U_phase ** 2) / Q_phase

            # Wzór na indukcyjność: L = XL / (2 * pi * fn)
            L_H = XL / (2 * math.pi * FREQUENCY)
            L_mH = L_H * 1000

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES_3P)

            self.input_fields["Indukcyjność"].setText(f"{L_mH:.2f}")
            self.input_fields["Moc podana przez producenta"].setText(f"{rounded_kvar}")

        except ValueError:
            self.input_fields["Indukcyjność"].setText("Błąd!")
            self.input_fields["Moc podana przez producenta"].setText("Błąd!")
        except ZeroDivisionError:
            self.input_fields["Indukcyjność"].setText("0")
            self.input_fields["Moc podana przez producenta"].setText("0")



# --- KLASA GŁÓWNA GUI ---
class TesterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tester Podzespołów")
        self.modbus_thread = None
        self.data_labels = {}
        self.selected_label = QLabel("Brak wybranego podzespołu")
        self.testers_combos = {}  # Słownik do przechowywania QComboBoxes z zakładki Tester
        self.add_window = None
        self.tables = {}  # Słownik do przechowywania tabel, aby można było je odświeżyć

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_tester_tab(), "Tester")
        self.tab_widget.addTab(self.create_components_tab(), "Komponenty")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def create_tester_tab(self):
        global last_selected_item  # deklaracja zmiennej globalnej
        tester_tab = QWidget()
        main_layout = QHBoxLayout(tester_tab)

        # Lewa część: podzespoły
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.selected_label)

        self.combo_cond_1f_tester = QComboBox()
        self.combo_cond_1f_tester.addItem("brak")  # dodajemy brak jako pierwszą pozycję
        self.combo_cond_1f_tester.addItems(
            self.convert_list_to_strings_for_combo(load_csv("cond_1f.csv"), "cond_1f.csv"))
        left_layout.addWidget(QLabel("Kondensatory 1-fazowe:"))
        left_layout.addWidget(self.combo_cond_1f_tester)

        self.combo_cond_3f_tester = QComboBox()
        self.combo_cond_3f_tester.addItem("brak")
        self.combo_cond_3f_tester.addItems(
            self.convert_list_to_strings_for_combo(load_csv("cond_3f.csv"), "cond_3f.csv"))
        left_layout.addWidget(QLabel("Kondensatory 3-fazowe:"))
        left_layout.addWidget(self.combo_cond_3f_tester)

        self.combo_ind_1f_tester = QComboBox()
        self.combo_ind_1f_tester.addItem("brak")
        self.combo_ind_1f_tester.addItems(
            self.convert_list_to_strings_for_combo(load_csv("ind_1f.csv"), "ind_1f.csv"))
        left_layout.addWidget(QLabel("Dławiki 1-fazowe:"))
        left_layout.addWidget(self.combo_ind_1f_tester)

        self.combo_ind_3f_tester = QComboBox()
        self.combo_ind_3f_tester.addItem("brak")
        self.combo_ind_3f_tester.addItems(
            self.convert_list_to_strings_for_combo(load_csv("ind_3f.csv"), "ind_3f.csv"))
        left_layout.addWidget(QLabel("Dławiki 3-fazowe:"))
        left_layout.addWidget(self.combo_ind_3f_tester)

        # Zapisanie referencji do QComboBoxes
        self.testers_combos["ind_1f.csv"] = self.combo_ind_1f_tester
        self.testers_combos["ind_3f.csv"] = self.combo_ind_3f_tester
        self.testers_combos["cond_1f.csv"] = self.combo_cond_1f_tester
        self.testers_combos["cond_3f.csv"] = self.combo_cond_3f_tester

        # Funkcja pomocnicza do ustawienia globalnej zmiennej
        def _update_last_selected(text, category):
            global last_selected_item
            last_selected_item = text
            print("zawartość zmiennej globalnej->last_selected_item:")
            print(last_selected_item)
            self.show_selected_from_Tester(text, category)

        # Połączenie sygnałów z funkcją globalną
        self.combo_cond_1f_tester.currentTextChanged.connect(
            lambda text: _update_last_selected(text, "Kondensatory 1-fazowe"))
        self.combo_cond_3f_tester.currentTextChanged.connect(
            lambda text: _update_last_selected(text, "Kondensatory 3-fazowe"))
        self.combo_ind_1f_tester.currentTextChanged.connect(
            lambda text: _update_last_selected(text, "Dławiki 1-fazowe"))
        self.combo_ind_3f_tester.currentTextChanged.connect(
            lambda text: _update_last_selected(text, "Dławiki 3-fazowe"))

        # Linia pionowa
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        # Prawa część: porty COM i dane z analizatora
        right_layout = QVBoxLayout()

        com_group = QGroupBox("Konfiguracja COM")
        com_layout = QVBoxLayout()

        self.com_status_label = QLabel("Status połączenia: brak")
        com_layout.addWidget(self.com_status_label)

        self.combo_com = QComboBox()
        self.combo_com.addItem("brak")
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.combo_com.addItems(ports)
        com_layout.addWidget(QLabel("Wybierz port COM:"))
        com_layout.addWidget(self.combo_com)
        self.combo_com.currentTextChanged.connect(self.handle_com_selection)

        com_group.setLayout(com_layout)
        right_layout.addWidget(com_group)

        # Sekcja z danymi odczytanymi z analizatora
        data_group = QGroupBox("Odczytane dane z Analizatora Sieci")
        data_layout = QGridLayout()

        # Nagłówki kolumn
        data_layout.addWidget(QLabel(""), 0, 0)
        col_names = ["L1", "L2", "L3"]
        for i, name in enumerate(col_names):
            label = QLabel(name)
            label.setStyleSheet("font-weight: bold;")
            data_layout.addWidget(label, 0, i + 1)

        # Nagłówki wierszy i etykiety dla wartości aktualnych
        row_params = [("U [V]", ["U1", "U2", "U3"]),
                      ("I [A]", ["I1", "I2", "I3"]),
                      ("Q [var]", ["Q1", "Q2", "Q3"])]

        for row, (row_name, params) in enumerate(row_params):
            label = QLabel(row_name)
            label.setStyleSheet("font-weight: bold;")
            data_layout.addWidget(label, row + 1, 0)
            for col, param in enumerate(params):
                self.data_labels[param] = QLabel("---")
                self.data_labels[param].setStyleSheet("font-size: 14px; color: blue;")
                data_layout.addWidget(self.data_labels[param], row + 1, col + 1)

        data_group.setLayout(data_layout)
        right_layout.addWidget(data_group)

        # Sekcja dla obliczonych napięć międzyfazowych
        volt_ll_group = QGroupBox("Obliczone napięcia międzyfazowe [V]")
        volt_ll_layout = QGridLayout()
        volt_ll_params = ["U12", "U23", "U31"]
        for col, param in enumerate(volt_ll_params):
            label = QLabel(param)
            label.setStyleSheet("font-weight: bold;")
            volt_ll_layout.addWidget(label, 0, col)
            self.data_labels[param] = QLabel("---")
            self.data_labels[param].setStyleSheet("font-size: 14px; color: green;")
            volt_ll_layout.addWidget(self.data_labels[param], 1, col)

        volt_ll_group.setLayout(volt_ll_layout)
        right_layout.addWidget(volt_ll_group)

        # Sekcja dla średniego napięcia międzyfazowego
        avg_volt_group = QGroupBox("Średnie napięcie międzyfazowe [V]")
        avg_volt_layout = QVBoxLayout()
        self.data_labels["U_avg"] = QLabel("---")
        self.data_labels["U_avg"].setStyleSheet("font-size: 16px; font-weight: bold; color: darkred;")
        avg_volt_layout.addWidget(self.data_labels["U_avg"])
        avg_volt_group.setLayout(avg_volt_layout)
        right_layout.addWidget(avg_volt_group)

        # Dodanie części do layoutu głównego
        main_layout.addLayout(left_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(right_layout)

        # --- Druga pionowa linia po prawej stronie ---
        line2 = QFrame()
        line2.setFrameShape(QFrame.VLine)
        line2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line2)

        # --- Dodatkowa sekcja z tekstem po prawej stronie od nowej linii ---
        extra_group = QGroupBox("Informacje dodatkowe")
        extra_layout = QVBoxLayout()

        # Etykieta z instrukcją
        extra_label = QLabel("Wybierz port COM dla Testera")
        extra_label.setStyleSheet("font-size: 14px; color: purple;")
        extra_label.setWordWrap(True)  # aby tekst się zawijał
        extra_layout.addWidget(extra_label)

        # --- Rozwijana lista portów COM wewnątrz ramki ---
        self.combo_com_extra = QComboBox()
        self.combo_com_extra.addItem("brak")  # domyślnie brak

        # Pobranie dostępnych portów COM
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.combo_com_extra.addItems(ports)

        # Dodanie do layoutu ramki
        extra_layout.addWidget(self.combo_com_extra)

        # Funkcja wywoływana przy zmianie wyboru
        def on_combo_com_extra_changed(index):
            global COM
            selected_port = self.combo_com_extra.currentText()
            print("Wybrany port COM (extra):", selected_port)
            COM = selected_port  # zapisanie wybranego portu do zmiennej globalnej

        # Podłączenie sygnału zmiany wyboru
        self.combo_com_extra.currentIndexChanged.connect(on_combo_com_extra_changed)

        # --- Przycisk Start pod listą ---
        start_button = QPushButton("Start")
        extra_layout.addWidget(start_button)

        # Funkcja do otwarcia nowego okna
        def open_start_window():

            global COM, polaczono_z_Novar

            if COM is not None and polaczono_z_Novar is not None:
                # Wszystko OK, otwieramy okno
                self.start_window = StartWindow()  # zapisujemy w self
                self.start_window.exec()  # otwiera okno modalnie
            else:
                # Któraś zmienna jest None, pokazujemy komunikat
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Brak połączenia")
                msg_box.setText("Nie jesteś połączony po portach COM!")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()

        start_button.clicked.connect(open_start_window)

        extra_group.setLayout(extra_layout)

        # Dodanie całej sekcji do głównego layoutu
        main_layout.addWidget(extra_group)

        # --- Logika resetowania pozostałych list ---
        def reset_other_combos(changed_combo):
            # sprawdzamy, czy wybrano coś innego niż "brak"
            if changed_combo.currentIndex() > 0:
                combos = [
                    self.combo_cond_1f_tester,
                    self.combo_cond_3f_tester,
                    self.combo_ind_1f_tester,
                    self.combo_ind_3f_tester,
                ]
                for combo in combos:
                    if combo is not changed_combo:
                        combo.setCurrentIndex(0)  # ustawiamy na "brak"

        self.combo_cond_1f_tester.currentIndexChanged.connect(
            lambda: reset_other_combos(self.combo_cond_1f_tester)
        )
        self.combo_cond_3f_tester.currentIndexChanged.connect(
            lambda: reset_other_combos(self.combo_cond_3f_tester)
        )
        self.combo_ind_1f_tester.currentIndexChanged.connect(
            lambda: reset_other_combos(self.combo_ind_1f_tester)
        )
        self.combo_ind_3f_tester.currentIndexChanged.connect(
            lambda: reset_other_combos(self.combo_ind_3f_tester)
        )

        return tester_tab

    def create_components_tab(self):
        components_tab = QWidget()
        self.sub_tab_widget = QTabWidget(components_tab)
        layout = QVBoxLayout(components_tab)
        layout.addWidget(self.sub_tab_widget)

        def create_table_tab(file_path, tab_name):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)

            button_layout = QHBoxLayout()
            delete_button = QPushButton("Usuń zaznaczony element")
            add_button = QPushButton("Dodaj element")

            button_layout.addWidget(add_button)
            button_layout.addWidget(delete_button)
            tab_layout.addLayout(button_layout)

            items = load_csv(file_path)

            table = QTableWidget()

            # Konfiguracja tabeli w zależności od pliku
            if file_path == "ind_1f.csv" or file_path == "ind_3f.csv":
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Moc producenta [kVAr]", "Indukcyjność [mH]", "Moc obliczona [kVAr]", "Producent"])
            elif file_path == "cond_1f.csv":
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Moc producenta [kVAr]", "Pojemność [uF]", "Moc obliczona [kVAr]", "Producent"])
            elif file_path == "cond_3f.csv":
                table.setColumnCount(6)
                table.setHorizontalHeaderLabels(
                    ["Moc producenta przy 440V [kVAr]", "Moc producenta przy 400V [kVAr]", "Pojemność [uF]",
                     "Moc obliczona przy 400V [kVAr]", "Moc obliczona przy 440V [kVAr]", "Producent"])
            elif items:
                table.setColumnCount(len(items[0]))
                table.setHorizontalHeaderLabels([f"Kolumna {i + 1}" for i in range(table.columnCount())])
            else:
                table.setColumnCount(1)
                table.setHorizontalHeaderLabels(["Nazwa"])

            table.setRowCount(len(items))
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().hide()
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setStyleSheet("QTableWidget::item:selected { background-color: lightblue; }")

            for row, item_row in enumerate(items):
                for col, item_value in enumerate(item_row):
                    table.setItem(row, col, QTableWidgetItem(item_value))

            self.tables[file_path] = table

            table.cellClicked.connect(lambda row, col: self.show_selected(table.item(row, col).text(), tab_name))

            delete_button.clicked.connect(lambda: self.delete_selected_item(table, file_path, tab_name))
            add_button.clicked.connect(lambda: self.open_add_window(tab_name))

            tab_layout.addWidget(table)
            return tab

        self.sub_tab_widget.addTab(create_table_tab("ind_1f.csv", "1-fazowe_dławiki"), "1-fazowe_dławiki")
        self.sub_tab_widget.addTab(create_table_tab("ind_3f.csv", "3-fazowe_dławiki"), "3-fazowe_dławiki")
        self.sub_tab_widget.addTab(create_table_tab("cond_1f.csv", "1-fazowe_kondensatory"), "1-fazowe_kondensatory")
        self.sub_tab_widget.addTab(create_table_tab("cond_3f.csv", "3-fazowe_kondensatory"), "3-fazowe_kondensatory")

        return components_tab

    def add_and_refresh(self, file_path, new_item):
        items = load_csv(file_path)

        # Wartość mocy nowego elementu
        try:
            # Dla kondensatora 3-fazowego bierzemy moc podana przez producenta przy 400V jako klucz sortowania
            if file_path == "cond_3f.csv":
                new_power = float(new_item[1].replace(',', '.'))
            else:
                new_power = float(new_item[0].replace(',', '.'))
        except ValueError:
            print("Błąd: Wartość mocy nowego elementu jest nieprawidłowa.")
            return

        insertion_index = -1

        # Znajdź indeks, w którym należy wstawić nowy element, aby zachować sortowanie
        for i, item_row in enumerate(items):
            try:
                # Wartość mocy istniejącego elementu
                if file_path == "cond_3f.csv":
                    current_power = float(item_row[1].replace(',', '.'))
                else:
                    current_power = float(item_row[0].replace(',', '.'))
                # Sprawdzanie, czy nowa moc jest mniejsza lub równa istniejącej
                if new_power <= current_power:
                    insertion_index = i
                    break
            except (ValueError, IndexError):
                # Ignoruj wiersze z nieprawidłowymi danymi
                continue

        # Wstaw nowy element we właściwe miejsce lub dodaj na końcu, jeśli nie znaleziono miejsca
        if insertion_index != -1:
            items.insert(insertion_index, new_item)
        else:
            items.append(new_item)

        save_csv(file_path, items)
        self.refresh_ui(file_path)

    def refresh_ui(self, file_path):
        items = load_csv(file_path)

        # Odśwież QTableWidget
        if file_path in self.tables:
            table = self.tables[file_path]

            # Ustaw liczbę kolumn i nagłówki w zależności od pliku
            if file_path == "ind_1f.csv" or file_path == "ind_3f.csv":
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Moc producenta [kVAr]", "Indukcyjność [mH]", "Moc obliczona [kVAr]","Producent"])
            elif file_path == "cond_1f.csv":
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Moc producenta [kVAr]", "Pojemność [uF]", "Moc obliczona [kVAr]", "Producent"])
            elif file_path == "cond_3f.csv":
                table.setColumnCount(6)
                table.setHorizontalHeaderLabels(
                    ["Moc producenta przy 440V [kVAr]", "Moc producenta przy 400V [kVAr]", "Pojemność [uF]",
                     "Moc obliczona przy 400V [kVAr]", "Moc obliczona przy 440V [kVAr]","Producent"])
            elif items:
                table.setColumnCount(len(items[0]))
                table.setHorizontalHeaderLabels([f"Kolumna {i + 1}" for i in range(table.columnCount())])
            else:
                table.setColumnCount(1)
                table.setHorizontalHeaderLabels(["Nazwa"])

            table.setRowCount(len(items))

            for row, item_row in enumerate(items):
                for col, item_value in enumerate(item_row):
                    table.setItem(row, col, QTableWidgetItem(item_value))

        # Odśwież QComboBox
        if file_path in self.testers_combos:
            combo = self.testers_combos[file_path]
            combo.clear()
            # Użycie nowej funkcji do formatowania stringów
            combo.addItems(self.convert_list_to_strings_for_combo(items, file_path))

    def convert_list_to_strings_for_combo(self, items_list, file_path):
        formatted_list = []
        if file_path == "cond_1f.csv":
            for item in items_list:
                if len(item) >= 4:  # producent w 4 kolumnie, indeks 3
                    formatted_list.append(f"{item[0]} [kVAr], {item[1]} [uF]   {item[3]}")
                else:
                    formatted_list.append(", ".join(item))
        elif file_path == "cond_3f.csv":
            for item in items_list:
                if len(item) >= 6:  # producent w 6 kolumnie, indeks 5
                    formatted_list.append(
                        f"{item[0]} [kVAr] 440 V, {item[1]} [kVAr] 400 V, {item[2]} [uF]  {item[5]}")
                else:
                    formatted_list.append(", ".join(item))
        elif file_path == "ind_1f.csv" or file_path == "ind_3f.csv":
            for item in items_list:
                if len(item) >= 4:  # producent w 4 kolumnie, indeks 3
                    formatted_list.append(f"{item[0]} [kVAr], {item[1]} [mH]   {item[3]}")
                else:
                    formatted_list.append(", ".join(item))
        else:
            # Domyślne zachowanie dla innych plików
            for item in items_list:
                formatted_list.append(", ".join(item))

        return formatted_list

    def open_add_window(self, tab_name):
        self.add_window = AddElementWindow(self, tab_name)
        self.add_window.show()

    def delete_selected_item(self, table, file_path, tab_name):
        selected_rows = sorted(list(set(index.row() for index in table.selectedIndexes())), reverse=True)
        if not selected_rows:
            return

        items = load_csv(file_path)

        for row in selected_rows:
            if 0 <= row < len(items):
                items.pop(row)

        save_csv(file_path, items)

        self.refresh_ui(file_path)

        self.show_selected("", "")

    def handle_com_selection(self, port_name):
        if self.modbus_thread and self.modbus_thread.isRunning():
            self.modbus_thread.stop()
            self.modbus_thread.quit()
            self.modbus_thread.wait()

        if port_name != "brak":
            self.modbus_thread = ModbusReader(port_name)
            self.modbus_thread.data_ready.connect(self.update_data_display)
            self.modbus_thread.connection_status.connect(self.com_status_label.setText)
            self.modbus_thread.start()
        else:
            self.com_status_label.setText("Status połączenia: brak")
            self.clear_data_display()

    def update_data_display(self, data):
        global global_u1, global_u2, global_u3
        global global_u12, global_u23, global_u31, global_u_avg
        global global_i1, global_i2, global_i3
        global global_q1, global_q2, global_q3

        for name, value in data.items():
            label = self.data_labels.get(name)
            if label:
                if value is not None:
                    label.setText(f"{value:.2f}")
                else:
                    label.setText("N/A")

        # zapis prądów do zmiennych globalnych
        if all(k in data and data[k] is not None for k in ["I1", "I2", "I3"]):
            global_i1 = data["I1"]
            global_i2 = data["I2"]
            global_i3 = data["I3"]
            print(f"Prądy zapisane globalnie: I1={global_i1}, I2={global_i2}, I3={global_i3}")

        # zapis mocy biernej do zmiennych globalnych
        if all(k in data and data[k] is not None for k in ["Q1", "Q2", "Q3"]):
            global_q1 = data["Q1"]
            global_q2 = data["Q2"]
            global_q3 = data["Q3"]
            print(f"Moc bierna zapisana globalnie: Q1={global_q1}, Q2={global_q2}, Q3={global_q3}")

        if all(key in data and data[key] is not None for key in ["U1", "U2", "U3"]):
            try:
                u1 = data["U1"]
                u2 = data["U2"]
                u3 = data["U3"]

                # zapis do zmiennych globalnych
                global_u1 = u1
                global_u2 = u2
                global_u3 = u3
                print(f"zapisano do zmiennych globalnych wartości napięć : U1: {u1} V, U2: {u2}V, U3: {u3}V")

                u12 = math.sqrt(u1 ** 2 + u2 ** 2 + u1 * u2)
                u23 = math.sqrt(u2 ** 2 + u3 ** 2 + u2 * u3)
                u31 = math.sqrt(u3 ** 2 + u1 ** 2 + u3 * u1)

                # zapis wyników obliczeń do globalnych
                global_u12 = u12
                global_u23 = u23
                global_u31 = u31
                print(f"zapisano do zmiennych globalnych wartości napięć : U1-2: {u12} V, U2-3: {u23}V, U3-1: {u31}V")

                u_avg = (u12 + u23 + u31) / 3
                global_u_avg = u_avg
                print(f"zapisano do zmiennych globalnych wartość średniego napięcia międzyfazowego : {u_avg}V")

                self.data_labels["U12"].setText(f"{u12:.2f}")
                self.data_labels["U23"].setText(f"{u23:.2f}")
                self.data_labels["U31"].setText(f"{u31:.2f}")
                self.data_labels["U_avg"].setText(f"{u_avg:.2f} V")
            except (KeyError, TypeError):
                self.data_labels["U12"].setText("Err")
                self.data_labels["U23"].setText("Err")
                self.data_labels["U31"].setText("Err")
                self.data_labels["U_avg"].setText("Err")

    def clear_data_display(self):
        for label in self.data_labels.values():
            label.setText("---")

    def show_selected(self, text, list_name):
        # Sprawdzenie, czy wybrany tekst nie jest pusty
        if text.strip():
            #self.selected_label.setText(f"Wybrano: {text} z listy: {list_name}")
            print(f"zaznaczono element : {text} , w tabeli : {list_name}")
        else:
            self.selected_label.setText("Brak wybranego podzespołu")
            pass


    def show_selected_from_Tester(self, text, list_name):
        global last_selected_item
        if text.strip() and text != "brak":
            last_selected_item = text
        self.selected_label.setText(f"Wybrano: {last_selected_item}")

    def closeEvent(self, event):
        if self.modbus_thread and self.modbus_thread.isRunning():
            self.modbus_thread.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TesterGUI()
    window.show()
    sys.exit(app.exec())