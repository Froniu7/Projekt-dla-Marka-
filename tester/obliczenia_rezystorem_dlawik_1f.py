import math


def oblicz_parametry_RL(indukcyjnosc_mH, napiecie_V, rezystancja_ohm, czestotliwosc_Hz=50):
    import math
    """
    Funkcja obliczajaca prad, napiecia i moc w obwodzie R-L.

    Parametry:
    - indukcyjnosc_mH (float): Indukcyjnosc dlawika w milihenrach (mH).
    - napiecie_V (float): Skuteczne napiecie w sieci w woltach (V).
    - rezystancja_ohm (float): Opor rezystora w omach (Ohm).
    - czestotliwosc_Hz (float): Czestotliwosc sieci w hercach (Hz), domyslnie 50 Hz.

    Zwraca:
    - tuple: (prad_skuteczny_A, napiecie_na_rezystorze_V, napiecie_na_dlawiku_V, moc_na_rezystorze_W)
    """

    # Konwersja indukcyjnosci z milihenrow (mH) na henry (H)
    indukcyjnosc_H = indukcyjnosc_mH / 1000.0

    # 1. Obliczenie reaktancji indukcyjnej (XL)
    xl = 2 * math.pi * czestotliwosc_Hz * indukcyjnosc_H

    # 2. Obliczenie impedancji (Z)
    impedancja_Z = math.sqrt(rezystancja_ohm ** 2 + xl ** 2)

    # 3. Obliczenie pradu skutecznego (Isk)
    prad_skuteczny_A = napiecie_V / impedancja_Z

    # 4. Obliczenie napiecia odkladajacego sie na rezystorze (UR)
    napiecie_na_rezystorze_V = prad_skuteczny_A * rezystancja_ohm

    # 5. Obliczenie napiecia odkladajacego sie na dlawiku (UL)
    napiecie_na_dlawiku_V = prad_skuteczny_A * xl

    # 6. Obliczenie mocy czynnej wydzielanej na rezystorze (P)
    moc_na_rezystorze_W = prad_skuteczny_A ** 2 * rezystancja_ohm

    return prad_skuteczny_A, napiecie_na_rezystorze_V, napiecie_na_dlawiku_V, moc_na_rezystorze_W


# Glowna czesc programu
if __name__ == "__main__":
    try:
        # Pytamy uzytkownika o wartosci
        indukcyjnosc = float(input("Podaj indukcyjnosc dlawika w milihenrach (mH): "))
        napiecie_sieci = float(input("Podaj napiecie sieciowe w woltach (V, np. 230): "))
        rezystor = 7.33  # Stala wartosc oporu rezystora

        # Wywolanie funkcji i przechwycenie wynikow
        prad, napiecie_rezystor, napiecie_dlawik, moc_rezystor = oblicz_parametry_RL(indukcyjnosc, napiecie_sieci,
                                                                                     rezystor)

        # Sprawdzenie prawa Ohma dla wartosci skutecznych napięc
        suma_kwadratow = math.sqrt(napiecie_rezystor ** 2 + napiecie_dlawik ** 2)

        # Wyswietlenie wynikow
        print(f"\n--- Dane obwodu ---")
        print(f"Rezystancja rezystora: {rezystor} Ω")
        print(f"Indukcyjnosc dlawika: {indukcyjnosc} mH")
        print(f"Napiecie zrodla: {napiecie_sieci} V")
        print(f"Czestotliwosc sieci: 50 Hz")
        print("-" * 30)

        print(f"Obliczona wartosc skuteczna pradu: {prad:.4f} A")
        print(f"Napiecie na rezystorze (UR): {napiecie_rezystor:.4f} V")
        print(f"Napiecie na dlawiku (UL): {napiecie_dlawik:.4f} V")
        print(f"Moc wydzielana na rezystorze (P): {moc_rezystor:.4f} W")
        print("-" * 30)
        print(f"Sprawdzenie: sqrt(UR^2 + UL^2) = {suma_kwadratow:.4f} V")

    except ValueError:
        print("Błąd: Podana wartość nie jest liczbą. Uruchom program ponownie i podaj poprawne dane.")
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad: {e}")