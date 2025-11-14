# testowanie.py
import sys
import csv, time, serial
from funkcja_do_otczytywania import extract_reactive_value
from obliczenia_rezystorem_kon_1f import oblicz_parametry_RC
from obliczenia_rezystorem_kon_3f import oblicz_parametry_RC_trojfazowy
from obliczenia_rezystorem_dlawik_1f import oblicz_parametry_RL
from obliczenia_rezystorem_dławik_3f import oblicz_parametry_RL_trojfazowy_gwiazda
from funkcje_testowanie.COM import test_mikrokontroler_bez_zamkniecia, wyslij_komende, check_power_within_limits, get_first_float_from_string, get_second_float_from_string, zapisz_wynik_testu_dziala, zapisz_wynik_testu_niedziala
from obliczenie_pradu_dla_kon1f import calculate_capacitor_power_delta, calculate_single_phase_power


# deklaracja zmiennych globalnych
global_u1 = global_u2 = global_u3 = 0.0
global_u12 = global_u23 = global_u31 = global_u_avg = 0.0
global_i1 = global_i2 = global_i3 = 0.0
global_q1 = global_q2 = global_q3 = global_qn = 0.0
selected_list = ""
last_selected_item = ""
COM = None
widelki_dolne = 0
widelki_gorne = 0

