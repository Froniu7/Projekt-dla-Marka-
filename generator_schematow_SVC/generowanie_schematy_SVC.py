import tkinter as tk
from PIL import Image
from tkinter import messagebox
from generator_schematow_SVC.generowanie_grafik import generuj_grafike_z_tekstem


#***********************************************************************************************************************
#BLOK 1
# w tym bloku są zmienne
# poniżej są zmienne dla funkcji pobierz_dane() - oraz dla ustawienia wartości początkowych - czyli tych które są
#zaznaczone zaraz po uruchomieniu programu - przypisanie tych wartości do przycisków w funkcji tk.StringVar(value="nazwa zmiennej")
zab_zew = "typ S - C 3polowe"
podzespoly_dodatkowe = "tylko łącznik tyrystorowy i 3 dlawiki"
zabezpieczenie_lacznika = "lacznik i stopnie - wspolne zabezpieczenie"
ilosc_stopni = 0
s4 = ""
s5 = ""
s6 = ""
s7 = ""
s8 = ""
s9 = ""
s10 = ""
s11 = ""
s12 = ""
s13 = ""
s14 = ""
s15 = ""
dodatkowe_stopnie = ["", "", "", "", "", "", "", "", "", "", "", ""]

#***********************************************************************************************************************
#BLOK 2
# Tworzymy główne okno - narazie puste , w kolejnych blokach dodajemy elementy
root = tk.Tk()
root.title("Wybór opcji")

#***********************************************************************************************************************
#BLOK 3
#tu blok kodu odpowiedzialny za pierwsze przyciski radiowe i obsługę tych przycisków ( wybranie rodzaju zabezpieczenia zew. inaczej glównego
#Wyświetlamy informacje nad pierwszymi przyciskami radiowymi
zabezpieczenia_zew = tk.Label(text="Wybierz rodzaj zabezpieczenia zewnetrznego")
zabezpieczenia_zew.grid(row=0, column=0)

#Funkcja do obslugi przyciskow - jest przed deklaracją przyciskow - aby ją widziały
#będzie wywoływana przez wybranie jedengo z przycisków
# Funkcja wywoływana po zmianie wyboru lub kliknięciu na juz zaznaczony
def pokaz_wybor():
    global zab_zew
    print("Wybrano:", wybor.get())
    zab_zew = wybor.get() # do zmiennej przypisujemy wartosc wybraną -

# Zmienna do przechowywania wybranej wartości - gdzie value to wartość początkowa - może się zmienić podczas pracy z GUI
wybor = tk.StringVar(value=zab_zew)  # Domyślnie wybrana opcja, zmienna zab_zew jest na początku skryptu

# Tworzenie przycisków radiowych
opcje = ["typ S - C 3polowe", "wkladki topikowe gG", "brak zabezpieczenia glownego"]
i = 1
for opcja in opcje:

    tk.Radiobutton(root, text=opcja, variable=wybor, value=opcja, command=pokaz_wybor).grid(row=i , column=0)
    i = i+1

#tu koniec bloku odpowiedzialnego za pierwsze przyciski radiowe - odnosnie zabezpieczenia zew. - głównego

#***********************************************************************************************************************
#BLOK 4
#tu blok  odpowiedzialny za przyciski radiowe - odnosnie - czy są dodatkowe stopnie
#wyświetlenie pierwszego tekstu
lacznik_tyrystorowy_i_stopnie = tk.Label(text="Ilosc podzespolow")
lacznik_tyrystorowy_i_stopnie.grid(row=4, column=0) #gdzie umieszczone

#funkcja do obsługi wybranego przyciski - funkcja musi być przed deklaracją przyciskow,
#działanie jeżeli zostanie wybrany przycisk - "dodatkowe stopnie" to funkcja ma umiejscowić w oknie
#dodatkowe pola na wpisanie wartości - dodatkowych stopni - definicje dodatkowych elementow są w innym BLOKU

