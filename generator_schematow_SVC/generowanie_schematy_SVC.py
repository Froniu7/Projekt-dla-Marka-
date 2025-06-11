import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from generator_schematow_SVC.generowanie_grafik import ToolTip, generuj_grafike_z_tekstem, generuj_plik_docx, konwertuj_docx_na_pdf, zapisz_plik_do_katalogu, show_non_blocking_message, close_message_window
import os

#***********************************************************************************************************************
#BLOK 1
# w tym bloku są zmienne
# poniżej są zmienne dla funkcji pobierz_dane() - oraz dla ustawienia wartości początkowych - czyli tych które są
#zaznaczone zaraz po uruchomieniu programu - przypisanie tych wartości do przycisków w funkcji tk.StringVar(value="nazwa zmiennej")
zab_zew = "typ S - C 3polowe"
podzespoly_dodatkowe = "tylko łącznik tyrystorowy i 3 dlawiki"
zabezpieczenie_lacznika = "główne zab. oraz zabezpieczenia stopni"
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
sekcja2b = None  # kontener na dodatkowe opcje
sekcja2c = None # kontener na dodatkowe stopnie
# dodatkowe_stopnie - wyświetlane jeżeli zostanie wykonana funkcja
stopien4 = None
stopien5 = None
stopien6 = None
stopien7 = None
stopien8 = None
stopien9 = None
stopien10 = None
stopien11 = None
stopien12 = None
stopien13 = None
stopien14 = None
stopien15 = None
dodatkowe_stopnie_jednfazowe = None
dodatkowe_stopnie_trzyfazow = None


#***********************************************************************************************************************
#BLOK 2
# Tworzymy główne okno - narazie puste , w kolejnych blokach dodajemy elementy
# tworzymy górne przyciski
root = tk.Tk()
root.title("Wybór opcji")



#***********************************************************************************************************************
#BLOK 3
#tu blok kodu odpowiedzialny za pierwsze przyciski radiowe i obsługę tych przycisków ( wybranie rodzaju zabezpieczenia zew. inaczej glównego
# === SEKCJA 1 === - kontener z niebieskim tłem
sekcja1 = tk.Frame(root, bg="lightblue", bd=2, relief="solid", padx=10, pady=10, width =480, height=170)
sekcja1.grid(row=1, column=0)
sekcja1.grid_propagate(False)

#Wyświetlamy informacje nad pierwszymi przyciskami radiowymi
zabezpieczenia_zew = tk.Label(sekcja1,text="Wybierz rodzaj zabezpieczenia zewnetrznego:", bg="lightblue", font=("Verdana", 14))
zabezpieczenia_zew.grid(row=0, column=0)
pusty_label_pod_zabezpieczenia_zew = tk.Label(sekcja1, text = "   ", bg="lightblue", font=("Verdana", 14))
pusty_label_pod_zabezpieczenia_zew.grid(row=1, column=0)
tooltip_zabezpieczenie_zew=ToolTip(zabezpieczenia_zew,"Zabezpieczenie zewnętrzne - czyli to poza skrzynką.\nJest umieszczone np: w szafie w rozdzielni.", delay=1000, image_path="grafiki_GUI/strzalka.png")

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
i = 2
for opcja in opcje:

    tk.Radiobutton(sekcja1, text=opcja, variable=wybor, value=opcja, command=pokaz_wybor, bg="lightblue", font=("Verdana", 11)).grid(row=i , column=0, sticky="w")
    i = i+1

#tu koniec bloku odpowiedzialnego za pierwsze przyciski radiowe - odnosnie zabezpieczenia zew. - głównego

#***********************************************************************************************************************
#BLOK 4
#tu blok  odpowiedzialny za przyciski radiowe - odnosnie - czy są dodatkowe stopnie
# === SEKCJA 2 ===
sekcja2 = tk.Frame(root, bg="grey", bd=2, relief="solid", padx=10, pady=10, width =480, height=135)
sekcja2.grid(row=2, column=0)
sekcja2.grid_propagate(False)
#wyświetlenie pierwszego tekstu
lacznik_tyrystorowy_i_stopnie = tk.Label(sekcja2 ,text="Ilosc podzespolow:\n ", bg="grey", font=("Verdana", 14))
lacznik_tyrystorowy_i_stopnie.grid(row=0, column=0, sticky="w") #gdzie umieszczone

