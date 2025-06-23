from PySide6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
)
import sys
import csv
from PySide6.QtWidgets import QSizePolicy


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

# Główny widget z dwoma zakładkami
okno = QTabWidget()

# 1. Zakładka "Generowanie schematów"
#generowanie_widget = QWidget()
#layout_generowanie = QVBoxLayout(generowanie_widget)
# Przykładowy widget - możesz tam wstawić swoje GUI

# Zakładka 1: Generowanie schematów
widget_generowanie = QWidget()
layout_generowanie = QVBoxLayout(widget_generowanie)

# Pierwszy przycisk z opisem
label1 = QLabel("Opis pierwszego przycisku:")
przycisk1 = QPushButton("Generuj schemat")
przycisk1.setMinimumSize(150, 40)   # minimalny rozmiar
przycisk1.setMaximumSize(300, 50)   # maksymalny rozmiar
przycisk1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # skalowalność w poziomie
layout_generowanie.addWidget(label1)
layout_generowanie.addWidget(przycisk1)

# Drugi przycisk z opisem
label2 = QLabel("Opis drugiego przycisku:")
przycisk2 = QPushButton("Podgląd PDF")
przycisk2.setMinimumSize(150, 40)
przycisk2.setMaximumSize(300, 50)
przycisk2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
layout_generowanie.addWidget(label2)
layout_generowanie.addWidget(przycisk2)


okno.addTab(widget_generowanie, "Generowanie schematów")



label = QLabel("Tu będzie Twoje GUI do generowania schematów")
layout_generowanie.addWidget(label)
przycisk = QPushButton("Przycisk generowania")
layout_generowanie.addWidget(przycisk)

#okno.addTab(widget_generowanie, "Generowanie schematów")

# 2. Zakładka "Dane"
dane_widget = QWidget()
layout_dane = QVBoxLayout(dane_widget)

# Podzakładki z tabelami
tabele_tabs = QTabWidget()

# Dodaj tutaj swoje tabele
csv_pliki = [
    ("zabezpieczenia-SVG", "zabezpieczeniaSVGgG[1].csv"),
    ("Dobór przekroje i zabezpieczenia", "moc_przekroj.csv"),
    ("Zabezpieczenia C i gG", "zabezpieczenia_C_gG.csv"),
    ("Przewody kablowe zasilające", "przewody_miedziane_B2.csv"),
    ("Przekladniki", "przekladniki.csv"),
    ("Przewody kablowe sterownicze", "przewody_sterownicze.csv"),
    ("Sterowniki", "sterowniki.csv"),
]

for nazwa, sciezka in csv_pliki:
    try:
        tabela = utworz_tabele_z_csv(sciezka)
    except FileNotFoundError:
        tabela = QLabel(f"Plik nie znaleziony:\n{sciezka}")
    tab = QWidget()
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(tabela)
    tabele_tabs.addTab(tab, nazwa)

layout_dane.addWidget(tabele_tabs)
okno.addTab(dane_widget, "Dane")

# Stylizacja zakładek (opcjonalnie)
okno.setStyleSheet("""
    QTabBar::tab {
        background: lightgray;
        padding: 8px;
        border: 1px solid gray;
        border-bottom: none;
        min-width: 120px;
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
okno.resize(700, 400)
okno.show()

sys.exit(app.exec())
