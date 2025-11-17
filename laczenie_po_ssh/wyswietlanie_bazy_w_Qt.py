import json
import os
import sys
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

CONFIG_FILE = "config_WAN.json"
LOCAL_TUNNEL_PORT = 6543
TARGET_DB_HOST = '127.0.0.1'  # Cel tunelu na Malinie

def load_config(file_path):
    """Wczytuje dane konfiguracyjne z pliku JSON."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        # Używamy QMessageBox.critical, aby wyświetlić błąd użytkownikowi
        QMessageBox.critical(None, "Błąd Konfiguracji",
                             f"Nie można wczytać lub przetworzyć pliku {file_path}: {e}")
        # Użycie sys.exit jest konieczne, jeśli brakuje konfiguracji
        sys.exit(1)
        return None

class Psycopg2TableModel(QAbstractTableModel):
    """Niestandardowy model PySide6, który pobiera dane przez psycopg2."""

    def __init__(self, data=None, header=None):
        super().__init__()
        self._data = data if data is not None else []
        self._header = header if header is not None else []

    def set_data(self, data, header):
        """Ustawia nowe dane z bazy i odświeża widok."""
        self.beginResetModel()
        self._data = data
        self._header = header
        self.endResetModel()

    # --- Wymagane Metody QAbstractTableModel ---

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        if self._data and self._data[0]:
            return len(self._data[0])
        return 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # Zwraca wartość z komórki
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            # Zwraca nagłówki kolumn
            if section < len(self._header):
                return self._header[section]
        return None


# --- 2. Główna Aplikacja Qt z Logicznym Połączeniem ---

class ClientDatabaseApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.tunnel = None
        self.conn = None

        self.setWindowTitle("Zarządzanie Klientami (Połączenie Psycopg2/SSH)")
        self.setGeometry(100, 100, 1000, 700)

        # Inicjalizacja widoku
        self.table_model = Psycopg2TableModel()
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table_view)

        # Uruchomienie połączenia
        self._connect_and_load_data()

    def _connect_and_load_data(self):
        """Łączy się z bazą danych przez tunel i pobiera dane."""
        db_cfg = self.config["database"]
        db_user = db_cfg["db_user"]
        db_pass = db_cfg["db_password"]
        db_name = db_cfg["db_name"]

        if not self._start_ssh_tunnel():
            return

        try:
            # Połączenie z PostgreSQL przez lokalny port tunelu
            self.conn = psycopg2.connect(
                host="127.0.0.1",
                port=LOCAL_TUNNEL_PORT,
                database=db_name,
                user=db_user,
                password=db_pass,
                connect_timeout=5
            )
            print("🎉 Połączenie z bazą PostgreSQL przez Psycopg2 zakończone sukcesem!")
            self._load_data_to_model()

        except Exception as e:
            QMessageBox.critical(self, "Błąd PostgreSQL", f"Błąd połączenia z bazą danych: {e}")
            self.close()

    def _start_ssh_tunnel(self):
        """Uruchamia tunel SSH, używając załadowanego klucza Paramiko."""
        ssh_cfg = self.config["connection"]
        ssh_auth = self.config["auth"]

        key_path = ssh_auth["key_path"]
        passphrase = ssh_auth.get("passphrase") or None

        try:
            # Ładowanie klucza (identyczne z Twoim działającym kodem)
            pkey = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)

            self.tunnel = SSHTunnelForwarder(
                (ssh_cfg["host"], ssh_cfg["port"]),
                ssh_username=ssh_cfg["username"],
                ssh_pkey=pkey,
                remote_bind_address=(TARGET_DB_HOST, self.config["database"]["db_port"]),
                local_bind_address=('127.0.0.1', LOCAL_TUNNEL_PORT),
                set_keepalive=20
            )
            self.tunnel.start()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Błąd Tunelu SSH", f"Nie udało się uruchomić tunelu SSH: {e}")
            return False

    def _load_data_to_model(self):
        """Wykonuje zapytanie SQL i przekazuje wyniki do modelu tabeli."""
        query = """
        SELECT 
            k.nazwa_firmy, k.nip, k.miasto_siedziby,
            l.nazwa_lokalizacji, l.nr_ppe_glowny,
            o.imie, o.nazwisko
        FROM klienci k
        LEFT JOIN lokalizacje l ON k.klient_id = l.klient_id
        LEFT JOIN osoby_kontaktowe o ON k.klient_id = o.klient_id
        ORDER BY k.nazwa_firmy;
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            # Pobieranie nazw kolumn z kursora
            header = [desc[0] for desc in cursor.description]

            self.table_model.set_data(data, header)
            self.table_view.resizeColumnsToContents()
            print(f"Pobrano i wyświetlono {len(data)} wierszy.")

        except Exception as e:
            QMessageBox.warning(self, "Błąd SQL", f"Nie można wykonać zapytania SQL: {e}")
        finally:
            cursor.close()

    def closeEvent(self, event):
        """Zamyka połączenie DB i tunel SSH przy zamykaniu aplikacji."""
        if self.conn:
            self.conn.close()
            print("Połączenie z PostgreSQL zamknięte.")
        if self.tunnel:
            self.tunnel.stop()
            print("Tunel SSH zatrzymany.")
        super().closeEvent(event)


# --- 3. Główna pętla aplikacji ---

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Ładowanie konfiguracji
    CONFIG_DATA = load_config(CONFIG_FILE)
    if CONFIG_DATA:
        # 2. Uruchomienie aplikacji
        window = ClientDatabaseApp(CONFIG_DATA)
        window.show()

        # 3. Wykonanie pętli aplikacji
        sys.exit(app.exec())
    else:
        sys.exit(-1)