#funkcja do obsługi wybranego przyciski - funkcja musi być przed deklaracją przyciskow,
#działanie jeżeli zostanie wybrany przycisk - "dodatkowe stopnie" to funkcja ma umiejscowić w oknie
#dodatkowe pola na wpisanie wartości - dodatkowych stopni - definicje dodatkowych elementow są w innym BLOKU

def pokaz_wybor2():
    global miejsce_podlaczenia_zab, radio_buttons, podzespoly_dodatkowe, sekcja2b, sekcja2c
    global stopien4, stopien5, stopien6, stopien7, stopien8, stopien9, stopien10, stopien11, stopien12, stopien13, stopien14, stopien15
    global dodatkowe_stopnie_jednfazowe, dodatkowe_stopnie_trzyfazow
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



    # Jeśli wybrano "dodatkowe stopnie", tworzymy nowe widgety
    if wybor2.get() == "dodatkowe stopnie":

        # Usowanie nawet jezeli nie istnieją bo jak klikniesz przez przypadek to powstanie dwa razy ten sam kontener 
        if sekcja2b:
            sekcja2b.destroy()
            sekcja2b = None
        if sekcja2c:
            sekcja2c.destroy()
            sekcja2c = None

        sekcja2b = tk.Frame(root, bg="lightgreen", bd=2, relief="solid", padx=10, pady=10, width=480, height=135)
        sekcja2b.grid(row=3, column=0)
        sekcja2b.grid_propagate(False)

        miejsce_podlaczenia_zab = tk.Label(sekcja2b,
                                           text="Wybierz sposób podłączenia zabezpieczenia łącznika tyrystorowego:\n ", bg="lightgreen", font=("Verdana", 10))
        miejsce_podlaczenia_zab.grid(row=7, column=0, sticky="w")

        for i, opcja in enumerate(opcje3):

            rb = tk.Radiobutton(sekcja2b, text=opcja, variable=wybor3, value=opcja, bg="lightgreen", font=("Verdana", 10))
            rb.grid(row=i+8, column=0, sticky="w")
            radio_buttons.append(rb)  # Przechowujemy referencję do przycisku

        sekcja2c = tk.Frame(root, bg="red", bd=2, relief="solid", padx=10, pady=10, width=480, height=230)
        sekcja2c.grid(row=5, column=0)
        sekcja2c.grid_propagate(False)

        # dodatkowe_stopnie - wyświetlane jeżeli zostanie wykonana funkcja
        dodatkowe_stopnie_jednfazowe = tk.Label(sekcja2c, text="Podaj wartosci stopni jednofazowych: \n", bg = "red", font=("Verdana", 12))
        dodatkowe_stopnie_jednfazowe.grid(row=0, column=0, columnspan=11, sticky="w")

        L1 = tk.Label(sekcja2c, text="L1: ", bg="red")
        L1.grid(row=1,column=0)

        stopien4 = tk.Entry(sekcja2c, width=10)
        stopien4.grid(row=1, column=1)

        L2 = tk.Label(sekcja2c, text="L2: ", bg="red")
        L2.grid(row=2, column=0)

        stopien5 = tk.Entry(sekcja2c, width=10)
        stopien5.grid(row=2, column=1)

        L3 = tk.Label(sekcja2c, text="L2: ", bg="red")
        L3.grid(row=3, column=0)

        stopien6 = tk.Entry(sekcja2c, width=10)
        stopien6.grid(row=3, column=1)

        plusL1 = tk.Label(sekcja2c, text=" + ", bg="red", font=("Verdana", 10))
        plusL1.grid(row=1, column=2)
        stopien7 = tk.Entry(sekcja2c, width=10)
        stopien7.grid(row=1, column=3)

        plusL2 = tk.Label(sekcja2c, text=" + ", bg="red", font=("Verdana", 10))
        plusL2.grid(row=2, column=2)
        stopien8 = tk.Entry(sekcja2c, width=10)
        stopien8.grid(row=2, column=3)

        plusL3 = tk.Label(sekcja2c, text=" + ", bg="red", font=("Verdana", 10))
        plusL3.grid(row=3, column=2)
        stopien9 = tk.Entry(sekcja2c, width=10)
        stopien9.grid(row=3, column=3)

        dodatkowe_stopnie_trzyfazowe = tk.Label(sekcja2c, text="\nPodaj wartosci stopni trzyfazowych:\n", bg ="red", font=("Verdana", 12))
        dodatkowe_stopnie_trzyfazowe.grid(row=4, column=0, columnspan=11, sticky="w")

        L123 = tk.Label(sekcja2c, text="L123: ", bg="red" )
        L123.grid(row=5, column= 0)
        stopien10 = tk.Entry(sekcja2c, width=8)
        stopien10.grid(row=5, column=1)
        plusL123 = tk.Label(sekcja2c, text="+", bg="red", font=("Verdana", 10))
        plusL123.grid(row=5, column=2)
        stopien11 = tk.Entry(sekcja2c, width=8)
        stopien11.grid(row=5, column=3)
        plusL123b = tk.Label(sekcja2c, text="+", bg="red", font=("Verdana", 10))
        plusL123b.grid(row=5, column=4)
        stopien12 = tk.Entry(sekcja2c, width=8)
        stopien12.grid(row=5, column=5)
        plusL123c = tk.Label(sekcja2c, text="+", bg="red", font=("Verdana", 10))
        plusL123c.grid(row=5, column=6)
        stopien13 = tk.Entry(sekcja2c, width=8)
        stopien13.grid(row=5, column=7)
        plusL123d = tk.Label(sekcja2c, text="+", bg="red", font=("Verdana", 10))
        plusL123d.grid(row=5, column=8)
        stopien14 = tk.Entry(sekcja2c, width=8)
        stopien14.grid(row=5, column=9)
        plusL123e = tk.Label(sekcja2c, text="+", bg="red", font=("Verdana", 10))
        plusL123e.grid(row=5, column=10)
        stopien15 = tk.Entry(sekcja2c, width=8)
        stopien15.grid(row=5, column=11)


    if wybor2.get() == "tylko łącznik tyrystorowy i 3 dlawiki":
        print("wybrana opcja - tylko lacznik tyrystorowy i 3 dlawiki ")

        if sekcja2b:
            print("usowamy kontener sekcja2b")
            sekcja2b.destroy()
            sekcja2b = None

        if sekcja2c:
            print("usowamy kontener sekcja2b")
            sekcja2c.destroy()
            sekcja2c = None

        '''
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
        '''

