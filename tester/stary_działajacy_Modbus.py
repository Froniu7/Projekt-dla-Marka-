import sys
import csv
import serial.tools.list_ports
import math
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QFrame, QGridLayout, \
    QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QAbstractItemView, QRadioButton, \
    QButtonGroup, QLineEdit, QDialog
from PySide6.QtCore import QThread, Signal
from pymodbus.client.sync import ModbusSerialClient
import struct
import time

# Stałe używane do obliczeń
VOLTAGE_1_PHASE = 230  # V
FREQUENCY = 50  # Hz


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
        else:
            self.connection_status.emit("❌ Błąd połączenia!")

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


# --- KLASA DEDYKOWANA DLA OKNA DODAWANIA NOWEGO ELEMENTU ---
class AddElementWindow(QDialog):
    # Lista standardowych wartości mocy w kvar
    STANDARD_KVAR_VALUES = sorted(list(set([
        0.02, 0.04, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.33, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9,
        1.0, 1.25, 1.3, 1.5, 1.66, 1.75, 2.0, 2.25, 2.5, 3.0, 3.25, 3.33, 3.5, 4.0, 5.0, 6.66, 10.0
    ])))

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
        if self.radio_buttons["dławik 1 fazowy"].isChecked():
            try:
                # Pobierz wartości z pól tekstowych
                calculated_power = self.input_fields["Moc obliczona"].text()
                manufacturer_power = self.input_fields["Moc podana przez producenta"].text()
                inductance = self.input_fields["Indukcyjność"].text()

                # Sprawdź, czy wartości są poprawne
                if not calculated_power or not manufacturer_power or not inductance or "Błąd" in calculated_power:
                    print("Nie można dodać elementu: brak danych lub błąd w obliczeniach.")
                    return

                # Utwórz listę wartości do zapisania w pliku CSV
                new_item = [manufacturer_power, inductance, calculated_power]

                # Zapisz do pliku i odśwież widoki
                file_path = "ind_1f.csv"
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

            # Połączenie sygnałów
            if component_type == "dławik 1 fazowy":
                self.input_fields["Indukcyjność"].returnPressed.connect(self.calculate_power_from_inductance)
                self.input_fields["Moc obliczona"].returnPressed.connect(self.calculate_inductance_from_power)

    def calculate_power_from_inductance(self):
        try:
            L_mH = float(self.input_fields["Indukcyjność"].text().replace(',', '.'))

            # Wzór na moc
            L_H = L_mH * 1e-3
            XL = 2 * math.pi * FREQUENCY * L_H
            QL = (VOLTAGE_1_PHASE ** 2) / XL
            QL_kvar = QL / 1000

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES)

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

            rounded_kvar = find_nearest_standard_value(QL_kvar, self.STANDARD_KVAR_VALUES)

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
        tester_tab = QWidget()
        main_layout = QHBoxLayout(tester_tab)

        # Lewa część: podzespoły
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.selected_label)

        self.combo_cond_1f_tester = QComboBox()
        self.combo_cond_1f_tester.addItems(self.convert_list_to_strings(load_csv("cond_1f.csv")))
        left_layout.addWidget(QLabel("Kondensatory 1-fazowe:"))
        left_layout.addWidget(self.combo_cond_1f_tester)

        self.combo_cond_3f_tester = QComboBox()
        self.combo_cond_3f_tester.addItems(self.convert_list_to_strings(load_csv("cond_3f.csv")))
        left_layout.addWidget(QLabel("Kondensatory 3-fazowe:"))
        left_layout.addWidget(self.combo_cond_3f_tester)

        self.combo_ind_1f_tester = QComboBox()
        self.combo_ind_1f_tester.addItems(self.convert_list_to_strings(load_csv("ind_1f.csv")))
        left_layout.addWidget(QLabel("Dławiki 1-fazowe:"))
        left_layout.addWidget(self.combo_ind_1f_tester)

        self.combo_ind_3f_tester = QComboBox()
        self.combo_ind_3f_tester.addItems(self.convert_list_to_strings(load_csv("ind_3f.csv")))
        left_layout.addWidget(QLabel("Dławiki 3-fazowe:"))
        left_layout.addWidget(self.combo_ind_3f_tester)

        # Zapisanie referencji do QComboBoxes
        self.testers_combos["cond_1f.csv"] = self.combo_cond_1f_tester
        self.testers_combos["cond_3f.csv"] = self.combo_cond_3f_tester
        self.testers_combos["ind_1f.csv"] = self.combo_ind_1f_tester
        self.testers_combos["ind_3f.csv"] = self.combo_ind_3f_tester

        self.combo_cond_1f_tester.currentTextChanged.connect(
            lambda text: self.show_selected(text, "Kondensatory 1-fazowe"))
        self.combo_cond_3f_tester.currentTextChanged.connect(
            lambda text: self.show_selected(text, "Kondensatory 3-fazowe"))
        self.combo_ind_1f_tester.currentTextChanged.connect(lambda text: self.show_selected(text, "Dławiki 1-fazowe"))
        self.combo_ind_3f_tester.currentTextChanged.connect(lambda text: self.show_selected(text, "Dławiki 3-fazowe"))

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
            if file_path == "ind_1f.csv":
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["Moc producenta", "Indukcyjność", "Moc obliczona"])
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

            table.cellClicked.connect(lambda row, col: self.show_selected(table.item(row, col), tab_name))

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
        items.append(new_item)
        save_csv(file_path, items)
        self.refresh_ui(file_path)

    def refresh_ui(self, file_path):
        items = load_csv(file_path)

        # Odśwież QTableWidget
        if file_path in self.tables:
            table = self.tables[file_path]

            # Ustaw liczbę kolumn i nagłówki w zależności od pliku
            if file_path == "ind_1f.csv":
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["Moc producenta", "Indukcyjność", "Moc obliczona"])
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
            combo.addItems(self.convert_list_to_strings(items))

    def convert_list_to_strings(self, items_list):
        return [", ".join(map(str, item)) for item in items_list]

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

        self.show_selected("Brak wybranego podzespołu", "")

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
        for name, value in data.items():
            label = self.data_labels.get(name)
            if label:
                if value is not None:
                    label.setText(f"{value:.2f}")
                else:
                    label.setText("N/A")

        if all(key in data and data[key] is not None for key in ["U1", "U2", "U3"]):
            try:
                u1 = data["U1"]
                u2 = data["U2"]
                u3 = data["U3"]

                u12 = math.sqrt(u1 ** 2 + u2 ** 2 + u1 * u2)
                u23 = math.sqrt(u2 ** 2 + u3 ** 2 + u2 * u3)
                u31 = math.sqrt(u3 ** 2 + u1 ** 2 + u3 * u1)

                u_avg = (u12 + u23 + u31) / 3

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

    def show_selected(self, item, list_name):
        if isinstance(item, str):
            text = item
        elif item:
            text = item.text()
        else:
            text = "Brak wybranego podzespołu"

        self.selected_label.setText(f"Wybrano: {text} z listy: {list_name}")

    def closeEvent(self, event):
        if self.modbus_thread and self.modbus_thread.isRunning():
            self.modbus_thread.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TesterGUI()
    window.show()
    sys.exit(app.exec())