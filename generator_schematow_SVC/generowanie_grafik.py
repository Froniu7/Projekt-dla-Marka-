

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

def generuj_plik_docx(sciezka_obrazu, sciezka_docx):
    from docx import Document
    from docx.shared import Inches
    doc = Document()
    doc.add_paragraph("To jest obrazek:")
    doc.add_picture(sciezka_obrazu, width=Inches(4))
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



