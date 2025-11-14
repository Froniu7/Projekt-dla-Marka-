import argparse
import json
from datetime import datetime

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Program do doboru przekladnikow pradowych i przewodu kablowego sterowniczego"
    )


    parser.add_argument("-mz", "--moc_zamowiona", type=float, default=None, help = "parametr wystepujacy na fakturze za energie elektryczna. Nalezy podac jeden z argumentow moc_zamowiona badz moc_max")
    parser.add_argument("-mm", "--moc_max", type=float, default=None, help = "moc szczytowa, parametr wystepujacy na niektorych fakturach")
    parser.add_argument("-pup", "--przekladnia_uzwojenie_pierwotne", type=int, default=None)
    parser.add_argument("-puw", "--przekladnia_uzwojenie_wtorne", type=int, default=None)
    parser.add_argument("-va", "--VA", type=float, default=None)
    parser.add_argument("-p", "--przewod", type=float, default=None)
    parser.add_argument("-dp", "--dlugosc_przewodu", type=float, default=None)
    parser.add_argument("-a", "--asymetria", type=float, default=None)
    parser.add_argument("-s", "--strona", type=int, default=None)

    # Parsowanie argumentów
    args = parser.parse_args()


    # --- Walidacja: przynajmniej jeden z dwóch argumentów musi być podany ---
    if args.moc_zamowiona is None and args.moc_max is None:
        parser.error("Musisz podać przynajmniej jeden z argumentów: --moc_zamowiona lub --moc_wystepujaca")
    else:
        # Użycie argumentów
        print("➡ Otrzymane argumenty:")
        print(f"  moc_zamowiona:     {args.moc_zamowiona}")
        print(f"  moc_max:     {args.moc_max}")
        print(f"  przekladnia_uzwojenie_pierwotne:   {args.przekladnia_uzwojenie_pierwotne}")
        print(f"  przekladnia_uzwojenie_wtorne:    {args.przekladnia_uzwojenie_wtorne}")
        print(f"  przewod:  {args.VA}")
        print(f"  przewod:  {args.przewod}")
        print(f"  dlugosc_przewodu:  {args.dlugosc_przewodu}")
        print(f"  asymetria:  {args.asymetria}")
        print(f"  strona:  {args.strona}")

    # Zwracamy wszystkie argumenty jako krotkę
    return (
        args.moc_zamowiona,
        args.moc_max,
        args.przekladnia_uzwojenie_pierwotne,
        args.przekladnia_uzwojenie_wtorne,
        args.VA,
        args.przewod,
        args.dlugosc_przewodu,
        args.asymetria,
        args.strona
    )


def obliczenie_mocy_wydzielonej(przekladnia, dlugosc_przewodu, przekroj_przewodu_mm2, prad_uzwojenie_pierwotne):
    """
    Oblicza straty mocy na przewodzie miedzianym zasilającym uzwojenie wtórne
    przekładnika prądowego.

    Parametry:
        przekladnia (float): przekładnia przekładnika prądowego [-]
        VA (float): moc pozorna obciążenia [VA] (opcjonalnie, w tym wzorze nie używana)
        dlugosc_przewodu (float): długość przewodu [m] (jedna żyła)
        przekroj_przewodu_mm2 (float): przekrój przewodu [mm²]
        prad_uzwojenie_pierwotne (float): prąd na uzwojeniu pierwotnym [A]

    Zwraca:
        float: straty mocy na przewodzie [W]
    """

    print("\n— DOBÓR PRZEKROJU PRZEWODU STERUJĄCEGO —\n")

    # Konwersja jednostek: mm² -> m²
    A = przekroj_przewodu_mm2 * 1e-6

    # Uwzględnienie pełnej pętli przewodu (tam i z powrotem)
    L = 2 * dlugosc_przewodu

    print("Wzór na straty mocy w przewodzie miedzianym:")
    print("  P_strat = (I^2 * ρ * L) / A")
    print("  gdzie:")
    print("    P_strat  — straty mocy na przewodzie [W]")
    print("    I        — prąd w uzwojeniu wtórnym [A] (I_wtórne = I_pierwotne / k)")
    print("    ρ        — oporność właściwa miedzi w 20°C = 1.724 × 10⁻⁸ Ω·m")
    print(f"    L        — długość przewodu = {L} m (pełna pętla)")
    print(f"    A        — przekrój przewodu = {A:.6e} m²\n")

    # Obliczenie prądu wtórnego
    print("Obliczamy prąd na uzwojeniu wtórnym:")
    I = prad_uzwojenie_pierwotne / przekladnia
    print(f"  I_wtórne = {prad_uzwojenie_pierwotne} / {przekladnia} = {I:.3f} A\n")

    # Obliczenie strat mocy
    rho = 1.724e-8  # Ω·m
    Pstrat = (I ** 2 * rho * L) / A
    print("Obliczenie strat mocy w przewodzie:")
    print(f"  P_strat = ({I:.3f}² * {rho} * {L}) / {A:.6e}")
    print(f"  P_strat = {Pstrat:.6f} W\n")

    return Pstrat

import json

