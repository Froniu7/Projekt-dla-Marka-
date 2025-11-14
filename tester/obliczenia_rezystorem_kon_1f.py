import math


def oblicz_parametry_RC(pojemnosc_uF, napiecie_V, rezystancja_ohm, czestotliwosc_Hz=50):
    import math
    """
    Funkcja obliczajaca prad, napiecia i moc w obwodzie R-C.

    Parametry:
    - pojemnosc_uF (float): Pojemnosc kondensatora w mikrofaradach (uF).
    - napiecie_V (float): Skuteczne napiecie w sieci w woltach (V).
    - rezystancja_ohm (float): Opor rezystora w omach (Ohm).
    - czestotliwosc_Hz (float): Czestotliwosc sieci w hercach (Hz), domyslnie 50 Hz.

    Zwraca:
    - tuple: (prad_skuteczny_A, napiecie_na_rezystorze_V, napiecie_na_kondensatorze_V, moc_na_rezystorze_W)
    """

    # Konwersja pojemnosci z mikrofaradow (uF) na farady (F)
    pojemnosc_F = pojemnosc_uF / 1_000_000.0

    # 1. Obliczenie reaktancji pojemnosciowej (XC)
    xc = 1 / (2 * math.pi * czestotliwosc_Hz * pojemnosc_F)

    # 2. Obliczenie impedancji (Z)
    impedancja_Z = math.sqrt(rezystancja_ohm ** 2 + xc ** 2)

    # 3. Obliczenie pradu skutecznego (Isk)
    prad_skuteczny_A = napiecie_V / impedancja_Z

    # 4. Obliczenie napiecia odkladajacego sie na rezystorze (UR)
    napiecie_na_rezystorze_V = prad_skuteczny_A * rezystancja_ohm

    # 5. Obliczenie napiecia odkladajacego sie na kondensatorze (UC)
    napiecie_na_kondensatorze_V = prad_skuteczny_A * xc

    # 6. Obliczenie mocy czynnej wydzielanej na rezystorze (P)
    moc_na_rezystorze_W = prad_skuteczny_A ** 2 * rezystancja_ohm

    return prad_skuteczny_A, napiecie_na_rezystorze_V, napiecie_na_kondensatorze_V, moc_na_rezystorze_W


# Glowna czesc programu
if __name__ == "__main__":
    try:
        # Pytamy uzytkownika o wartosci
        pojemnosc = float(input("Podaj pojemnosc kondensatora w mikrofaradach (uF): "))
        napiecie_sieci = float(input("Podaj napiecie sieciowe w woltach (V, np. 230): "))
        rezystor = 7.33  # Stala wartosc oporu rezystora

        # Wywolanie funkcji i przechwycenie wynikow
        prad, napiecie_rezystor, napiecie_kondensator, moc_rezystor = oblicz_parametry_RC(pojemnosc, napiecie_sieci,
                                                                                          rezystor)

        # Sprawdzenie prawa Ohma dla wartosci skutecznych napięc
        suma_kwadratow = math.sqrt(napiecie_rezystor ** 2 + napiecie_kondensator ** 2)

        # Wyswietlenie wynikow
        print(f"\n--- Dane obwodu ---")
        print(f"Rezystancja rezystora: {rezystor} Ω")
        print(f"Pojemnosc kondensatora: {pojemnosc} uF")
        print(f"Napiecie zrodla: {napiecie_sieci} V")
        print(f"Czestotliwosc sieci: 50 Hz")
        print("-" * 30)

        print(f"Obliczona wartosc skuteczna pradu: {prad:.4f} A")
        print(f"Napiecie na rezystorze (UR): {napiecie_rezystor:.4f} V")
        print(f"Napiecie na kondensatorze (UC): {napiecie_kondensator:.4f} V")
        print(f"Moc wydzielana na rezystorze (P): {moc_rezystor:.4f} W")
        print("-" * 30)
        print(f"Sprawdzenie: sqrt(UR^2 + UC^2) = {suma_kwadratow:.4f} V")

    except ValueError:
        print("Błąd: Podana wartość nie jest liczbą. Uruchom program ponownie i podaj poprawne dane.")
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad: {e}")
