import sys, os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
from glowny.funkcje import resource_path, resource_path_all

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uruchamianie programów")

        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Generator Standardowe schematy")
        self.button1.clicked.connect(self.run_notepad)

        self.button2 = QPushButton("Generator SVC")
        self.button2.clicked.connect(self.run_generator_SVC)

        self.button3 = QPushButton("Generator Schematy podłączenia")
        self.button3.clicked.connect(self.run_pdf)

        self.button4 = QPushButton("Generator Schematy jednokreskowe")
        self.button4.clicked.connect(self.run_pdf)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)

        self.setLayout(self.layout)

    def run_notepad(self):
        subprocess.Popen(["notepad.exe"])

    def run_generator_SVC(self):

        sciezka2 = resource_path_all(r'generator_schematow_SVC\generowanie_schematy_SVC.exe')
        sciezka1 = resource_path_all(r'generator_schematow_SVC')
        subprocess.Popen([sciezka2], cwd=sciezka1)

    def run_pdf(self):
        try:
            subprocess.Popen(["C:/Program Files/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe", "plik.pdf"])
        except FileNotFoundError:
            QMessageBox.warning(self, "Błąd", "Nie znaleziono programu do otwierania PDF.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