def read_csv_to_globals(csv_file_path="dane_globalne.csv"):
    """Odczytuje plik CSV i zapisuje wartości do zmiennych globalnych"""
    global global_u1, global_u2, global_u3
    global global_u12, global_u23, global_u31, global_u_avg
    global global_i1, global_i2, global_i3
    global global_q1, global_q2, global_q3, global_qn

    try:
        with open(csv_file_path, mode="r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 2:
                    continue
                name, value = row
                try:
                    value = float(value)
                except ValueError:
                    continue  # ignorujemy niepoprawne wartości

                if name == "U1": global_u1 = value
                elif name == "U2": global_u2 = value
                elif name == "U3": global_u3 = value
                elif name == "U12": global_u12 = value
                elif name == "U23": global_u23 = value
                elif name == "U31": global_u31 = value
                elif name == "U_avg": global_u_avg = value
                elif name == "I1": global_i1 = value
                elif name == "I2": global_i2 = value
                elif name == "I3": global_i3 = value
                elif name == "Q1": global_q1 = value
                elif name == "Q2": global_q2 = value
                elif name == "Q3": global_q3 = value
                elif name == "Qn": global_qn = value

        print("Dane CSV zapisane do zmiennych globalnych:")
        print(f"U1={global_u1}, U2={global_u2}, U3={global_u3}")
        print(f"U12={global_u12}, U23={global_u23}, U31={global_u31}, U_avg={global_u_avg}")
        print(f"I1={global_i1}, I2={global_i2}, I3={global_i3}")
        print(f"Q1={global_q1}, Q2={global_q2}, Q3={global_q3}, Qn={global_qn}")

    except FileNotFoundError:
        print(f"Nie znaleziono pliku {csv_file_path}!")
    except Exception as e:
        print(f"Błąd podczas odczytu pliku CSV: {e}")

def main():
    global selected_list, last_selected_item, COM, widelki_dolne, widelki_gorne
    if len(sys.argv) >= 4:
        COM = sys.argv[1]
        selected_list = sys.argv[2]
        last_selected_item = sys.argv[3]
        widelki_dolne = sys.argv[4]
        widelki_gorne = sys.argv[5]

        print(f"Uruchomiono testowanie.py z parametrami:")
        print(f"  COM: {COM}")
        print(f"  selected_list: {selected_list}")
        print(f"  last_selected_item: {last_selected_item}")
    else:
        print("Nie podano wszystkich wymaganych parametrów!")

    # odczyt CSV do zmiennych globalnych
    read_csv_to_globals()
    time.sleep(1)



def prad_z_marginesem(prad_A, procent=20):
    """
    Oblicza zakres prądu ± podany procent.

    Parametry:
    - prad_A (float): wartość prądu w amperach
    - procent (float): procent odchylenia (domyślnie 20)

    Zwraca:
    - tuple: (prad_min, prad_max)
    """
    delta = prad_A * procent / 100.0
    return prad_A - delta, prad_A + delta

if __name__ == "__main__":
    main()
    print(f"zmienna zawiera: {last_selected_item}")
    dane = extract_reactive_value(last_selected_item)
    dane_typ = dane['type']
    dane_wartosc = float(dane['value'])
    dane_jednostka = dane['unit']

    mikrokontroler, informacja_zwrotna = test_mikrokontroler_bez_zamkniecia(COM)

    if informacja_zwrotna == "Nieznana komenda":
        print(f"poprawny test komunikacji na porcie: {COM}")
        print("port COM zostaje otwarty")
        print(f"selected list: {selected_list}")


        if selected_list == "1":
            print("wybrano kondensator 1 fazowy")
            print("Liczymy wartosc pradu z rezystorem\n"
                  "dla kondensatora 1 fazowego")
            print("Uruchamiamy pomiar z rezystorem")

            # 4
            informacja_zwrotna = wyslij_komende(mikrokontroler, "p1")
            wartos_zwrotna_float = float(informacja_zwrotna)
            napiecie = float(global_u1)
            prad, napiecie_rezystor, napiecie_kondensator, moc_rezystor = oblicz_parametry_RC(dane_wartosc,
                                                                                              napiecie, 33,
                                                                                              50)
            I_min, I_max = prad_z_marginesem(prad)

            if wartos_zwrotna_float >= I_min and wartos_zwrotna_float <= I_max:
                print("prad miesci sie w zakresie")

                informacja_zwrotna = wyslij_komende(mikrokontroler, "1")

                if informacja_zwrotna == "S":
                    print("zalaczamy kondensator")
                    time.sleep(3)
                    read_csv_to_globals()

                    dane = extract_reactive_value(last_selected_item)
                    dane_typ = dane['type']  # typ np C lub L
                    dane_wartosc = float(dane['value'])  # wartosc w mH lub uF
                    dane_jednostka = dane['unit']  # jednostka uF lub mH
                    napiecie = float(global_u1)  # napiecie pobrane z pliku CSV
                    print(f"napiecie: {global_u1}, prąd: {global_i1}, moc bierna: {global_q1}")
                    widelki_dolne_float = float(widelki_dolne) * 0.01
                    widelki_gorne_float = float(widelki_gorne) * 0.01
                    print(f"sprawdzamy dla widełek: \n"
                          f"górne: {widelki_gorne} %, float: {widelki_gorne_float}\n"
                          f"dolne: {widelki_dolne} %, float: {widelki_dolne_float}")
                    napiecie = float(global_u1)
                    moc_pomiar = calculate_single_phase_power(dane_wartosc, napiecie, 50)

                    moc_float = float(moc_pomiar)
                    print(f"wyliczona moc: {moc_float}")
                    dane_float_moc_kvar = get_first_float_from_string(last_selected_item)
                    print(f"moc podana przez producenta: {dane_float_moc_kvar}")
                    wynik, dane = check_power_within_limits(dane_float_moc_kvar, moc_float, widelki_gorne_float,
                                                            widelki_dolne_float)

                    if wynik == True:
                        print(f"wynik testu = {wynik} ")
                        print(f"wynik testu = {dane} D")
                        zapisz_wynik_testu_dziala("kondensatory1fazowe_dobre.csv", "1 fazwoy kondensator", moc_pomiar,
                                                  last_selected_item, "Działa")
                    if wynik == False:
                        print(f"wynik testu = {wynik} ")
                        print(f"wynik testu = {dane} Z")
                        zapisz_wynik_testu_niedziala("kondensatory1fazowe_zle.csv", "1 fazwoy kondensator", moc_pomiar,
                                                     last_selected_item, "NIE DZIAŁA !!!")



            else:
                print("Wartosc pradu z rezystorem nie miesci sie w widełkach")
                #print(f"Prad zmiwerzony : {global_i1}")




                """
                time.sleep(2)
                read_csv_to_globals()
                informacja_zwrotna = wyslij_komende(mikrokontroler, "on1fazowy")
                time.sleep(0.1)
                informacja_zwrotnaA = wyslij_komende(mikrokontroler, "stop1rez")
                time.sleep(2)
                informacja_zwrotnaB = wyslij_komende(mikrokontroler, "off1fazowy")
                #5
                print(informacja_zwrotna)
                if informacja_zwrotnaA == "wylaczono 1 fazowy z rezystorem" and informacja_zwrotnaB == "pin1 ustawiony na HIGH":
                    print("działa")
                    #6
                    dane = extract_reactive_value(last_selected_item)
                    dane_typ = dane['type'] #typ np C lub L
                    dane_wartosc = float(dane['value']) # wartosc w mH lub uF
                    dane_jednostka = dane['unit'] # jednostka uF lub mH
                    napiecie = float(global_u1) #napiecie pobrane z pliku CSV
                    #7
                    prad, napiecie_rezystor, napiecie_kondensator, moc_rezystor = oblicz_parametry_RC(dane_wartosc,
                                                                                                      napiecie, 33,
                                                                                                   50)
                    I_min, I_max = prad_z_marginesem(prad)
                    print(f"Prąd obliczony: {prad} A, zakres -20%: {I_min:.2f} A , +20% {I_max:.2f} A")
                    if global_i1 >= I_min and global_i1 <= I_max:
                        print("Wartosc pradu z rezystorem miesci sie w widełkach")
                        print(f"Prad zmiwerzony : {global_i1}")
                        print("Załączamy bez rezystora")
                        informacja_zwrotna = wyslij_komende(mikrokontroler, "start1")
                        time.sleep(2)
                        read_csv_to_globals()
                        informacja_zwrotna = wyslij_komende(mikrokontroler, "on1fazowy")
                        time.sleep(0.1)
                        informacja_zwrotnaA = wyslij_komende(mikrokontroler, "stop1")
                        time.sleep(2)
                        informacja_zwrotnaB = wyslij_komende(mikrokontroler, "off1fazowy")
                        print(f"napiecie: {global_u1}, prąd: {global_i1}, moc bierna: {global_q1}")
                        widelki_dolne_float = float(widelki_dolne) * 0.01
                        widelki_gorne_float = float(widelki_gorne) * 0.01
                        print(f"sprawdzamy dla widełek: \n"
                              f"górne: {widelki_gorne} %, float: {widelki_gorne_float}\n"
                              f"dolne: {widelki_dolne} %, float: {widelki_dolne_float}")
                        napiecie = float(global_u1)
                        moc_pomiar = calculate_single_phase_power(dane_wartosc, napiecie, 50)

                        moc_float= float(moc_pomiar)
                        print(f"wyliczona moc: {moc_float}")
                        dane_float_moc_kvar = get_first_float_from_string(last_selected_item)
                        print(f"moc podana przez producenta: {dane_float_moc_kvar}")
                        wynik, dane = check_power_within_limits(dane_float_moc_kvar, moc_float, widelki_gorne_float, widelki_dolne_float)

                        if wynik == True:
                            print(f"wynik testu = {wynik} ")
                            print(f"wynik testu = {dane} D")
                            zapisz_wynik_testu_dziala("kondensatory1fazowe_dobre.csv","1 fazwoy kondensator", moc_pomiar, last_selected_item,"Działa")
                        if wynik == False:
                            print(f"wynik testu = {wynik} ")
                            print(f"wynik testu = {dane} Z")
                            zapisz_wynik_testu_niedziala("kondensatory1fazowe_zle.csv","1 fazwoy kondensator", moc_pomiar, last_selected_item,"NIE DZIAŁA !!!")



                    else:
                        print("Wartosc pradu z rezystorem nie miesci sie w widełkach")
                        print(f"Prad zmiwerzony : {global_i1}")
                        
                """
        elif selected_list == "2":
            print("wybrano kondensator 3 fazowy")
            print("Liczymy wartosc pradu z rezystorem\n"
                  "dla kondensatora 3 fazowego")
            print("Uruchamiamy pomiar z rezystorem")
            read_csv_to_globals

            # 4
            informacja_zwrotna = wyslij_komende(mikrokontroler, "p2")
            wartos_zwrotna_float = float(informacja_zwrotna)
            print(f"wartosc zwrucona tp : {wartos_zwrotna_float}")
            napiecie = float(global_u_avg)
            prad_fazowy, prad_przewodowy, napiecie_rezystor, napiecie_kondensator, moc_calkowita = oblicz_parametry_RC_trojfazowy(dane_wartosc,
                                                                                              33, napiecie,
                                                                                              50)
            print(prad_fazowy)
            print(prad_przewodowy)
            prad = float(prad_przewodowy)
            print(napiecie_kondensator)
            print(moc_calkowita)
            I_min, I_max = prad_z_marginesem(prad)
            print(f"widelki I_min: {I_min}")
            print(f"widelki I_max: {I_max}")
            if wartos_zwrotna_float >= I_min and wartos_zwrotna_float <= I_max:
                print("prad miesci sie w zakresie")
                informacja_zwrotna2 = ""
                informacja_zwrotna2 = wyslij_komende(mikrokontroler, "2")
                if informacja_zwrotna2 != "":
                    print("zalaczamy kondensator 3 fazowy")
                    time.sleep(3)
                    read_csv_to_globals()
                    print(f"prad wynosił : I1 {global_i1} , I2 {global_i2} , I3 {global_i3}")

                    dane = extract_reactive_value(last_selected_item)
                    dane_typ = dane['type']  # typ np C lub L
                    dane_wartosc = float(dane['value'])  # wartosc w mH lub uF
                    dane_jednostka = dane['unit']  # jednostka uF lub mH
                    napiecie = float(global_u_avg)  # napiecie pobrane z pliku CSV

                    widelki_dolne_float = float(widelki_dolne) * 0.01
                    widelki_gorne_float = float(widelki_gorne) * 0.01
                    print(f"sprawdzamy dla widełek: \n"
                          f"górne: {widelki_gorne} %, float: {widelki_gorne_float}\n"
                          f"dolne: {widelki_dolne} %, float: {widelki_dolne_float}")
                    napiecie = float(global_u_avg)
                    Q1 = float(global_q1)
                    Q2 = float(global_q2)
                    Q3 = float(global_q3)
                    Qn = Q1*(-1) + Q2*(-1) + Q3
                    moc_pomiar = calculate_capacitor_power_delta(dane_wartosc, napiecie, 50)

                    print()
                    print(f"Qn policzone - jako suma Q1 + Q2 + Q3 z analizatora : {Qn}")
                    print()

                    moc_float = float(moc_pomiar)
                    print(f"wyliczona moc: {moc_float}")
                    dane_float_moc_kvar = get_second_float_from_string(last_selected_item)

                    print(f"moc podana przez producenta: {dane_float_moc_kvar}")
                    wynik, dane = check_power_within_limits(dane_float_moc_kvar, Qn, widelki_gorne_float,
                                                            widelki_dolne_float)

                    if wynik == True:
                        print(f"wynik testu = {wynik} ")
                        print(f"wynik testu = {dane} D")
                        zapisz_wynik_testu_dziala("kondensatory3fazowe_dobre.csv", "3 fazwoy kondensator", moc_pomiar,
                                                  last_selected_item, "Działa")
                    if wynik == False:
                        print(f"wynik testu = {wynik} ")
                        print(f"wynik testu = {dane} Z")
                        zapisz_wynik_testu_niedziala("kondensatory3fazowe_zle.csv", "3 fazwoy kondensator", moc_pomiar,
                                                     last_selected_item, "NIE DZIAŁA !!!")




            else :
                print("prad poza zakresem")










    else:
        print(f"nie otrzymano poprawnej odpowiedzi na porcie: {COM}")
    input("Naciśnij Enter, aby zamknąć okno...")











