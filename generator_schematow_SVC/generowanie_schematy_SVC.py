import tkinter as tk
from PIL import Image

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
dodatkowe_stopnie = ["", "", "", "", "", "", "", "", "", "", "", "", ""]

# Tworzymy główne okno
root = tk.Tk()
root.title("Wybór opcji")

zabezpieczenia_zew = tk.Label(text="Wybierz rodzaj zabezpieczenia zewnetrznego")
zabezpieczenia_zew.grid(row=0, column=0)

# Zmienna do przechowywania wybranej wartości
wybor = tk.StringVar(value="typ S - C 3polowe")  # Domyślnie wybrana opcja

# Funkcja wywoływana po zmianie wyboru
def pokaz_wybor():
    global zab_zew
    print("Wybrano:", wybor.get())
    zab_zew = wybor.get()


# Tworzenie przycisków radiowych
opcje = ["typ S - C 3polowe", "wkladki topikowe gG", "brak zabezpieczenia glownego"]
i = 1
for opcja in opcje:

    tk.Radiobutton(root, text=opcja, variable=wybor, value=opcja, command=pokaz_wybor).grid(row=i , column=0)
    i = i+1

lacznik_tyrystorowy_i_stopnie = tk.Label(text="Ilosc podzespolow")
lacznik_tyrystorowy_i_stopnie.grid(row=4, column=0)

wybor3 = tk.StringVar(value="lacznik i stopnie - wspolne zabezpieczenie")
opcje3 = ["lacznik tyrystorowy ma swoje zabezpieczenie", "lacznik i stopnie - wspolne zabezpieczenie"]
# Przechowywanie dynamicznie tworzonych widgetów
radio_buttons = []
miejsce_podlaczenia_zab = None

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

# Zmienna do przechowywania wybranej wartości
wybor2 = tk.StringVar(value="tylko łącznik tyrystorowy i 3 dlawiki")
opcje2 = ["tylko łącznik tyrystorowy i 3 dlawiki", "dodatkowe stopnie"]
i = 5
for opcja2 in opcje2:

    tk.Radiobutton(root, text=opcja2, variable=wybor2, value=opcja2, command=pokaz_wybor2).grid(row=i , column=0)
    i = i+1

miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposub podlaczenia zabezpieczenia lacznika tyrystorowego")

opis_dlawiki_lacznik = tk.Label(root, text="podaj warosci trzech dlawikow podpietych do lacznika tyrystorowe")
opis_dlawiki_lacznik .grid(row=10,column=0)

dlawik1 = tk.Entry(root, width=30)
dlawik1.grid(row=11,column=0)
dlawik2= tk.Entry(root, width=30)
dlawik2.grid(row=12,column=0)
dlawik3= tk.Entry(root, width=30)
dlawik3.grid(row=13,column=0)

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


def pobierz_dane():
    global zab_zew, podzespoly_dodatkowe, wybor3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, dodatkowe_stopnie
    print(zab_zew)
    print(podzespoly_dodatkowe)
    zabezpieczenie_lacznika=wybor3.get()
    print(zabezpieczenie_lacznika)
    d1 = dlawik1.get()
    print(d1)
    d2 = dlawik2.get()
    print(d2)
    d3 = dlawik3.get()
    print(d3)
    s4 = stopien4.get()
    print(s4)
    dodatkowe_stopnie[0] = s4
    s5 = stopien5.get()
    print(s5)
    dodatkowe_stopnie[1] = s5
    s6 = stopien6.get()
    print(s6)
    dodatkowe_stopnie[2] = s6
    s7 = stopien7.get()
    print(s7)
    dodatkowe_stopnie[3] = s7
    s8 = stopien8.get()
    print(s8)
    dodatkowe_stopnie[4] = s8
    s9 = stopien9.get()
    print(s9)
    dodatkowe_stopnie[5] = s9
    s10 = stopien10.get()
    print(s10)
    dodatkowe_stopnie[6] = s10
    s11 = stopien11.get()
    print(s11)
    dodatkowe_stopnie[7] = s11
    s12 = stopien12.get()
    print(s12)
    dodatkowe_stopnie[8] = s12
    s13 = stopien13.get()
    print(s13)
    dodatkowe_stopnie[9] = s13
    s14 = stopien14.get()
    print(s14)
    dodatkowe_stopnie[10] = s14
    s15 = stopien15.get()
    print(s15)
    dodatkowe_stopnie[11] = s15

    #tu do poprawy 
    # ta czesc odpowiedzialna za schematy z termostatem - badz bez , oraz za schematy bez dodatkowych stopni
    if zab_zew == "typ S - C 3polowe" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")

    if zab_zew == "wkladki topikowe gG" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie_termostat_zabezpieczenie_zew_gG.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")

    if zab_zew == "brak zabezpieczenia glownego" and podzespoly_dodatkowe == "tylko łącznik tyrystorowy i 3 dlawiki":
        schemat_podstawowy = Image.open("pod_3_stopnie_uniwersalny/SVC_3_stopnie_termostat.png")
        width_podstawowy, height_podstawowy = schemat_podstawowy.size
        obraz_do_wygenerowania = Image.new("RGBA", (width_podstawowy, height_podstawowy))
        obraz_do_wygenerowania.paste(schemat_podstawowy,(0,0))
        obraz_do_wygenerowania.save(f"wygenerowany.png")


    # dodatkowe stopnie
    if zab_zew == "typ S - C 3polowe" and podzespoly_dodatkowe == "dodatkowe stopnie":
        global ilosc_stopni
        policz_dodatkowe_stopnie()
        print(f"mamy stopni {ilosc_stopni}")
        print(dodatkowe_stopnie)
        if ilosc_stopni <= 6:
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


            obraz_do_wygenerowania.save(f"wygenerowany.png")
            ilosc_stopni = 0
        else :
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