# Zmienna do przechowywania wybranej wartości - gdzie value to wartość początkowa - może się zmienić podczas pracy z GUI
wybor2 = tk.StringVar(value=podzespoly_dodatkowe)
opcje2 = ["tylko łącznik tyrystorowy i 3 dlawiki", "dodatkowe stopnie"]
i = 5
for opcja2 in opcje2:

    tk.Radiobutton(sekcja2, text=opcja2, variable=wybor2, value=opcja2, command=pokaz_wybor2, bg="grey", font=("Verdana", 11)).grid(row=i , column=0, sticky="w")
    i = i+1

#***********************************************************************************************************************
#BLOK 5
# trzecia częśc przyciskow radiowych - dostepna jezeli wybiorę opcje - dodatkowe stopnie
# Zmienna do przechowywania wybranej wartości - gdzie value to wartość początkowa - może się zmienić podczas pracy z GUI
wybor3 = tk.StringVar(value=zabezpieczenie_lacznika)
opcje3 = ["główne zab. oraz wszystkie podzespoły mają zab.", "główne zab. oraz zabezpieczenia stopni", "brak głównego zab. oraz wszystkie podzespoły mają zab."]
# Przechowywanie dynamicznie tworzonych widgetów
radio_buttons = []
miejsce_podlaczenia_zab = None

