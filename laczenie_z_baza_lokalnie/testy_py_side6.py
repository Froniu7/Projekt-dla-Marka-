import sys
import json
import psycopg2
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox


class DatabaseViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Podgląd danych z PostgreSQL")
        self.resize(1000, 500)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        try:
            self.db_cfg = self.load_config()
            data = self.load_data()
            self.populate_table(data)
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

    def load_config(self):
        """Wczytuje dane logowania z pliku config.json"""
        with open("config.json", "r") as f:
            return json.load(f)

    def load_data(self):
        cfg = self.db_cfg

        conn = psycopg2.connect(
            host=cfg["host"],
            port=cfg["port"],
            dbname=cfg["dbname"],
            user=cfg["user"],
            password=cfg["password"]
        )

        cur = conn.cursor()

        query = """
            --wyswietlanie danych wielu klientów 
SELECT
    -- Dane Klienta
    k.nazwa_firmy,
    k.nip,
    k.telefon_glowny,
    -- Dane Lokalizacji
    l.nazwa_lokalizacji,
    l.miasto || ', ' || l.ulica || ' ' || l.nr_budynku AS pelny_adres_lokalizacji,
    -- Dane Licznika (punktu pomiarowego)
    lc.nr_licznika,
    lc.nr_ppe,
    lc.typ_licznika,
    -- Dane Urządzenia
    u.numer_urzadzenia AS nr_urzadzenia_zamontowanego,
    u.typ_urzadzenia AS typ_zamontowanego_urzadzenia,
    u.moc_kvar,
    u.data_montazu,
    u.status AS status_urzadzenia,
    -- Dane Zlecenia
    z.data_zlecenia,
    z.opis AS opis_zlecenia,
    z.status AS status_zlecenia
FROM
    klient k
JOIN
    lokalizacja l ON l.klient_id = k.klient_id
JOIN
    licznik lc ON lc.lokalizacja_id = l.lokalizacja_id
LEFT JOIN
    urzadzenie u ON u.licznik_id = lc.licznik_id
LEFT JOIN
    zlecenie z ON z.licznik_id = lc.licznik_id
WHERE
    k.klient_id IN (1, 2, 3); -- Zmieniony warunek
        """

        cur.execute(query)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        return col_names, rows

    def populate_table(self, data):
        col_names, rows = data

        self.table.setColumnCount(len(col_names))
        self.table.setHorizontalHeaderLabels(col_names)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec())
