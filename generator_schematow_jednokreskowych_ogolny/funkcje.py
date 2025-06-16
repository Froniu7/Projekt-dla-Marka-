from PIL import Image

from dobor_przewodu_zasilajacego_i_zabezpieczen.dobor_przewodu_zas_i_zab import zabezpieczenie


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
    bbox = draw.textbbox((0, 0), f"{tekst}", font=czcionka)
    tekst_szerokosc = bbox[2] - bbox[0]
    tekst_wysokosc = bbox[3] - bbox[1]

    # Środek obrazu
    pozycja = ((szerokosc - tekst_szerokosc) // 2, (wysokosc - tekst_wysokosc) // 2)

    # Rysuj tekst
    draw.text(pozycja, f"{tekst}", fill='black', font=czcionka)

    # Zapisz
    obraz.save(nazwa_pliku)
    print(f"Grafika zapisana jako {nazwa_pliku}")

def generuj_grafiki_do_schematu(cable, control, przekladnik, zabezpieczenie):
    generuj_grafike_z_tekstem(tekst=cable, szerokosc=300, wysokosc=80, rozmiar_fonta=50,
                              nazwa_pliku="przewod_kablowy.png")
    generuj_grafike_z_tekstem(tekst=control, szerokosc=400, wysokosc=100, rozmiar_fonta=50,
                              nazwa_pliku="przewod_sterowniczy.png")
    generuj_grafike_z_tekstem(tekst=przekladnik, szerokosc=600, wysokosc=100, rozmiar_fonta=50,
                              nazwa_pliku="przekladnik.png")
    generuj_grafike_z_tekstem(tekst=zabezpieczenie, szerokosc=100, wysokosc=100, rozmiar_fonta=50,
                              nazwa_pliku="zabezpiecznie.png")


def generowanie_schematu_jednokreskowego(rodzaj_zab):
    print("Generowanie schematu jednokreskowego.")
    if rodzaj_zab == "typ S Cx A":
        schemat_jednokreskowy = Image.open("schematy_zabezpiecznie_C/schemat_jednokreskowy_SVC_C.png")
    elif rodzaj_zab == "wkładki gG":
        schemat_jednokreskowy = Image.open("schematy_zabezpiecznie_gG/schemat_jednokreskowy_SVC_gG.png")
    else:
        schemat_jednokreskowy = Image.open("schematy_zabezpiecznie_brak/schemat_jednokreskowy_SVC_brak.png")
    width_schemat, height_schemat = schemat_jednokreskowy.size
    print(f"width {width_schemat}")
    print(f"height {height_schemat}")

    przewod_kablowy = Image.open("przewod_kablowy.png")
    przewod_sterowniczy = Image.open("przewod_sterowniczy.png")
    przekladnik = Image.open("przekladnik.png")
    zabezpieczenie = Image.open("zabezpiecznie.png")
    obraz_do_wygenerowania = Image.new("RGBA", (width_schemat, height_schemat))
    obraz_do_wygenerowania.paste(schemat_jednokreskowy, (0, 0))
    obraz_do_wygenerowania.paste(przewod_kablowy, (2300, 980))
    obraz_do_wygenerowania.paste(przewod_sterowniczy,(1300,1000))
    obraz_do_wygenerowania.paste(przekladnik, (1230, 100))
    obraz_do_wygenerowania.paste(zabezpieczenie,(3000,800))

    obraz_do_wygenerowania.save(f"schemat_jednokreskowy.png")
    print("Został wygenerowany shemat jednokreskowy.")