#***********************************************************************************************************************
#BLOK 6
#
#miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposub podlaczenia zabezpieczenia lacznika tyrystorowego")
# === SEKCJA 1 === - kontener z niebieskim tłem
sekcja3 = tk.Frame(root, bg="yellow", bd=2, relief="solid", padx=10, pady=10, width =480, height=130)
sekcja3.grid(row=4, column=0)
sekcja3.grid_propagate(False)

opis_dlawiki_lacznik = tk.Label(sekcja3, text="Podaj wartości dławików podpiętych do łącznika tyrystorowego:\n", bg="yellow", font=("Verdana", 10))
opis_dlawiki_lacznik .grid(row=0,column=0, columnspan=3)

#pola do wpisywania wartości dla trzech dławików - tych co są zawsze , podpięte do łącznika tyrystorowego
dlawik1_faza = tk.Label(sekcja3, text="                              L1: ", bg = "yellow")
dlawik1_faza.grid(row=1,column=0, sticky="w")
#dodane aby wyregulowac odstepy
dlawik1_faza_puste = tk.Label(sekcja3, text="                          ", bg = "yellow")
dlawik1_faza_puste.grid(row=1,column=2, sticky="w")
dlawik1 = tk.Entry(sekcja3, width=30)
dlawik1.grid(row=1,column=1, sticky="w")
dlawik2_faza = tk.Label(sekcja3, text="                              L2: ", bg = "yellow")
dlawik2_faza.grid(row=2,column=0, sticky="w")
dlawik2= tk.Entry(sekcja3, width=30)
dlawik2.grid(row=2,column=1, sticky="w")
dlawik3_faza = tk.Label(sekcja3, text="                              L3: " , bg = "yellow")
dlawik3_faza.grid(row=3,column=0, sticky="w")
dlawik3= tk.Entry(sekcja3, width=30)
dlawik3.grid(row=3,column=1, sticky="w")

#***********************************************************************************************************************
#BLOK7
# przeniesione

#***********************************************************************************************************************
#BLOK8
#BLOK - pobierz_dane - tak będę go wewnątrz funkcji opisywał - aby podzielić ją na części

