import math


def oblicz_parametry_RC_trojfazowy(pojemnosc_uF, rezystancja_ohm, napiecie_miedzyfazowe_V, czestotliwosc_Hz=50):
    import math
    """
    Funkcja obliczajaca parametry dla obwodu 3-fazowego R-C w ukladzie trojkata.

    Parametry:
    - pojemnosc_uF (float): Pojemnosc kondensatora w mikrofaradach (uF).
    - rezystancja_ohm (float): Opor rezystora w omach (Ohm).
    - napiecie_miedzyfazowe_V (float): Napięcie miedzyfazowe w woltach (V, np. 400).
    - czestotliwosc_Hz (float): Czestotliwosc sieci w hercach (Hz), domyslnie 50 Hz.

    Zwraca:
    - tuple: (prad_fazowy_A, prad_przewodowy_A, napiecie_na_rezystorze_V, napiecie_na_kondensatorze_V, moc_calkowita_W)
    """

    # W ukladzie trojkata, napiecie na elemencie (fazowe) jest rowne napieciu miedzyfazowemu
    napiecie_fazowe_V = napiecie_miedzyfazowe_V

    # Konwersja pojemnosci z mikrofaradow (uF) na farady (F)
    pojemnosc_F = pojemnosc_uF / 1_000_000.0

    # 1. Obliczenie reaktancji pojemnosciowej (XC) dla jednej fazy
    xc = 1 / (2 * math.pi * czestotliwosc_Hz * pojemnosc_F)

    # 2. Obliczenie impedancji (Z) dla jednej fazy
    impedancja_Z = math.sqrt(rezystancja_ohm ** 2 + xc ** 2)

    # 3. Obliczenie pradu fazowego (pradu plynacego przez jeden kondensator/rezystor)
    prad_fazowy_A = napiecie_fazowe_V / impedancja_Z

    # 4. Obliczenie pradu przewodowego (pradu plynacego w przewodach zasilajacych)
    prad_przewodowy_A = prad_fazowy_A * math.sqrt(3)

    # 5. Obliczenie napiecia odkladajacego sie na rezystorze w danej fazie (jest to napiecie fazowe)
    napiecie_na_rezystorze_V = prad_fazowy_A * rezystancja_ohm

    # 6. Obliczenie napiecia odkladajacego sie na kondensatorze w danej fazie
    napiecie_na_kondensatorze_V = prad_fazowy_A * xc

    # 7. Obliczenie mocy czynnej wydzielanej na jednym rezystorze
    moc_na_jednym_rezystorze_W = prad_fazowy_A ** 2 * rezystancja_ohm

    # 8. Obliczenie calkowitej mocy czynnej w ukladzie
    moc_calkowita_W = 3 * moc_na_jednym_rezystorze_W

    return prad_fazowy_A, prad_przewodowy_A, napiecie_na_rezystorze_V, napiecie_na_kondensatorze_V, moc_calkowita_W


# Glowna czesc programu
if __name__ == "__main__":
    try:
        # Pytamy uzytkownika o wartosci
        pojemnosc = float(input("Podaj pojemnosc kondensatora w mikrofaradach (uF): "))
        rezystor = 33  # Stala wartosc oporu rezystora
        napiecie_miedzyfazowe = float(input("Podaj napiecie miedzyfazowe (V, np. 400): "))

        # Wywolanie funkcji i przechwycenie wynikow
        prad_fazowy, prad_przewodowy, napiecie_rezystor, napiecie_kondensator, moc_calkowita = oblicz_parametry_RC_trojfazowy(
            pojemnosc, rezystor, napiecie_miedzyfazowe)

        # Wyswietlenie wynikow
        print(f"\n--- Dane obwodu trojfazowego w ukladzie trojkata ---")
        print(f"Rezystancja w kazdej fazie: {rezystor} Ω")
        print(f"Pojemnosc w kazdej fazie: {pojemnosc} uF")
        print(f"Napiecie miedzyfazowe: {napiecie_miedzyfazowe} V")
        print(f"Napiecie fazowe (na elemencie) jest rowne napieciu miedzyfazowemu: {napiecie_miedzyfazowe} V")
        print("-" * 30)

        print(f"Obliczony prad fazowy (przez kondensator/rezystor): {prad_fazowy:.4f} A")
        print(f"Obliczony prad przewodowy (prad w kablach zasilajacych): {prad_przewodowy:.4f} A")
        print(f"Napiecie na rezystorze w danej fazie (UR): {napiecie_rezystor:.4f} V")
        print(f"Napiecie na kondensatorze w danej fazie (UC): {napiecie_kondensator:.4f} V")
        print(f"Calkowita moc wydzielana w ukladzie (na 3 rezystorach): {moc_calkowita:.4f} W")
        print("-" * 30)

    except ValueError:
        print("Błąd: Podana wartość nie jest liczbą. Uruchom program ponownie i podaj poprawne dane.")
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad: {e}")