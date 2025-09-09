from PySide6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHBoxLayout
)
import sys
import csv
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy

import subprocess
import os
import sys, os
import subprocess
from glowny.funkcje import resource_path, resource_path_all

from datetime import datetime
import json

ścieżka_json = "komunikacja.json"

def generuj_nazwe_json(prefix="schemat", suffix=".json"):
    teraz = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{teraz}{suffix}"


def utworz_tabele_z_csv(sciezka):
    with open(sciezka, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        wiersze = list(reader)

    if not wiersze:
        return QTableWidget()

    naglowki = wiersze[0]
    dane = wiersze[1:]
    tabela = QTableWidget(len(dane), len(naglowki))
    tabela.setHorizontalHeaderLabels(naglowki)

    for i, wiersz in enumerate(dane):
        for j, komorka in enumerate(wiersz):
            tabela.setItem(i, j, QTableWidgetItem(komorka))

    tabela.resizeColumnsToContents()
    tabela.setShowGrid(True)
    return tabela

app = QApplication(sys.argv)

# Główne okno z zakładkami
okno = QTabWidget()

# Zakładka 1: Generowanie schematów
widget_generowanie = QWidget()
layout_generowanie = QVBoxLayout(widget_generowanie)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem

# Kontener na przyciski z ograniczoną wysokością
kontener_przyciski = QWidget()
kontener_przyciski.setMaximumHeight(220)  # maksymalna wysokość całej sekcji z przyciskami
kontener_layout = QVBoxLayout(kontener_przyciski)

# Wiersz 1: opis + przycisk 1
layout_wiersz1 = QVBoxLayout()
layout_wiersz1.addWidget(QLabel("Etap 1 : Kliknij na przycisk i wybierz dane do wygenrowania schematu podłączenia:"))

wiersz1 = QHBoxLayout()
wiersz1.addStretch()  # wypycha przycisk na prawo
przycisk1 = QPushButton("Generuj schematy podłączenia")
przycisk1.setMinimumSize(150, 40)
przycisk1.setMaximumSize(300, 50)
przycisk1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
wiersz1.addWidget(przycisk1)
layout_wiersz1.addLayout(wiersz1)

# Wiersz 2: opis + przycisk 2
layout_wiersz2 = QVBoxLayout()
layout_wiersz2.addWidget(QLabel("Etap 2 : Generowanie schematu urządzenia:"))

wiersz2 = QHBoxLayout()
wiersz2.addStretch()  # wypycha przycisk na prawo
przycisk2 = QPushButton("Generuj schemat urządzenia")
przycisk2.setMinimumSize(150, 40)
przycisk2.setMaximumSize(300, 50)
przycisk2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
wiersz2.addWidget(przycisk2)
layout_wiersz2.addLayout(wiersz2)

# Dodanie obu wierszy do kontenera
kontener_layout.addLayout(layout_wiersz1)
kontener_layout.addLayout(layout_wiersz2)
kontener_layout.addStretch()  # wypycha wszystko do góry

# Dodanie kontenera do layoutu zakładki "Generowanie schematów"
layout_generowanie.addWidget(kontener_przyciski)
layout_generowanie.addStretch()  # wypycha wszystko do góry w zakładce

okno.addTab(widget_generowanie, "Generowanie schematów")

# Zakładka 2: Dane (z podzakładkami)
widget_dane = QWidget()
layout_dane = QVBoxLayout(widget_dane)
tabele_tabs = QTabWidget()

def uruchom_program_generuj():
    nazwa_pliku = generuj_nazwe_json()
    print(f"zostanie przekazany argument :  {nazwa_pliku}")

    sciezka2 = resource_path_all(r'generator_schematow_jednokreskowych_ogolny\generator_schematow_jednokreskowych.py')
    sciezka1 = resource_path_all(r'generator_schematow_jednokreskowych_ogolny')
    subprocess.Popen(["python", sciezka2, nazwa_pliku], cwd=sciezka1)


def uruchom_program_podglad():

    sciezka2 = resource_path_all(r'generator_schematow_SVC\generowanie_schematy_SVC.exe')
    sciezka1 = resource_path_all(r'generator_schematow_SVC')
    subprocess.Popen([sciezka2], cwd=sciezka1)

przycisk1.clicked.connect(uruchom_program_generuj)
przycisk2.clicked.connect(uruchom_program_podglad)

def dodaj_tabele_z_csv(nazwa, sciezka):
    tabela = utworz_tabele_z_csv(sciezka)
    podwidget = QWidget()
    layout = QVBoxLayout(podwidget)
    layout.addWidget(tabela)
    tabele_tabs.addTab(podwidget, nazwa)

dodaj_tabele_z_csv("zabezpieczenia-SVG", "dane/zabezpieczeniaSVGgG[1].csv")
dodaj_tabele_z_csv("Dobór przekroje", "dane/moc_przekroj.csv")
dodaj_tabele_z_csv("Zabezpieczenia C i gG", "dane/zabezpieczenia_C_gG.csv")
dodaj_tabele_z_csv("Przewody zasilające", "dane/przewody_miedziane_B2.csv")
dodaj_tabele_z_csv("Przekładniki", "dane/przekladniki.csv")
dodaj_tabele_z_csv("Sterownicze", "dane/przewody_sterownicze.csv")
dodaj_tabele_z_csv("Sterowniki", "dane/sterowniki.csv")

layout_dane.addWidget(tabele_tabs)
okno.addTab(widget_dane, "Dane")

# Styl zakładek
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
okno.resize(600, 400)
okno.show()
sys.exit(app.exec())