def zapisz_pole_json(sciezka, nazwa_pola, wartosc):
    """
    Aktualizuje lub dodaje wybrane pole w pliku JSON.
    Nie zmienia innych pól w pliku.

    Parametry:
        sciezka (str): ścieżka do pliku JSON
        nazwa_pola (str): nazwa pola, które ma być zapisane/zmienione
        wartosc: wartość do zapisania
    """

    # Wczytanie istniejącego pliku JSON lub utworzenie nowego słownika
    try:
        with open(sciezka, 'r', encoding='utf-8') as f:
            dane = json.load(f)
    except FileNotFoundError:
        dane = {}

    # Aktualizacja wskazanego pola
    dane[nazwa_pola] = wartosc

    # Zapis do pliku
    with open(sciezka, 'w', encoding='utf-8') as f:
        json.dump(dane, f, ensure_ascii=False, indent=4)

    print(f"Pole '{nazwa_pola}' zapisane w pliku '{sciezka}' z wartością: {wartosc}")

def prad(moc: float, asymetria: float = 0) -> float:
    """
    Oblicza prąd fazowy dla obciążenia trójfazowego przy napięciu fazowym 230 V.
    Parametry:
        moc (float): moc całkowita układu trójfazowego [W]
        asymetria (float): procentowa różnica prądu między fazami [%] (opcjonalnie)
    Zwraca:
        float: prąd w jednej fazie [A]
    """

    print("— OBLICZENIE PRĄDU W UKŁADZIE TRÓJFAZOWYM —")
    print("Założenia:")
    print(f"  Moc całkowita P = {moc} W")
    print("  Napięcie międzyfazowe: 400 V")
    print("  Napięcie fazowe (L–N): 230 V")
    print("  Liczba faz: 3\n")

    print("Wzór:")
    print("  I_f = (P / 3) / U_f")
    print("  gdzie:")
    print("      I_f — prąd w jednej fazie [A]")
    print("      P   — moc całkowita układu [W]")
    print("      U_f — napięcie fazowe (L–N) [V]\n")

    prad = (moc / 3) / 230
    print(f"Podstawienie: I_f = ({moc} / 3) / 230")
    print(f"Wynik bez uwzględnienia asymetrii: I_f = {prad:.3f} A\n")

    if asymetria != 0:
        print(f"Uwzględniamy asymetrię prądu fazowego: {asymetria:.1f} %")
        wspolczynnik = 1 + (asymetria / 100)
        print(f"Prąd po korekcie: I_f' = I_f × (1 + {asymetria/100:.3f})")
        prad *= wspolczynnik
        print(f"Wynik po korekcie: I_f' = {prad:.3f} A\n")

    print("— KONIEC OBLICZEŃ —\n")
    return prad


def wyliczenie_przekladni(uzwojenie_pierwotne, uzwojenie_wtorne):
    print("Obliczamy przekładnię przekładnika prądowego")
    print("Wzór ogólny:")
    print("k = N₁ / N₂")
    print("gdzie:")
    print("k  – przekładnia przekładnika prądowego [-]")
    print("N₁ – liczba zwojów (lub prąd) uzwojenia pierwotnego [A]")
    print("N₂ – liczba zwojów (lub prąd) uzwojenia wtórnego [A]")

    przekladnia = uzwojenie_pierwotne / uzwojenie_wtorne

    print(f"\nPodstawienie do wzoru:")
    print(f"k = {uzwojenie_pierwotne} / {uzwojenie_wtorne}")
    print(f"k = {przekladnia:.2f}")

    return przekladnia

def sprawdzenie_warunku(moc_wyliczona, VA):
    """
    Sprawdza, czy moc strat w przewodzie jest mniejsza lub równa
    mocy znamionowej przekładnika prądowego.

    Parametry:
        moc_wyliczona (float): moc strat w przewodzie [W]
        VA (float): moc znamionowa przekładnika prądowego [VA]

    Zwraca:
        None
    """

    print("\n— SPRAWDZENIE WARUNKU DOBORU PRZEKŁADNIKA PRĄDOWEGO —\n")
    print("Warunek do spełnienia:")
    print("  P_przekładnika ≥ P_strat")
    print("gdzie:")
    print("  P_przekładnika — moc znamionowa przekładnika prądowego [VA]")
    print("  P_strat        — moc strat w przewodzie zasilającym uzwojenie wtórne [W]\n")

    print(f"Podstawienie wartości:")
    print(f"  P_przekładnika = {VA} VA")
    print(f"  P_strat        = {moc_wyliczona:.6f} W\n")

    if moc_wyliczona <= VA:
        print("Analiza porównawcza: P_przekładnika ≥ P_strat")
        print(f"  {VA} ≥ {moc_wyliczona:.6f} ✅")
        print("Wniosek: Warunek doboru przekładnika prądowego został spełniony.\n")
        return True
    else:
        print("Analiza porównawcza: P_przekładnika ≥ P_strat")
        print(f"  {VA} < {moc_wyliczona:.6f} ❌")
        print("Wniosek: Warunek doboru przekładnika prądowego NIE został spełniony.\n")
        return False

def aktualna_data():
    # Pobranie aktualnej daty i czasu
    teraz = datetime.now()
    aktualna_data = teraz.strftime("%Y-%m-%d %H:%M:%S")
    return aktualna_data