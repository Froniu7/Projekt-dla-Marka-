import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QFileDialog, QMessageBox
)
from docx import Document
from docxcompose.composer import Composer


class ScalaczDocx(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scalacz DOCX")
        self.resize(400, 200)

        self.plik1 = None
        self.plik2 = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Przycisk 1
        self.button1 = QPushButton("1. Załaduj pierwszy plik")
        self.button1.clicked.connect(self.wybierz_plik1)
        layout.addWidget(self.button1)

        # Przycisk 2
        self.button2 = QPushButton("2. Załaduj drugi plik")
        self.button2.clicked.connect(self.wybierz_plik2)
        layout.addWidget(self.button2)

        # Przycisk 3
        self.button3 = QPushButton("3. Połącz pliki")
        self.button3.clicked.connect(self.polacz_pliki)
        layout.addWidget(self.button3)

        # Informacja o wybranych plikach
        self.label_info = QLabel("Nie wybrano plików.")
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def wybierz_plik1(self):
        plik, _ = QFileDialog.getOpenFileName(self, "Wybierz pierwszy plik DOCX", filter="Dokumenty Word (*.docx)")
        if plik:
            self.plik1 = plik
            self.aktualizuj_etykiete()

    def wybierz_plik2(self):
        plik, _ = QFileDialog.getOpenFileName(self, "Wybierz drugi plik DOCX", filter="Dokumenty Word (*.docx)")
        if plik:
            self.plik2 = plik
            self.aktualizuj_etykiete()

    def aktualizuj_etykiete(self):
        t1 = self.plik1 if self.plik1 else "[brak]"
        t2 = self.plik2 if self.plik2 else "[brak]"
        self.label_info.setText(f"Plik 1: {t1}\nPlik 2: {t2}")

    def polacz_pliki(self):
        if not self.plik1 or not self.plik2:
            QMessageBox.warning(self, "Błąd", "Wybierz oba pliki przed połączeniem.")
            return

        try:
            doc1 = Document(self.plik1)
            doc2 = Document(self.plik2)
            composer = Composer(doc1)
            composer.append(doc2)

            wynik = "polaczony.docx"
            composer.save(wynik)

            QMessageBox.information(self, "Sukces", f"Pliki zostały połączone jako: {wynik}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = ScalaczDocx()
    okno.show()
    sys.exit(app.exec())
