import datetime


def oblicz_prad_zadzialania(typ_zabezpieczenia, prad_znamionowy):
    """Oblicza prąd zadziałania Ia na podstawie typu zabezpieczenia."""

    charakterystyka = typ_zabezpieczenia[0].upper()

    if charakterystyka == 'B':
        wspolczynnik = 5
        ia = wspolczynnik * prad_znamionowy
    elif charakterystyka == 'C':
        wspolczynnik = 10
        ia = wspolczynnik * prad_znamionowy
    elif charakterystyka == 'G':
        # Dla wkładek gG przyjmuje się, że Ia = 4*In dla czasów < 0.2s
        # lub 5*In dla czasów < 0.4s.
        # W praktyce przyjmuje się wartość prądu wyzwalania natychmiastowego
        # zgodnie z normą IEC 60898 lub PN-EN 60898.
        # W tym uproszczonym modelu, przyjęto stały współczynnik
        # jako wystarczający do celów ilustracyjnych.
        wspolczynnik = 5  # Przyjęto 5xIn dla uproszczenia
        ia = wspolczynnik * prad_znamionowy
    else:
        return None, "Nieobsługiwana charakterystyka zabezpieczenia (obsługiwane: B, C, gG)."

    return ia, None


def generuj_protokol():
    """Generuje protokół z pomiaru impedancji pętli zwarcia."""

    print("--- Generator protokołów pomiaru impedancji pętli zwarcia ---")

    # Dane do wprowadzenia przez użytkownika
    lokalizacja = input("Podaj lokalizację pomiaru (np. Gniazdo 1, Oświetlenie Kuchnia): ")
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

    # Automatyczne obliczenia
    napiecie_znamionowe = 230  # V

    if prad_zadzialania_Ia == 0:
        print("Błąd: Prąd zadziałania Ia nie może być zerowy.")
        return

    impedancja_dopuszczalna = napiecie_znamionowe / prad_zadzialania_Ia
    prad_zwarcia_Isc = napiecie_znamionowe / impedancja_zmierzona

    # Ocena pomiaru
    ocena = "TAK" if prad_zwarcia_Isc >= prad_zadzialania_Ia else "NIE"

    # Przygotowanie danych do zapisu w pliku
    tresc_protokolu = f"""
==================================================
        PROTOKÓŁ Z POMIARU IMPEDANCJI PĘTLI ZWARCIA
==================================================
Data wykonania: {datetime.date.today()}
Lokalizacja pomiaru: {lokalizacja}

--- Dane zabezpieczenia ---
Typ zabezpieczenia: {typ_zabezpieczenia.upper()}
Prąd znamionowy In: {prad_znamionowy} A
Prąd zadziałania Ia: {prad_zadzialania_Ia} A

--- Wyniki pomiaru ---
Impedancja zmierzona Zz: {impedancja_zmierzona:.2f} Ω
Impedancja dopuszczalna Zd: {impedancja_dopuszczalna:.2f} Ω
Obliczeniowy prąd zwarcia Isc: {prad_zwarcia_Isc:.2f} A
(wartość dopuszczalna >= {prad_zadzialania_Ia} A)

--- Ocena ---
Pomiar pomyślny? {ocena}

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