def pokaz_wybor2():
    global miejsce_podlaczenia_zab, radio_buttons, podzespoly_dodatkowe

    print("Wybrano:", wybor2.get())
    podzespoly_dodatkowe = wybor2.get()

    # Jeśli były wcześniej dodane przyciski, usuwamy je
    for rb in radio_buttons:
        rb.destroy()
    radio_buttons.clear()

    # Ukrywanie etykiety, jeśli istnieje
    if miejsce_podlaczenia_zab:
        miejsce_podlaczenia_zab.destroy()
        miejsce_podlaczenia_zab = None

    if wybor2.get() == "tylko łącznik tyrystorowy i 3 dlawiki":
        print("mamy to")
        if dodatkowe_stopnie_jednfazowe is not None:
            dodatkowe_stopnie_jednfazowe.grid_forget()
        if stopien4 is not None:
            stopien4.grid_forget()
        if stopien5 is not None:
            stopien5.grid_forget()
        if stopien6 is not None:
            stopien6.grid_forget()
        if stopien7 is not None:
            stopien7.grid_forget()
        if stopien8 is not None:
            stopien8.grid_forget()
        if stopien9 is not None:
            stopien9.grid_forget()
        if dodatkowe_stopnie_trzyfazowe is not None:
            dodatkowe_stopnie_trzyfazowe.grid_forget()
        if stopien10 is not None:
            stopien10.grid_forget()
        if stopien11 is not None:
            stopien11.grid_forget()
        if stopien12 is not None:
            stopien12.grid_forget()
        if stopien13 is not None:
            stopien13.grid_forget()
        if stopien14 is not None:
            stopien14.grid_forget()
        if stopien15 is not None:
            stopien15.grid_forget()



    # Jeśli wybrano "dodatkowe stopnie", tworzymy nowe widgety
    if wybor2.get() == "dodatkowe stopnie":
        miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposób podłączenia zabezpieczenia łącznika tyrystorowego")
        miejsce_podlaczenia_zab.grid(row=7, column=0)

        for i, opcja in enumerate(opcje3):
            rb = tk.Radiobutton(root, text=opcja, variable=wybor3, value=opcja)
            rb.grid(row=i+8, column=0)
            radio_buttons.append(rb)  # Przechowujemy referencję do przycisku

        dodatkowe_stopnie_jednfazowe.grid(row=14, column=0)
        stopien4.grid(row=15, column=0)
        stopien5.grid(row=16, column=0)
        stopien6.grid(row=17, column=0)
        stopien7.grid(row=15, column=1)
        stopien8.grid(row=16, column=1)
        stopien9.grid(row=17, column=1)
        dodatkowe_stopnie_trzyfazowe.grid(row=18,column=0)
        stopien10.grid(row=19, column=0)
        stopien11.grid(row=19, column=1)
        stopien12.grid(row=19, column=2)
        stopien13.grid(row=19, column=3)
        stopien14.grid(row=19, column=4)
        stopien15.grid(row=19, column=5)



# Zmienna do przechowywania wybranej wartości - gdzie value to wartość początkowa - może się zmienić podczas pracy z GUI
wybor2 = tk.StringVar(value=podzespoly_dodatkowe)
opcje2 = ["tylko łącznik tyrystorowy i 3 dlawiki", "dodatkowe stopnie"]
i = 5
for opcja2 in opcje2:

    tk.Radiobutton(root, text=opcja2, variable=wybor2, value=opcja2, command=pokaz_wybor2).grid(row=i , column=0)
    i = i+1


#***********************************************************************************************************************
#BLOK 5
# trzecia częśc przyciskow radiowych - dostepna jezeli wybiorę opcje - dodatkowe stopnie
# Zmienna do przechowywania wybranej wartości - gdzie value to wartość początkowa - może się zmienić podczas pracy z GUI
wybor3 = tk.StringVar(value=zabezpieczenie_lacznika)
opcje3 = ["lacznik tyrystorowy ma swoje zabezpieczenie", "lacznik i stopnie - wspolne zabezpieczenie"]
# Przechowywanie dynamicznie tworzonych widgetów
radio_buttons = []
miejsce_podlaczenia_zab = None