def pobierz_dane():
    global zab_zew, podzespoly_dodatkowe, wybor3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, dodatkowe_stopnie, stopien4, stopien5, stopien6, stopien7, stopien8, stopien9, stopien10, stopien11, stopien12, stopien13, stopien14, stopien15
    global zabezpieczenie_lacznika, gotowe

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
    if sekcja2b:

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
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie_termostat_zabezpieczenie_zew.png")
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
    policz_dodatkowe_stopnie()
    global ilosc_stopni
    if (podzespoly_dodatkowe == "dodatkowe stopnie") and ilosc_stopni > 0 :

        print(f"mamy stopni {ilosc_stopni}")
        print(dodatkowe_stopnie)

        if ilosc_stopni <= 6:

            # ----------------------------------------------------------------------------------------------------------
            # BLOK - pobierz_dane - dodatkowe stopnie -> generowanie grafiki z dodatkowymi stopniami
            if zabezpieczenie_lacznika == "główne zab. oraz zabezpieczenia stopni":
                if zab_zew == "typ S - C 3polowe":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_C_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "wkladki topikowe gG":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_gG_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "brak zabezpieczenia glownego":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_b_podlaczenie_stopnie_zab_na_szystkie_stop/SVC_3_termostat_zew_b_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

            if zabezpieczenie_lacznika == "główne zab. oraz wszystkie podzespoły mają zab.":
                if zab_zew == "typ S - C 3polowe":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab/SVC_3_termostat_zew_C_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "wkladki topikowe gG":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab/SVC_3_termostat_zew_gG_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "brak zabezpieczenia glownego":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab/SVC_3_termostat_zew_b_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

            if zabezpieczenie_lacznika == "brak głównego zab. oraz wszystkie podzespoły mają zab.":
                if zab_zew == "typ S - C 3polowe":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_C_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_C_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "wkladki topikowe gG":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_gG_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_gG_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

                if zab_zew == "brak zabezpieczenia glownego":
                    if ilosc_stopni == 1:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_1stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 2:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_2stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 3:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_3stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 4:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_4stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 5:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_5stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size
                    if ilosc_stopni == 6:
                        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/schematy_brak_lacznik_zab_brak_zab_glow_wew/SVC_3_termostat_zew_b_6stopnie_C_wszystkie_stopnie.png")
                        width_podstawowy, height_podstawowy = schemat_podstawowy.size

            print(f"width_podstawowy = {width_podstawowy}")

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

            # ... dolaczenie grafiki dla trzech dlawikow - podlaczonych do lacznika tyrystorowego
            print("generowanie grafiki dla dlawik D3")
            generuj_grafike_z_tekstem(d3, 1299, 236, 100, nazwa_pliku)
            print("otwarcie grafiki dla dlawika D3")
            opis_stopien_d3 = Image.open(nazwa_pliku).convert("RGBA")
            print("pobranie wymiarow grafiki D3")
            w_o_s_d3, h_o_s_d3 = opis_stopien_d3.size
            print(f"width_podstawowy = {width_podstawowy}")
            print(f"w_o_s_d3 = {w_o_s_d3}")
            punkt_wstawienia = width_podstawowy - w_o_s_d3
            print(f"punkt_wstawienia = {punkt_wstawienia}")
            obraz_do_wygenerowania.paste(opis_stopien_d3,
                                         (width_podstawowy - w_o_s_d3,
                                          height_podstawowy - h_o_s_d3 - h_o_s_d3 - h_o_s_d3))
            # ...
            # ... dolaczenie grafiki dla trzech dlawikow - podlaczonych do lacznika tyrystorowego
            print("generowanie grafiki dla dlawik D2")
            generuj_grafike_z_tekstem(d2, 1299, 236, 100, nazwa_pliku)
            print("otwarcie grafiki dla dlawika D2")
            opis_stopien_d2 = Image.open(nazwa_pliku).convert("RGBA")
            print("pobranie wymiarow grafiki D2")
            w_o_s_d2, h_o_s_d2 = opis_stopien_d2.size
            obraz_do_wygenerowania.paste(opis_stopien_d2,
                                         (width_podstawowy - w_o_s_d3 - w_o_s_d2,
                                          height_podstawowy - h_o_s_d2 - h_o_s_d2 - h_o_s_d2))
            # ...
            # ... dolaczenie grafiki dla trzech dlawikow - podlaczonych do lacznika tyrystorowego
            print("generowanie grafiki dla dlawik D1")
            generuj_grafike_z_tekstem(d1, 1299, 236, 100, nazwa_pliku)
            print("otwarcie grafiki dla dlawika D1")
            opis_stopien_d1 = Image.open(nazwa_pliku).convert("RGBA")
            print("pobranie wymiarow grafiki D1")
            w_o_s_d1, h_o_s_d1 = opis_stopien_d1.size
            obraz_do_wygenerowania.paste(opis_stopien_d1,
                                         (width_podstawowy - w_o_s_d3 - w_o_s_d2 - w_o_s_d1,
                                          height_podstawowy - h_o_s_d1 - h_o_s_d1 - h_o_s_d1))
            # ...

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

                            generuj_grafike_z_tekstem(s4,1299,236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                  (szerokosc_wstawianie_sciezki, height_podstawowy + height_sciezki_stopien_1 + h_s1 + h_o_s1))


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
                            w_o_s2, h_o_s2 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien2, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_2 + h_s2))
                            #...
                            generuj_grafike_z_tekstem(s5, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_1 + h_s2 + h_o_s2))
                            #...

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
                            w_o_s3, h_o_s3 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien3, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_3 + h_s3))

                            # ...
                            generuj_grafike_z_tekstem(s6, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_1 + h_s3 + h_o_s3))
                            # ...

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
                            w_o_s4, h_o_s4 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien4, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_4 + h_s4))
                            # ...
                            generuj_grafike_z_tekstem(s7, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_1 + h_s4 + h_o_s4))
                            # ...

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
                            w_o_s5, h_o_s5 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien5, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_5 + h_s5))

                            # ...
                            generuj_grafike_z_tekstem(s8, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_1 + h_s5 + h_o_s5))
                            # ...

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
                            w_o_s6, h_o_s6 = opis_stopien1.size
                            ilosc_umieszczonych_stopni += 1

                            obraz_do_wygenerowania.paste(opis_stopien1, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_6 + h_s6))

                            # ...
                            generuj_grafike_z_tekstem(s9, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_1 + h_s6 + h_o_s6))
                            # ...

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

                            w_o_s7, h_o_s7 = opis_stopien7.size

                            obraz_do_wygenerowania.paste(opis_stopien7, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_7 + h_s7))

                            # ...
                            generuj_grafike_z_tekstem(s10, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_7 + h_s7 + h_o_s7))
                            # ...

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

                            w_o_s8, h_o_s8 = opis_stopien8.size


                            obraz_do_wygenerowania.paste(opis_stopien8, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_8 + h_s8))

                            # ...
                            generuj_grafike_z_tekstem(s11, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_8 + h_s8 + h_o_s8))
                            # ...

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_8

                        if i == 8:
                            sciezki_stopien_9 = Image.open("pod_3_stopnie_uniwersalny/schematy_dodatkowe_stopnie/podlaczenie_stopnie/podlaczenie_3_fazowe.png")
                            width_sciezki_stopien_9, height_sciezki_stopien_9 = sciezki_stopien_9.size
                            obraz_do_wygenerowania.paste(sciezki_stopien_9,
                                                             (szerokosc_wstawianie_sciezki, height_podstawowy))
                            if zawartosc[0] == "-":
                                print("na schemacie zostanie umiejscowiony dławik jednofazowy")
                                stopien_9 = Image.open(
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

                            w_o_s9, h_o_s9 = opis_stopien9.size


                            obraz_do_wygenerowania.paste(opis_stopien9, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_9 + h_s9))

                            # ...
                            generuj_grafike_z_tekstem(s12, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_9 + h_s9 + h_o_s9))
                            # ...

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

                            w_o_s10, h_o_s10 = opis_stopien10.size

                            obraz_do_wygenerowania.paste(opis_stopien10, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_10 + h_s10))

                            # ...
                            generuj_grafike_z_tekstem(s13, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_10 + h_s10 + h_o_s10))
                            # ...

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

                            w_o_s11, h_o_s11= opis_stopien11.size

                            obraz_do_wygenerowania.paste(opis_stopien11, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_11 + h_s11))

                            # ...
                            generuj_grafike_z_tekstem(s14, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_11 + h_s11 + h_o_s11))
                            # ...

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

                            w_o_s12, h_o_s12 = opis_stopien12.size


                            obraz_do_wygenerowania.paste(opis_stopien12, (szerokosc_wstawianie_sciezki,
                                                                         height_podstawowy + height_sciezki_stopien_12 + h_s12))

                            # ...
                            generuj_grafike_z_tekstem(s15, 1299, 236, 100, nazwa_pliku)
                            opis_moc_stopien = Image.open(nazwa_pliku)
                            obraz_do_wygenerowania.paste(opis_moc_stopien,
                                                         (szerokosc_wstawianie_sciezki,
                                                          height_podstawowy + height_sciezki_stopien_12 + h_s12 + h_o_s12))
                            # ...

                            szerokosc_wstawianie_sciezki = szerokosc_wstawianie_sciezki + width_sciezki_stopien_12

            obraz_do_wygenerowania.save(f"wygenerowany.png")
            ilosc_stopni = 0

            generuj_plik_docx("wygenerowany.png", "schemat.docx")
            konwertuj_docx_na_pdf("schemat.docx")



        #---------------------------------------------------------------------------------------------------------------
        #BLOK - pobierz_dane - dodatkowe stopnie -> nie generujemy schematu , wyswietlamy komunikat
        else :
            messagebox.showinfo("Informacja", "Przekroczono ilosc stopni , aplikacja pozwala na max 6")
            print("przekroczona ilosc stopni")
            print(dodatkowe_stopnie)
            ilosc_stopni = 0

    elif (podzespoly_dodatkowe == "dodatkowe stopnie") and ilosc_stopni == 0:
        messagebox.showinfo("Informacja", "Brak wpisanych dodatkowych stopni")


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

