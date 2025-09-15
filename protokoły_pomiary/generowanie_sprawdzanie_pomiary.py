import datetime


def generuj_protokol():
    """Generuje protokół z pomiaru impedancji pętli zwarcia."""

    print("--- Generator protokołów pomiaru impedancji pętli zwarcia ---")

    # Dane do wprowadzenia przez użytkownika
    lokalizacja = input("Podaj lokalizację pomiaru (np. Gniazdo 1, Oświetlenie Kuchnia): ")
    typ_zabezpieczenia = input("Podaj typ zabezpieczenia (np. C16, B10): ").upper().strip()
    try:
        impedancja_zmierzona = float(input("Podaj zmierzoną impedancję Zz [Ω]: "))
    except ValueError:
        print("Błąd: Wprowadzona wartość impedancji musi być liczbą. Spróbuj ponownie.")
        return

    # Ustalanie danych na podstawie typu zabezpieczenia
    try:
        charakterystyka = typ_zabezpieczenia[0]
        prad_znamionowy = int(typ_zabezpieczenia[1:])
    except (IndexError, ValueError):
        print("Błąd: Niepoprawny format typu zabezpieczenia. Wpisz np. C16 lub B10.")
        return

    # Automatyczne obliczenia
    napiecie_znamionowe = 230  # V

    if charakterystyka == 'B':
        wspolczynnik = 5
    elif charakterystyka == 'C':
        wspolczynnik = 10
    else:
        print("Błąd: Nieobsługiwana charakterystyka zabezpieczenia (obsługiwane: B, C).")
        return

    prad_zadzialania_Ia = wspolczynnik * prad_znamionowy
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
Typ zabezpieczenia: {typ_zabezpieczenia}
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