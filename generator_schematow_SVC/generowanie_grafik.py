

def generuj_grafike_z_tekstem(tekst, szerokosc, wysokosc, rozmiar_fonta, nazwa_pliku):
    from PIL import Image, ImageDraw, ImageFont
    # Tworzymy pusty biały obraz
    obraz = Image.new('RGBA', (szerokosc, wysokosc), color=(0,0,0,0))

    # Obiekt do rysowania
    draw = ImageDraw.Draw(obraz)

    # Czcionka – jeśli nie masz arial.ttf, załadujemy domyślną
    try:
        czcionka = ImageFont.truetype("arial.ttf", rozmiar_fonta)
    except IOError:
        czcionka = ImageFont.load_default()

    # Oblicz wymiary tekstu za pomocą textbbox
    bbox = draw.textbbox((0, 0), f"{tekst} kVAr", font=czcionka)
    tekst_szerokosc = bbox[2] - bbox[0]
    tekst_wysokosc = bbox[3] - bbox[1]

    # Środek obrazu
    pozycja = ((szerokosc - tekst_szerokosc) // 2, (wysokosc - tekst_wysokosc) // 2)

    # Rysuj tekst
    draw.text(pozycja, f"{tekst} kVAr", fill='black', font=czcionka)

    # Zapisz
    obraz.save(nazwa_pliku)
    print(f"Grafika zapisana jako {nazwa_pliku}")

#generuj_grafike_z_tekstem("4",1299, 300,100,"grafika.png")

from docx.shared import Cm

def generuj_plik_docx(sciezka_obrazu, sciezka_docx):
    from docx import Document
    from docx.shared import Inches, Cm

    doc = Document()

    # Ustaw marginesy na 1 cm
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(1)
        section.bottom_margin = Cm(1)
        section.left_margin = Cm(1)
        section.right_margin = Cm(1)

    # Oblicz szerokość do wykorzystania: szerokość strony - marginesy
    section = doc.sections[0]
    szerokosc_strony = section.page_width  # w EMU
    lewy_margin = section.left_margin
    prawy_margin = section.right_margin
    szerokosc_do_wykorzystania = szerokosc_strony - lewy_margin - prawy_margin

    doc.add_paragraph("Schemat urządzenia SVC:")

    # Dodaj obraz o maksymalnej szerokości (EMU to jednostka używana przez python-docx)
    doc.add_picture(sciezka_obrazu, width=szerokosc_do_wykorzystania)
    doc.save(sciezka_docx)

def konwertuj_docx_na_pdf(sciezka_docx):
    import subprocess
    import os
    sciezka_docx = os.path.abspath(sciezka_docx)
    katalog_wyjscia = os.path.dirname(sciezka_docx)

    # PEŁNA ŚCIEŻKA do LibreOffice w Windows
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    subprocess.run([
        libreoffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", katalog_wyjscia,
        sciezka_docx
    ], check=True)

    print(f"PDF zapisany w katalogu: {katalog_wyjscia}")


import shutil
import os
from tkinter import filedialog
from tkinter import Tk

def zapisz_plik_do_katalogu(sciezka_pliku):
    # Ukryj główne okno Tkintera
    root = Tk()
    root.withdraw()

    # Domyślna nazwa pliku
    domyslna_nazwa = os.path.basename(sciezka_pliku)

    # Okno do wyboru lokalizacji i nazwy pliku
    sciezka_docelowa = filedialog.asksaveasfilename(
        title="Zapisz plik jako",
        initialfile=domyslna_nazwa,
        defaultextension=os.path.splitext(domyslna_nazwa)[1],
        filetypes=[("Wszystkie pliki", "*.*")]
    )

    if not sciezka_docelowa:
        print("Anulowano zapis.")
        return

    try:
        shutil.copy2(sciezka_pliku, sciezka_docelowa)
        print(f"Plik zapisany do: {sciezka_docelowa}")
    except Exception as e:
        print(f"Błąd podczas zapisu pliku: {e}")

import tkinter as tk
def show_non_blocking_message(parent, message):
    win = tk.Toplevel(parent)
    win.title("Ładowanie")
    win.transient(parent)
    win.geometry("250x100")
    #tk.Label(win, text=message).pack(pady=20)
    #tk.Button(win, text="Zamknij", command=win.destroy).pack()
    return win

def close_message_window(window):
    if window.winfo_exists():
        window.destroy()


