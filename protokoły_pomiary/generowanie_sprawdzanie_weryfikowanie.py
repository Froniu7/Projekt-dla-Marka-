import datetime


def oblicz_prad_zadzialania(typ_zabezpieczenia, prad_znamionowy):
    """Oblicza prąd zadziałania Ia na podstawie typu zabezpieczenia."""

    charakterystyka = typ_zabezpieczenia[0].upper()

    if charakterystyka == 'B':
        ia = 5 * prad_znamionowy
    elif charakterystyka == 'C':
        ia = 10 * prad_znamionowy
    elif charakterystyka == 'G':
        ia = 5 * prad_znamionowy
    else:
        return None, "Nieobsługiwana charakterystyka zabezpieczenia (obsługiwane: B, C, gG)."

    return ia, None


def generuj_protokol():
    """Generuje protokół z pomiaru impedancji pętli zwarcia."""

    print("--- Generator protokołów pomiaru impedancji pętli zwarcia ---")

    # Dane do wprowadzenia przez użytkownika
    lokalizacja = input("Podaj lokalizację pomiaru (np. Gniazdo 1, Oświetlenie Kuchnia): ")
    rodzaj_sieci = input("Podaj rodzaj sieci (np. TN-C-S, TN-S, TT): ").upper().strip()
    typ_zabezpieczenia = input("Podaj typ zabezpieczenia (np. C16, B10, gG10): ").strip()
    try:
        impedancja_zmierzona = float(input("Podaj zmierzoną impedancję Zz [Ω]: "))
    except ValueError:
        print("Błąd: Wprowadzona wartość impedancji musi być liczbą. Spróbuj ponownie.")
        return

    # Ustalanie danych na podstawie typu zabezpieczenia
    try:
        prad_znamionowy = int(''.join(filter(str.isdigit, typ_zabezpieczenia)))
    except ValueError:
        print("Błąd: Niepoprawny format typu zabezpieczenia. Wpisz np. C16, B10 lub gG10.")
        return

    prad_zadzialania_Ia, blad = oblicz_prad_zadzialania(typ_zabezpieczenia, prad_znamionowy)

    if blad:
        print(f"Błąd: {blad}")
        return

    # Ustalanie czasu wyłączenia Ta na podstawie rodzaju sieci
    if rodzaj_sieci in ['TN-C-S', 'TN-S', 'TN-C']:
        czas_wylaczenia_Ta = 0.4
    elif rodzaj_sieci == 'TT':
        czas_wylaczenia_Ta = 0.2
    else:
        print("Błąd: Nieobsługiwany rodzaj sieci (obsługiwane: TN-C-S, TN-S, TN-C, TT).")
        return

    # Automatyczne obliczenia
    napiecie_znamionowe = 230  # V

    if prad_zadzialania_Ia == 0:
        print("Błąd: Prąd zadziałania Ia nie może być zerowy.")
        return

    impedancja_dopuszczalna = napiecie_znamionowe / prad_zadzialania_Ia
    prad_zwarcia_Isc = napiecie_znamionowe / impedancja_zmierzona

    # Ocena pomiaru i generowanie uwag
    ocena = "TAK"
    uwagi = "Pomiar poprawny."
    if prad_zwarcia_Isc < prad_zadzialania_Ia:
        ocena = "NIE"
        uwagi = "Niska wartość obliczeniowego prądu zwarcia (Isc). Możliwa błędna instalacja, luźne połączenie lub błąd w pomiarze."

    # Przygotowanie danych do zapisu w pliku
    tresc_protokolu = f"""
==================================================
        PROTOKÓŁ Z POMIARU IMPEDANCJI PĘTLI ZWARCIA
==================================================
Data wykonania: {datetime.date.today()}
Lokalizacja pomiaru: {lokalizacja}
Rodzaj sieci: {rodzaj_sieci}

--- Dane zabezpieczenia ---
Typ zabezpieczenia: {typ_zabezpieczenia.upper()}
Prąd znamionowy In: {prad_znamionowy} A
Prąd zadziałania Ia: {prad_zadzialania_Ia} A
Dopuszczalny czas wyłączenia Ta: {czas_wylaczenia_Ta} s

--- Wyniki pomiaru ---
Impedancja zmierzona Zz: {impedancja_zmierzona:.2f} Ω
Impedancja dopuszczalna Zd: {impedancja_dopuszczalna:.2f} Ω
Obliczeniowy prąd zwarcia Isc: {prad_zwarcia_Isc:.2f} A
(wymagana wartość >= {prad_zadzialania_Ia} A)

--- Ocena ---
Pomiar pomyślny? {ocena}
Uwagi: {uwagi}

"""
    # Zapis do pliku
    nazwa_pliku = "protokol_pomiaru.txt"
    try:
        with open(nazwa_pliku, "w", encoding='utf-8') as plik:
            plik.write(tresc_protokolu)
        print(f"\nProtokół został wygenerowany i zapisany do pliku '{nazwa_pliku}'.")
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisu pliku: {e}")


# Uruchomienie programu
if __name__ == "__main__":
    generuj_protokol()