#***********************************************************************************************************************

# BLOK 9 - od przycisków - gorna czesc GUI

def podglad():
    import threading

    popup = show_non_blocking_message(root, "Generowanie png , docx, pdf")

    def watek():
        pobierz_dane()  # to działa w tle
        # po zakończeniu pobierania, zamknij okno z głównego wątku
        root.after(0, lambda: close_message_window(popup))

    threading.Thread(target=watek, daemon=True).start()


obraz_przycisk_generuj = Image.open("grafiki_GUI/strzalka.png")
obraz_przycisk_generuj = obraz_przycisk_generuj.resize((24,24))
ikonka1 = ImageTk.PhotoImage(obraz_przycisk_generuj)


sekcja0 = tk.Frame(root, width =480, height=33)
sekcja0.grid(row=0, column=0)
sekcja0.grid_propagate(False)

generuj_schemat = tk.Button(sekcja0, text="Generuj schemat", compound="left", command=podglad, font=("Helvetica", 8), padx=5, pady=5)
generuj_schemat.grid(row=0, column=0, sticky="w")
tooltip0 = ToolTip(generuj_schemat, "Zostanie wygenerowany schemat na podstawie wybranych opcji.\nMożesz też nacisnąć enter na klawiaturze - aby wygenerować schemat.", delay=1000)

