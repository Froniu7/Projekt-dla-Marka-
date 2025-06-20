from PySide6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
)
import sys

def utworz_tabele(dane, naglowki):
    tabela = QTableWidget(len(dane), len(naglowki))
    tabela.setHorizontalHeaderLabels(naglowki)
    for i, wiersz in enumerate(dane):
        for j, komorka in enumerate(wiersz):
            tabela.setItem(i, j, QTableWidgetItem(str(komorka)))
    return tabela

import csv
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

def utworz_tabele_z_csv(sciezka):
    with open(sciezka, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        wiersze = list(reader)

    if not wiersze:
        return QTableWidget()  # pusty widżet, jeśli plik pusty

    naglowki = wiersze[0]
    dane = wiersze[1:]

    tabela = QTableWidget(len(dane), len(naglowki))
    tabela.setHorizontalHeaderLabels(naglowki)

    for i, wiersz in enumerate(dane):
        for j, komorka in enumerate(wiersz):
            tabela.setItem(i, j, QTableWidgetItem(komorka))

    tabela.resizeColumnsToContents()
    tabela.setShowGrid(True)

    tabela.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #f3f3f3;
            }
        """)

    return tabela


app = QApplication(sys.argv)

# Główne okno z zakładkami
okno = QTabWidget()

# Zakładka 1
widget1 = QWidget()
layout1 = QVBoxLayout(widget1)
#dane1 = [[1, "Jan", 30], [2, "Anna", 25]]
tabela1 = utworz_tabele_z_csv("zabezpieczeniaSVGgG[1].csv")
#tabela1 = utworz_tabele(dane1, ["ID", "Imię", "Wiek"])
layout1.addWidget(tabela1)
okno.addTab(widget1, "zabezpieczenia-SVG")

# Zakładka 2
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("moc_przekroj.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Dobór przekroje i zabezpieczenia")

# Zakładka 3
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("zabezpieczenia_C_gG.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Zabezpieczenia C i gG")

# Zakładka 4
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("przewody_miedziane_B2.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Przewody kablowe zasilające")

# Zakładka 5
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("przekladniki.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Przekladniki")

# Zakładka 5
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("przewody_sterownicze.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Przewody kablowe sterownicze")

# Zakładka 5
widget2 = QWidget()
layout2 = QVBoxLayout(widget2)
#dane2 = [["001", "Wiertarka", 3], ["002", "Szlifierka", 5]]
tabela2 = utworz_tabele_z_csv("sterowniki.csv")
#tabela2 = utworz_tabele(dane2, ["Kod", "Nazwa", "Ilość"])
layout2.addWidget(tabela2)
okno.addTab(widget2, "Sterowniki")

okno.setStyleSheet("""
    QTabBar::tab {
        background: lightgray;
        padding: 8px;
        border: 1px solid gray;
        border-bottom: none;
        min-width: 100px;
    }

    QTabBar::tab:selected {
        background: orange;
        font-weight: bold;
        color: black;
    }

    QTabWidget::pane {
        border: 1px solid gray;
        top: -1px;
    }
""")

okno.setWindowTitle("Moje zakładki z tabelami")
okno.resize(500, 300)
okno.show()
sys.exit(app.exec())
