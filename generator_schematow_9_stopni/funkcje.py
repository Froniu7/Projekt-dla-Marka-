
def read_rows(file_path):
    import csv
    #utworzenie obiektu reader -
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        try:
            first_row = next(reader)  # Pobranie pierwszego wiersza
            first_row = [x for x in first_row if x != '']
            second_row = next(reader)  # Pobranie drugiego wiersza
            second_row = [x for x in second_row if x != '']
            third_row = next(reader)  # Pobranie trzeciego wiersza
            third_row = [x for x in third_row if x != '']

            return first_row, second_row, third_row

        except StopIteration:
            print("Błąd: Plik CSV zawiera mniej niż trzy wiersze.")
            return None, None, None

def generowanie_schematow_elementy1fazowe(faza1, faza2, faza3, Image_path, nazwa_pliku_graficznego):
    '''

    funkcja do generowania schematow z elementow 1 fazowych dla sterownika 9 stopniowego
    funkcja przyjmuje rowne ilosci elementow na faze,

    '''

    from PIL import Image

    # sytuacja kiedy mamy po tyle samo elementow jedno fazowych, wiec nie wystepuja trzy fazowe
    if (len(faza1) == len(faza2)) and (len(faza1) == len(faza3)):

        # policzenie ile wystepuje elementow 1 fazowych na faze
        liczba_elementow_1_fazowych = len(faza1)
        print(f"liczba elementów jedno fazowych to {liczba_elementow_1_fazowych}")

        # policzenie wszystkich elementow
        liczba_wszystkich_elementow = liczba_elementow_1_fazowych * 3

        print(f"uklad posiada rzedow 1 fazowych : {liczba_elementow_1_fazowych}")

        # zaladowanie grafiki sieci i zwymiarowanie
        siec = Image.open(f"{Image_path}1_siec_elektryczna/siec_zabezpieczenie_wewnetrzne.png")
        width_siec, height_siec = siec.size

        # obliczenieilosci stopni, zaladowanie grafiki i zwymiarowanie
        if (liczba_wszystkich_elementow == 3):
            stopnie = Image.open(f"{Image_path}2_podpiecie_stopnie/styczniki3.png")
        if (liczba_wszystkich_elementow == 6):
            stopnie = Image.open(f"{Image_path}2_podpiecie_stopnie/styczniki6.png")
        if (liczba_wszystkich_elementow == 9):
            stopnie = Image.open(f"{Image_path}2_podpiecie_stopnie/styczniki9.png")

        width_stopnie, height_stopnie = stopnie.size

        # sterownik - zaladowanie grafiki i zwymiarowanie
        sterownik = Image.open(f"{Image_path}3_sterownik/Sterownik.png")
        width_sterownik, height_sterownik = sterownik.size

        # kable - zaladowanie grafik i zwymiarowanie
        if (liczba_wszystkich_elementow > 3):
            kable_1_1 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza1.png")
            width_kable_1_1, height_kable_1_1 = kable_1_1.size

            kable_2_1 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza2.png")
            width_kable_2_1, height_kable_2_1 = kable_2_1.size

            kable_3_1 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza3.png")
            width_kable_3_1, height_kable_3_1 = kable_3_1.size

        if (liczba_wszystkich_elementow == 3):
            kable_1_1 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza1_ostatnia_sapozostale.png")
            width_kable_1_1, height_kable_1_1 = kable_1_1.size

            kable_2_1 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza2_ostatnia_sapozostale.png")
            width_kable_2_1, height_kable_2_1 = kable_2_1.size

            kable_3_1 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza3_ostatnia_sapozostale.png")
            width_kable_3_1, height_kable_3_1 = kable_3_1.size

        if (liczba_wszystkich_elementow > 6):
            kable_1_2 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza1.png")
            width_kable_1_2, height_kable_1_2 = kable_1_2.size

            kable_2_2 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza2.png")
            width_kable_2_2, height_kable_2_2 = kable_2_2.size

            kable_3_2 = Image.open(f"{Image_path}5_kable_stopnie/1_jednofazowe/podpiecie_faza3.png")
            width_kable_3_2, height_kable_3_2 = kable_3_2.size

        if (liczba_wszystkich_elementow == 6):
            kable_1_2 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza1_ostatnia_sapozostale.png")
            width_kable_1_2, height_kable_1_2 = kable_1_2.size

            kable_2_2 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza2_ostatnia_sapozostale.png")
            width_kable_2_2, height_kable_2_2 = kable_2_2.size

            kable_3_2 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza3_ostatnia_sapozostale.png")
            width_kable_3_2, height_kable_3_2 = kable_3_2.size

        if (liczba_wszystkich_elementow == 9):
            kable_1_3 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza1_ostatnia_sapozostale.png")
            width_kable_1_3, height_kable_1_3 = kable_1_3.size

            kable_2_3 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza2_ostatnia_sapozostale.png")
            width_kable_2_3, height_kable_2_3 = kable_2_3.size

            kable_3_3 = Image.open(
                f"{Image_path}5_kable_stopnie/1_jednofazowe_ostatnie/podpiecie_faza3_ostatnia_sapozostale.png")
            width_kable_3_3, height_kable_3_3 = kable_3_3.size

        # zabezpieczenia wewnetrzne - zaladowanie grafiki i zwymiarowanie

        zabezpieczenia = Image.open(f"{Image_path}4_zabezpieczenia/zabezpieczenia_plus_wew_C.png")
        width_kable_zabezpieczenia, height_kable_zabezpieczenia = zabezpieczenia.size

        # stopnie - zaladowanie i zwymiarowanie ( bloki z kondensatorami badź dlawikami )
        # sprawdzenie kondensatory czy dlawiki

        if faza1[0].startswith('-'):  # sprawdzenie czy to dławik
            stopien_1_1 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            width_stopien_1_1, height_stopien_1_1 = stopien_1_1.size
        else:
            stopien_1_1 = Image.open(f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_1_1, height_stopien_1_1 = stopien_1_1.size

        if faza2[0].startswith('-'):  # sprawdzenie czy to dławik
            stopien_2_1 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            width_stopien_2_1, height_stopien_2_1 = stopien_2_1.size
        else:
            stopien_2_1 = Image.open(f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_2_1, height_stopien_2_1 = stopien_2_1.size

        if faza3[0].startswith('-'):  # sprawdzenie czy to dławik
            stopien_3_1 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            width_stopien_3_1, height_stopien_3_1 = stopien_3_1.size
        else:
            stopien_3_1 = Image.open(f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_3_1, height_stopien_3_1 = stopien_3_1.size

        if (liczba_wszystkich_elementow >= 4):
            if faza1[1].startswith('-'):  # sprawdzenie czy to dławik
                stopien_1_2 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                width_stopien_1_2, height_stopien_1_2 = stopien_1_2.size
            else:
                stopien_1_2 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
                width_stopien_1_2, height_stopien_1_2 = stopien_1_2.size

            if faza2[1].startswith('-'):  # sprawdzenie czy to dławik
                stopien_2_2 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                width_stopien_2_2, height_stopien_2_2 = stopien_2_2.size
            else:
                stopien_2_2 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
                width_stopien_2_2, height_stopien_2_2 = stopien_2_2.size

            if faza3[1].startswith('-'):  # sprawdzenie czy to dławik
                stopien_3_2 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                width_stopien_3_2, height_stopien_3_2 = stopien_3_2.size
            else:
                stopien_3_2 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
                width_stopien_3_2, height_stopien_3_2 = stopien_3_2.size

        if (liczba_wszystkich_elementow == 9):
            if faza1[2].startswith('-'):  # sprawdzenie czy to dławik
                stopien_1_3 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            else:
                stopien_1_3 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_1_3, height_stopien_1_3 = stopien_1_3.size

            if faza2[2].startswith('-'):  # sprawdzenie czy to dławik
                stopien_2_3 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            else:
                stopien_2_3 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_2_3, height_stopien_2_3 = stopien_2_3.size

            if faza3[2].startswith('-'):  # sprawdzenie czy to dławik
                stopien_3_3 = Image.open(f"{Image_path}6_stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
            else:
                stopien_3_3 = Image.open(
                    f"{Image_path}6_stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")
            width_stopien_3_3, height_stopien_3_3 = stopien_3_3.size

        # oznaczenia stopni - zaladowanie i zwymarowanie
        if faza1[0].startswith('-'):  # sprawdzenie czy to dławik
            oznaczenie_1_1 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L1.png")
        else:
            oznaczenie_1_1 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C1.png")
        width_oznaczenie_1_1, height_oznaczenie_1_1 = oznaczenie_1_1.size
        if faza2[0].startswith('-'):  # sprawdzenie czy to dławik
            oznaczenie_2_1 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L2.png")
        else:
            oznaczenie_2_1 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C2.png")
        width_oznaczenie_2_1, height_oznaczenie_2_1 = oznaczenie_2_1.size
        if faza3[0].startswith('-'):  # sprawdzenie czy to dławik
            oznaczenie_3_1 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L3.png")
        else:
            oznaczenie_3_1 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C3.png")
        width_oznaczenie_3_1, height_oznaczenie_3_1 = oznaczenie_3_1.size

        if (liczba_wszystkich_elementow >= 4):
            if faza1[1].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_1_2 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L4.png")
            else:
                oznaczenie_1_2 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C4.png")
            width_oznaczenie_1_2, height_oznaczenie_1_2 = oznaczenie_1_2.size
            if faza1[1].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_2_2 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L5.png")
            else:
                oznaczenie_2_2 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C5.png")
            width_oznaczenie_2_2, height_oznaczenie_2_2 = oznaczenie_2_2.size
            if faza3[1].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_3_2 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L6.png")
            else:
                oznaczenie_3_2 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C6.png")
            width_oznaczenie_3_2, height_oznaczenie_3_2 = oznaczenie_3_2.size

        if (liczba_wszystkich_elementow == 9):
            if faza1[2].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_1_3 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L7.png")
            else:
                oznaczenie_1_3 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C7.png")
            width_oznaczenie_1_3, height_oznaczenie_1_3 = oznaczenie_1_3.size
            if faza1[2].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_2_3 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L8.png")
            else:
                oznaczenie_2_3 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C8.png")
            width_oznaczenie_2_3, height_oznaczenie_2_3 = oznaczenie_2_3.size
            if faza3[2].startswith('-'):  # sprawdzenie czy to dławik
                oznaczenie_3_3 = Image.open(f"{Image_path}7_numery_stopni/1_dlawiki/L9.png")
            else:
                oznaczenie_3_3 = Image.open(f"{Image_path}7_numery_stopni/2_kondensatory/C9.png")
            width_oznaczenie_3_3, height_oznaczenie_3_3 = oznaczenie_3_3.size

        obraz_poskladany = Image.new("RGBA", (width_siec + width_stopnie, height_siec))
        # siec umiejscownienie grafiki
        obraz_poskladany.paste(siec, (0, 0))  # Wklejamy pierwszy obraz w lewy górny róg
        # stopnie umiejscownienie grafiki
        obraz_poskladany.paste(stopnie, (width_siec, 0))  # Wklejamy pierwszy obraz w lewy górny róg
        # sterownik umiejscownienie grafiki
        obraz_poskladany.paste(sterownik, (width_siec, height_stopnie))
        # kable
        obraz_poskladany.paste(kable_1_1, (width_siec + width_sterownik, height_stopnie))
        obraz_poskladany.paste(kable_2_1, (width_siec + width_sterownik + width_kable_1_1, height_stopnie))
        obraz_poskladany.paste(kable_3_1,
                               (width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1, height_stopnie))
        if (liczba_wszystkich_elementow >= 4):
            obraz_poskladany.paste(kable_1_2, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1, height_stopnie))
            obraz_poskladany.paste(kable_2_2, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1 + width_kable_1_2,
                height_stopnie))
            obraz_poskladany.paste(kable_3_2, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1 + width_kable_1_2 + width_kable_2_2,
                height_stopnie))
        if (liczba_wszystkich_elementow == 9):
            obraz_poskladany.paste(kable_1_3, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1 + width_kable_1_2 + width_kable_2_2 + width_kable_3_2,
                height_stopnie))
            obraz_poskladany.paste(kable_2_3, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1 + width_kable_1_2 + width_kable_2_2 + width_kable_3_2 + width_kable_1_3,
                height_stopnie))
            obraz_poskladany.paste(kable_3_3, (
                width_siec + width_sterownik + width_kable_1_1 + width_kable_2_1 + width_kable_3_1 + width_kable_1_2 + width_kable_2_2 + width_kable_3_2 + width_kable_1_3 + width_kable_2_3,
                height_stopnie))

        # zabezpieczenia wewnetrzne
        obraz_poskladany.paste(zabezpieczenia, (width_siec, height_stopnie + height_sterownik))
        # stopnie
        obraz_poskladany.paste(stopien_1_1, (width_siec + width_sterownik, height_stopnie + height_kable_1_1))
        obraz_poskladany.paste(stopien_2_1,
                               (width_siec + width_sterownik + width_stopien_1_1, height_stopnie + height_kable_1_1))
        obraz_poskladany.paste(stopien_3_1, (
        width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1, height_stopnie + height_kable_1_1))
        if (liczba_wszystkich_elementow >= 4):
            obraz_poskladany.paste(stopien_1_2, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1,
                height_stopnie + height_kable_1_1))
            obraz_poskladany.paste(stopien_2_2, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1 + width_stopien_1_2,
                height_stopnie + height_kable_1_1))
            obraz_poskladany.paste(stopien_3_2, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1 + width_stopien_1_2 + width_stopien_2_2,
                height_stopnie + height_kable_1_1))
        if (liczba_wszystkich_elementow == 9):
            obraz_poskladany.paste(stopien_1_3, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1 + width_stopien_1_2 + width_stopien_2_2 + width_stopien_3_2,
                height_stopnie + height_kable_1_1))
            obraz_poskladany.paste(stopien_2_3, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1 + width_stopien_1_2 + width_stopien_2_2 + width_stopien_3_2 + width_stopien_1_3,
                height_stopnie + height_kable_1_1))
            obraz_poskladany.paste(stopien_2_3, (
                width_siec + width_sterownik + width_stopien_1_1 + width_stopien_2_1 + width_stopien_3_1 + width_stopien_1_2 + width_stopien_2_2 + width_stopien_3_2 + width_stopien_1_3 + width_stopien_2_3,
                height_stopnie + height_kable_1_1))

        # oznaczenia
        obraz_poskladany.paste(oznaczenie_1_1,
                               (width_siec + width_sterownik, height_stopnie + height_kable_1_1 + height_stopien_1_1))
        obraz_poskladany.paste(oznaczenie_2_1,
                               (width_siec + width_sterownik + width_oznaczenie_1_1,
                                height_stopnie + height_kable_1_1 + height_stopien_1_1))
        obraz_poskladany.paste(oznaczenie_3_1,
                               (width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1,
                                height_stopnie + height_kable_1_1 + height_stopien_1_1))
        if (liczba_wszystkich_elementow >= 4):
            obraz_poskladany.paste(oznaczenie_1_2,
                                   (
                                   width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1,
                                   height_stopnie + height_kable_1_1 + height_stopien_1_1))
            obraz_poskladany.paste(oznaczenie_2_2,
                                   (
                                       width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1 + width_oznaczenie_1_2,
                                       height_stopnie + height_kable_1_1 + height_stopien_1_1))
            obraz_poskladany.paste(oznaczenie_3_2,
                                   (
                                       width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1 + width_oznaczenie_1_2 + width_oznaczenie_2_2,
                                       height_stopnie + height_kable_1_1 + height_stopien_1_1))
        if (liczba_wszystkich_elementow == 9):
            obraz_poskladany.paste(oznaczenie_1_3,
                                   (
                                       width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1 + width_oznaczenie_1_2 + width_oznaczenie_2_2 + width_oznaczenie_3_2,
                                       height_stopnie + height_kable_1_1 + height_stopien_1_1))
            obraz_poskladany.paste(oznaczenie_2_3,
                                   (
                                       width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1 + width_oznaczenie_1_2 + width_oznaczenie_2_2 + width_oznaczenie_3_2 + width_oznaczenie_1_3,
                                       height_stopnie + height_kable_1_1 + height_stopien_1_1))
            obraz_poskladany.paste(oznaczenie_3_3,
                                   (
                                       width_siec + width_sterownik + width_oznaczenie_1_1 + width_oznaczenie_2_1 + width_oznaczenie_3_1 + width_oznaczenie_1_2 + width_oznaczenie_2_2 + width_oznaczenie_3_2 + width_oznaczenie_1_3 + width_oznaczenie_2_3,
                                       height_stopnie + height_kable_1_1 + height_stopien_1_1))


    obraz_poskladany.save(f"{nazwa_pliku_graficznego}.png")