def podglad_obrazu():


    # Ścieżka do pliku .exe, który jest w katalogu projektu (np. w tym samym folderze co skrypt)
    exe_path = os.path.join(os.getcwd(), "podglad_pdf.exe")

    # Otwieramy plik .exe
    os.startfile(exe_path)


podglad = tk.Button(sekcja0, text="Podglad", command=podglad_obrazu, font=("Helvetica", 8), padx=5, pady=5)
podglad.grid(row=0, column=1, sticky="w")
tooltip1 = ToolTip(podglad, "Zostanie otwarty podgląd pliku pdf.\nPodgląd jest odświerzany co 1 sekundę.\nZoom: Kliknij raz na obszar wyświetlanego podglądu,\n"
                            "przyciskając Ctrl + pokrętło na myszce - możesz zmieniać rozmiar wyświetlanej kartki.", delay=1000)
zapisz_grafike = tk.Button(sekcja0, text="Zapisz grafikę", command=lambda: zapisz_plik_do_katalogu("wygenerowany.png"), font=("Helvetica", 8), padx=5, pady=5)
zapisz_grafike.grid(row=0, column=2, sticky="w")
tooltip2 = ToolTip(zapisz_grafike, "Zostanie zapisana ostatnia grafika z schematem.\nZapis jest w formacie png.\nMożesz wybrać lokalizacje zapisu.", delay=1000)
zapisz_docx = tk.Button(sekcja0, text="Zapisz plik WORD", command=lambda: zapisz_plik_do_katalogu("schemat.docx"), font=("Helvetica", 8), padx=5, pady=5)
zapisz_docx.grid(row=0, column=3, sticky="w")
tooltip3 = ToolTip(zapisz_docx, "Zostanie zapisany plik WORD - edytowalny.\nMożesz wybrać lokalizacje zapisu.", delay=1000)
zapisz_pdf = tk.Button(sekcja0, text="Zapisz PDF", command=lambda: zapisz_plik_do_katalogu("schemat.pdf"), font=("Helvetica", 8), padx=5, pady=5)
zapisz_pdf.grid(row=0, column=4, sticky="w")
tooltip4 = ToolTip(zapisz_pdf, "Zostanie zapisany plik PDF.\nMożesz wybrać lokalizacje zapisu.", delay=1000)



root.bind('<Return>', lambda event: pobierz_dane())


# Uruchomienie pętli głównej
root.mainloop()