#***********************************************************************************************************************
#BLOK 6
#
miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposub podlaczenia zabezpieczenia lacznika tyrystorowego")

opis_dlawiki_lacznik = tk.Label(root, text="podaj warosci trzech dlawikow podpietych do lacznika tyrystorowe")
opis_dlawiki_lacznik .grid(row=10,column=0)

#pola do wpisywania wartości dla trzech dławików - tych co są zawsze , podpięte do łącznika tyrystorowego
dlawik1 = tk.Entry(root, width=30)
dlawik1.grid(row=11,column=0)
dlawik2= tk.Entry(root, width=30)
dlawik2.grid(row=12,column=0)
dlawik3= tk.Entry(root, width=30)
dlawik3.grid(row=13,column=0)

#***********************************************************************************************************************
#BLOK7
#dodatkowe_stopnie - wyświetlane jeżeli zostanie wykonana funkcja
dodatkowe_stopnie_jednfazowe = tk.Label(root, text="Podaj wartosci stopni jednofazowych")
stopien4= tk.Entry(root, width=30)
stopien5= tk.Entry(root, width=30)
stopien6= tk.Entry(root, width=30)
stopien7= tk.Entry(root, width=30)
stopien8= tk.Entry(root, width=30)
stopien9= tk.Entry(root, width=30)
dodatkowe_stopnie_trzyfazowe = tk.Label(root, text="Podaj wartosci stopni trzyfazowych")
stopien10= tk.Entry(root, width=30)
stopien11= tk.Entry(root, width=30)
stopien12= tk.Entry(root, width=30)
stopien13= tk.Entry(root, width=30)
stopien14= tk.Entry(root, width=30)
stopien15= tk.Entry(root, width=30)


#***********************************************************************************************************************
#BLOK8
#BLOK - pobierz_dane - tak będę go wewnątrz funkcji opisywał - aby podzielić ją na części

