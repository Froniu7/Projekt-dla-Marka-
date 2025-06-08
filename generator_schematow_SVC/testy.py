import os

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    current_dir = os.getcwd()

TEMP_PDF = os.path.join(current_dir, "schemat.pdf")

if not os.path.exists(TEMP_PDF):
    print("nie znaleziono pliku pdf")
else:
    print("plik pdf znaleziony:", TEMP_PDF)
