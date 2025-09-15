import math


def oblicz_parametry_RL_trojfazowy_gwiazda(indukcyjnosc_mH, rezystancja_ohm, napiecie_miedzyfazowe_V,
                                           czestotliwosc_Hz=50):
    """
    Funkcja obliczajaca parametry dla obwodu 3-fazowego R-L w ukladzie gwiazdy.

    Parametry:
    - indukcyjnosc_mH (float): Indukcyjnosc dlawika w milihenrach (mH).
    - rezystancja_ohm (float): Opor rezystora w omach (Ohm).
    - napiecie_miedzyfazowe_V (float): Napięcie miedzyfazowe w woltach (V, np. 400).
    - czestotliwosc_Hz (float): Czestotliwosc sieci w hercach (Hz), domyslnie 50 Hz.

    Zwraca:
    - tuple: (prad_przewodowy_A, napiecie_fazowe_V, napiecie_na_rezystorze_V, napiecie_na_dlawiku_V, moc_calkowita_W)
    """

    # W ukladzie gwiazdy, napiecie na elemencie (fazowe) jest napieciem miedzyfazowym podzielonym przez sqrt(3)
    napiecie_fazowe_V = napiecie_miedzyfazowe_V / math.sqrt(3)

    # Konwersja indukcyjnosc z milihenrow (mH) na henry (H)
    indukcyjnosc_H = indukcyjnosc_mH / 1000.0

    # 1. Obliczenie reaktancji indukcyjnej (XL) dla jednej fazy
    xl = 2 * math.pi * czestotliwosc_Hz * indukcyjnosc_H

    # 2. Obliczenie impedancji (Z) dla jednej fazy
    impedancja_Z = math.sqrt(rezystancja_ohm ** 2 + xl ** 2)

    # 3. Obliczenie pradu fazowego (pradu plynacego przez jeden dlawik/rezystor), ktory jest rowny pradowi przewodowemu
    prad_fazowy_A = napiecie_fazowe_V / impedancja_Z
    prad_przewodowy_A = prad_fazowy_A

    # 4. Obliczenie napiecia odkladajacego sie na rezystorze w danej fazie
    napiecie_na_rezystorze_V = prad_fazowy_A * rezystancja_ohm

    # 5. Obliczenie napiecia odkladajacego sie na dlawiku w danej fazie
    napiecie_na_dlawiku_V = prad_fazowy_A * xl

    # 6. Obliczenie mocy czynnej wydzielanej na jednym rezystorze
    moc_na_jednym_rezystorze_W = prad_fazowy_A ** 2 * rezystancja_ohm

    # 7. Obliczenie calkowitej mocy czynnej w ukladzie
    moc_calkowita_W = 3 * moc_na_jednym_rezystorze_W

    return prad_przewodowy_A, napiecie_fazowe_V, napiecie_na_rezystorze_V, napiecie_na_dlawiku_V, moc_calkowita_W


# Glowna czesc programu
if __name__ == "__main__":
    try:
        # Pytamy uzytkownika o wartosci
        indukcyjnosc = float(input("Podaj indukcyjnosc dlawika w milihenrach (mH): "))
        rezystor = 7.33  # Stala wartosc oporu rezystora
        napiecie_miedzyfazowe = float(input("Podaj napiecie miedzyfazowe (V, np. 400): "))

        # Wywolanie funkcji i przechwycenie wynikow
        prad_przewodowy, napiecie_fazowe, napiecie_rezystor, napiecie_dlawik, moc_calkowita = oblicz_parametry_RL_trojfazowy_gwiazda(
            indukcyjnosc, rezystor, napiecie_miedzyfazowe)

        # Wyswietlenie wynikow
        print(f"\n--- Dane obwodu trojfazowego w ukladzie gwiazdy ---")
        print(f"Rezystancja w kazdej fazie: {rezystor} Ω")
        print(f"Indukcyjnosc w kazdej fazie: {indukcyjnosc} mH")
        print(f"Napiecie miedzyfazowe: {napiecie_miedzyfazowe} V")
        print(f"Napiecie fazowe (na elemencie) = Napiecie miedzyfazowe / sqrt(3): {napiecie_fazowe:.2f} V")
        print("-" * 30)

        print(f"Obliczony prad przewodowy: {prad_przewodowy:.4f} A")
        print(f"Napiecie na rezystorze w danej fazie (UR): {napiecie_rezystor:.4f} V")
        print(f"Napiecie na dlawiku w danej fazie (UL): {napiecie_dlawik:.4f} V")
        print(f"Calkowita moc wydzielana w ukladzie (na 3 rezystorach): {moc_calkowita:.4f} W")
        print("-" * 30)

        # Dodatkowe sprawdzenie wektorowe
        sprawdzenie_napięcia_fazowego = math.sqrt(napiecie_rezystor ** 2 + napiecie_dlawik ** 2)
        print(
            f"Sprawdzenie: sqrt(UR^2 + UL^2) = {sprawdzenie_napięcia_fazowego:.2f} V (powinno byc rowne napieciu fazowemu)")

    except ValueError:
        print("Błąd: Podana wartość nie jest liczbą. Uruchom program ponownie i podaj poprawne dane.")
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad: {e}")