def pobierz_dane():
    global zab_zew, podzespoly_dodatkowe, wybor3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, dodatkowe_stopnie
    print(zab_zew)
    print(podzespoly_dodatkowe)
    zabezpieczenie_lacznika=wybor3.get()
    print(zabezpieczenie_lacznika)

    #-------------------------------------------------------------------------------------------------------------------

    #BLOK - pobierz_dane - przypisywanie do zmiennych od podzespoly - tu pobieramy wartości dla wszystkich mozliwych podzespolów - czyli dłaików i kondensatorów , mogą tez byc puste zmienne - czyli pusty string -> ""

    d1 = dlawik1.get()
    print(f"d1 = {d1}")
    d2 = dlawik2.get()
    print(f"d2 = {d2}")
    d3 = dlawik3.get()
    print(f"d3 = {d3}")
    s4 = stopien4.get()
    print(f"s4 = {s4}")
    dodatkowe_stopnie[0] = s4
    s5 = stopien5.get()
    print(f"s5 = {s5}")
    dodatkowe_stopnie[1] = s5
    s6 = stopien6.get()
    print(f"s6 = {s6}")
    dodatkowe_stopnie[2] = s6
    s7 = stopien7.get()
    print(f"s7 = {s7}")
    dodatkowe_stopnie[3] = s7
    s8 = stopien8.get()
    print(f"s8 = {s8}")
    dodatkowe_stopnie[4] = s8
    s9 = stopien9.get()
    print(f"s9 = {s9}")
    dodatkowe_stopnie[5] = s9
    s10 = stopien10.get()
    print(f"s10 = {s10}")
    dodatkowe_stopnie[6] = s10
    s11 = stopien11.get()
    print(f"s11 = {s11}")
    dodatkowe_stopnie[7] = s11
    s12 = stopien12.get()
    print(f"s12 = {s12}")
    dodatkowe_stopnie[8] = s12
    s13 = stopien13.get()
    print(f"s13 = {s13}")
    dodatkowe_stopnie[9] = s13
    s14 = stopien14.get()
    print(f"s14 = {s14}")
    dodatkowe_stopnie[10] = s14
    s15 = stopien15.get()
    print(f"s15 = {s15}")
    dodatkowe_stopnie[11] = s15
    # BLOK - pobierz_dane - schemat podstawowy
    # jezeli nie została zaznaczona opcja dodatkowe stopnie to zostanie wybrany jedna z ponizszych grafik

    #-------------------------------------------------------------------------------------------------------------------

    #BLOK - pobierz_dane -> brak dodatkowych podzespolow
    #to jest podzielone na czesc
    # ta czesc odpowiedzialna za schematy z termostatem - badz bez , oraz za schematy bez dodatkowych stopni
    if zab_zew == "typ S - C 3polowe" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        print("jestemy w if ")
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")

    if zab_zew == "wkladki topikowe gG" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        print("jestemy w if ")
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie_termostat_zabezpieczenie_zew_gG.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")

    if zab_zew == "brak zabezpieczenia glownego" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        print("jestemy w if ")
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie_termostat.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")

    #-------------------------------------------------------------------------------------------------------------------

    # BLOK - pobierz_dane -> dodatkowe stopnie
    # dodatkowe stopnie
    if zab_zew == "typ S - C 3polowe" and podzespoly_dodatkowe == "dodatkowe stopnie":
        global ilosc_stopni
        policz_dodatkowe_stopnie()
        print(f"mamy stopni {ilosc_stopni}")
        print(dodatkowe_stopnie)



        if ilosc_stopni <= 6:

            # ----------------------------------------------------------------------------------------------------------
            # BLOK - pobierz_dane - dodatkowe stopnie -> generowanie grafiki z dodatkowymi stopniami

            if ilosc_stopni == 1:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_1stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size
            if ilosc_stopni == 2:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_2stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size
            if ilosc_stopni == 3:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_3stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size
            if ilosc_stopni == 4:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_4stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size
            if ilosc_stopni == 5:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_5stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size
            if ilosc_stopni == 6:
                schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_6stopnie_C_wszystkie_stopnie.png")
                width_podstawowy, height_podstawowy = schemat_podstawowy.size

            siec_i_3_fazy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_glowne_i_siec.png")
            width_sieci_i_fazy, height_sieci_i_fazy = siec_i_3_fazy.size

            obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy + height_sieci_i_fazy))
            obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
            obraz_do_wygenerowania.paste(siec_i_3_fazy, (0, height_podstawowy))


            # zmienna szerokosc_wstawianie_sciezki - bedzie urzywana do przesówania grafik od stopni , po kazdym dodaniu stopnia będzie dodawana jego szerokość
            # dzieki temu kazdy kolejny stopien będzie przesuniety w prawo na schemacie

            szerokosc_wstawianie_sciezki = width_sieci_i_fazy
            ilosc_umieszczonych_stopni = 3
            nazwa_pliku = "grafika.png"



            for i in range(len(dodatkowe_stopnie)): #liczymy ile jest elementow w tablicy
                zawartosc = dodatkowe_stopnie[i]
                if zawartosc== "":
                    print("brak stopnia")
                else:

                    # --------------------------------------------------------------------------------------------------
                    # BLOK - pobierz_dane - dodatkowe stopnie -> generowanie grafiki z dodatkowymi stopniami ->
                    # -> jednofazowe
                    if i <= 5 :
                        print("dodanie sciezek dla elementow jednofazowych")
                        if i == 0:
                            sciezki_stopien_1 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza1.png")
                            width_sciezki_stopien_1, height_sciezki_stopien_1 = sciezki_stopien_1.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_1, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_1 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_1 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s1, h_s1 = stopien_1.size

                            obraz_do_wygenerowania.paste(stopien_1,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_1))


                            opis_stopien1 = Image.open(f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni+1}.png")
                            w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien1, (szerokosc_wstawianie_sciezki, height_podstawowy + height_sciezki_stopien_1+ h_s1))

                            generuj_grafike_z_tekstem("1",1299,236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                  (szerokosc_wstawianie_sciezki, height_podstawowy + height_sciezki_stopien_1 + h_s1))


                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_1



                        if i == 1:
                            sciezki_stopien_2 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza2.png")
                            width_sciezki_stopien_2, height_sciezki_stopien_2 = sciezki_stopien_2.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_2, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_2 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_2 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s2, h_s2 = stopien_2.size

                            obraz_do_wygenerowania.paste(stopien_2,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_2))

                            opis_stopien2 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni+1}.png")
                            # w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien2, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_2 + h_s2))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_2

                        if i == 2:
                            sciezki_stopien_3 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza3.png")
                            width_sciezki_stopien_3, height_sciezki_stopien_3 = sciezki_stopien_3.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_3, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_3 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_3 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s3, h_s3 = stopien_3.size

                            obraz_do_wygenerowania.paste(stopien_3,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_3))

                            opis_stopien3 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            # w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien3, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_3 + h_s3))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_3

                        if i == 3:
                            sciezki_stopien_4 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza1.png")
                            width_sciezki_stopien_4, height_sciezki_stopien_4 = sciezki_stopien_4.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_4, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_4 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_4 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s4, h_s4 = stopien_4.size

                            obraz_do_wygenerowania.paste(stopien_4,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_4))

                            opis_stopien4 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            # w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien4, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_4 + h_s4))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_4

                        if i == 4:
                            sciezki_stopien_5 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza2.png")
                            width_sciezki_stopien_5, height_sciezki_stopien_5 = sciezki_stopien_5.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_5, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_5 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_5 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s5, h_s5 = stopien_5.size

                            obraz_do_wygenerowania.paste(stopien_5,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_5))

                            opis_stopien5 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            # w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien5, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_5 + h_s5))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_5

                        if i == 5:
                            sciezki_stopien_6 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_faza3.png")
                            width_sciezki_stopien_6, height_sciezki_stopien_6 = sciezki_stopien_6.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_6, (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_6 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/2_jednofazowe_dlawiki/blok_1_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_6 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/1_jednofazowe_kondensatory/blok_1_fazowy_kondensator.png")

                            w_s6, h_s6 = stopien_6.size

                            obraz_do_wygenerowania.paste(stopien_6,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_6))

                            opis_stopien6 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            # w_o_s1, h_o_s1 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien1, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_6 + h_s6))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_6

                    # --------------------------------------------------------------------------------------------------
                    # BLOK - pobierz_dane - dodatkowe stopnie -> generowanie grafiki z dodatkowymi stopniami ->
                    # -> trzyfazowe

                    if i >= 6 :

                        print("dodanie sciezek dla elementow trzyfazowych")
                        if i == 6:
                            sciezki_stopien_7 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_7, height_sciezki_stopien_7 = sciezki_stopien_7.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_7,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_7 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_7 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s7, h_s7 = stopien_7.size

                            obraz_do_wygenerowania.paste(stopien_7,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_7))

                            opis_stopien7 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien7, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_7 + h_s7))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_7



                        if i == 7:
                            sciezki_stopien_8 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_8, height_sciezki_stopien_8 = sciezki_stopien_8.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_8,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))
                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_8 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_8 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s8, h_s8 = stopien_8.size

                            obraz_do_wygenerowania.paste(stopien_8,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_8))

                            opis_stopien8 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien8, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_8 + h_s8))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_8

                        if i == 8:
                            sciezki_stopien_9 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_9, height_sciezki_stopien_9 = sciezki_stopien_9.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_9,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))
                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_7 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_9 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s9, h_s9 = stopien_9.size

                            obraz_do_wygenerowania.paste(stopien_9,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_9))

                            opis_stopien9 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien9, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_9 + h_s9))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_9

                        if i == 9:
                            sciezki_stopien_10 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_10, height_sciezki_stopien_10 = sciezki_stopien_10.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_10,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))
                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_10 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_10 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s10, h_s10 = stopien_10.size

                            obraz_do_wygenerowania.paste(stopien_10,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_10))

                            opis_stopien10 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien10, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_10 + h_s10))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_10

                        if i == 10:
                            sciezki_stopien_11 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_11, height_sciezki_stopien_11 = sciezki_stopien_11.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_11,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_11 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_11 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s11, h_s11 = stopien_11.size

                            obraz_do_wygenerowania.paste(stopien_11,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_11))

                            opis_stopien11 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien11, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_11 + h_s11))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_11

                        if i == 11:
                            sciezki_stopien_12 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_12, height_sciezki_stopien_12 = sciezki_stopien_12.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_12,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))

                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_12 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/3_trzyfazowe_dlawiki/3_fazowy_dlawik.png")
                            else:
                                print("na schemacie zostanie umiejscowiony kondensator jednofazowy")
                                stopien_12 = Image.open(
                                    "pod_3_stopnie_uniwersalny/stopnie/4_trzyfazowe_kondensatory/blok_3_fazowy_kondensator.png")

                            w_s12, h_s12 = stopien_12.size

                            obraz_do_wygenerowania.paste(stopien_12,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy+height_sciezki_stopien_12))

                            opis_stopien12 = Image.open(
                                f"pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/oznaczenia_stopnie/Q{ilosc_umieszczonych_stopni + 1}.png")
                            ilosc_umieszczonych_stopni += 1


                            obraz_do_wygenerowania.paste(opis_stopien12, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_12 + h_s12))

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_12

                '''
                for i in range(len(dodatkowe_stopnie)): #liczymy ile jest elementow w tablicy
                    zawartosc = dodatkowe_stopnie[i]
                    if zawartosc== "":
                        print("brak stopnia")
                    elif zawartosc.startswith("-"):
                        print("dławik")
                        obraz_do_wygenerowania = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/SVC_3_termostat_zew_gG_6stopnie_C_wszystkie_stopnie.png")
                    else:
                        print("kondensator")
                '''

            obraz_do_wygenerowania.save(f"wygenerowany.png")
            ilosc_stopni = 0

        #---------------------------------------------------------------------------------------------------------------
        #BLOK - pobierz_dane - dodatkowe stopnie -> nie generujemy schematu , wyswietlamy komunikat
        else :
            messagebox.showinfo("Informacja", "Przekroczono ilosc stopni , aplikacja pozwala na max 6")
            print("przekroczona ilosc stopni")
            print(dodatkowe_stopnie)
            ilosc_stopni = 0

def policz_dodatkowe_stopnie():
    global ilosc_stopni, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15
    if s4 != "":
        ilosc_stopni=ilosc_stopni+1
    if s5 != "":
        ilosc_stopni=ilosc_stopni+1
    if s6 != "":
        ilosc_stopni=ilosc_stopni+1
    if s7 != "":
        ilosc_stopni=ilosc_stopni+1
    if s8 != "":
        ilosc_stopni=ilosc_stopni+1
    if s9 != "":
        ilosc_stopni=ilosc_stopni+1
    if s10 != "":
        ilosc_stopni=ilosc_stopni+1
    if s11 != "":
        ilosc_stopni=ilosc_stopni+1
    if s12 != "":
        ilosc_stopni=ilosc_stopni+1
    if s13 != "":
        ilosc_stopni=ilosc_stopni+1
    if s14 != "":
        ilosc_stopni=ilosc_stopni+1
    if s15 != "":
        ilosc_stopni=ilosc_stopni+1

generuj_schemat = tk.Button(root, text="Generuj", command=pobierz_dane)
generuj_schemat.grid(row=1, column=1)

# Uruchomienie pętli głównej
root.mainloop()
