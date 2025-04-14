import tkinter as tk
from tkinter import ttk
import math
import csv
import os

zabezpieczenie = 0
zabezpieczenie_gG = 0
kabel_zasilajacy = 0.0
wspolczynik_k = ["1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0"]
lista_dostepne_zab = []
prad_nom_urzadzenia = 0.0
prad_nom_przew = 0.0
dobrane_zabezpieczenie = 0.0
sprawdzenie_obciazalnosc_dlugotrwala = 0.0
warunek = ""
lista_prze_kabl = [2.5,4,6,10,16,25,35,50,70,95,120,150,185,240,300,400,500]
lista_dostepnych_zabezpieczen_z_A_wybrane_przez_szefa = []
lista_zabezpieczen = []



def load_csv_to_list(filename):
    data = []  # Lista, która będzie przechowywać dane z pliku CSV
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)  # Tworzymy obiekt do czytania CSV
            for row in csv_reader:
                data.append(row)  # Dodajemy każdy wiersz do listy
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    return data

def on_select(event):
    global lista_SVG, label_svg, entry_moc_standard, lista_dostepne_zab
    selected_index = combo1.current()  # Uzyskanie indeksu wybranego elementu
    selected_index = int(selected_index)
    print(f"Index wybranego elementu: {selected_index}")

    if(selected_index == 0): #wybrane SVG
        if "entry_moc_standard" in globals():
            entry_moc_standard.grid_forget()
        moc_SVG = ["5kVAr" , "10kVAr", "20kVAr", "30kVAr" , "50kVar","75kVAr","100kVAr"]
        if "wybor_wspolczynik_k" in globals():
            wybor_wspolczynik_k.grid_forget()
        if "linia" in globals():
            linia.grid_forget()
        if "label_obliczenia" in globals():
            label_obliczenia.grid_forget()
        if "entry_moc_standard" in globals():
            entry_moc_standard.grid_forget()
        if "label_z_tabeli_standard" in globals():
            label_z_tabeli_standard.grid_forget()
        if "obliczenia_I_nom_przew" in globals():
            obliczenia_I_nom_przew.grid_forget()
        if "dobrane_zab" in globals():
            dobrane_zab.grid_forget()
        if "rodzaj_dost_zab" in globals():
            rodzaj_dost_zab.grid_forget()
        if "sprawdzenie_warunku" in globals():
            sprawdzenie_warunku.grid_forget()
        lista_dostepne_zab.clear()
        lista_SVG.config(values=moc_SVG)
        lista_SVG.set('')
        lista_SVG.grid(row=2, column=0, columnspan=3)
        lista_SVG.bind("<<ComboboxSelected>>", svg)

    if(selected_index == 1):
        if "label_svg" in globals():
            label_svg.grid_forget()
        if "lista_SVG" in globals():
            lista_SVG.grid_forget()

    if (selected_index == 2):
        if "label_svg" in globals():
            label_svg.grid_forget()
        if "lista_SVG" in globals():
            lista_SVG.grid_forget()
        entry_moc_standard.grid(row=2, column=0, columnspan=3)
        entry_moc_standard.bind("<Return>", standard)  # Wiążemy naciśnięcie Enter z funkcją

def svg(event):
    global label_svg, zabezpieczenie, kabel_zasilajacy
    selected_index = lista_SVG.current()
    selected_index = int(selected_index)
    zabezpieczenie = int(svg_zabezpieczenia[selected_index+1][3])
    kabel_zasilajacy = float(svg_zabezpieczenia[selected_index+1][4])

    label_svg.config(text=f"Dla urzadzen SVG zabezpieczenia oraz kabel zasilajacy\n"
                          f"dobierany jest na podstawie instrukcji producenta\n"
                          f"urzadzenie SVG o mocy : {svg_zabezpieczenia[selected_index+1][0]}\n"
                          f"zabezpieczenie : {zabezpieczenie}\n"
                          f"kabel zasilający: {kabel_zasilajacy}")
    label_svg.grid(row=3, column=0, columnspan=3)


def standard(event):
    global zabezpieczenie, kabel_zasilajacy, entry_moc_standard, label_z_tabeli_standard, label_obliczenia, linia, moc_przekroj_standard, zabezpieczenie, zabezpieczenie_gG
    global wybor_wspolczynik_k, wspolczynik_k, prad_nom_urzadzenia, lista_prze_kabl, wybor_zabezpieczenia_od_szefa, proponowany_przew_kablowy, rodzaj_zabezpieczen_dla_szefa
    global lista_dostepnych_zabezpieczen_z_A_wybrane_przez_szefa
    zawartosc = entry_moc_standard.get()
    print("enter")
    if "wybor_wspolczynik_k" in globals():
        wybor_wspolczynik_k.grid_forget()
    if "linia" in globals():
        linia.grid_forget()
    if "label_obliczenia" in globals():
        label_obliczenia.grid_forget()
    if "label_z_tabeli_standard" in globals():
        label_z_tabeli_standard.grid_forget()
    if "obliczenia_I_nom_przew" in globals():
        obliczenia_I_nom_przew.grid_forget()
    if "dobrane_zab" in globals():
        dobrane_zab.grid_forget()
    if "rodzaj_dost_zab" in globals():
        rodzaj_dost_zab.grid_forget()
    if "sprawdzenie_warunku" in globals():
        sprawdzenie_warunku.grid_forget()


    #wybor_przewodu_kablowego.config(values=)
    print(zawartosc)
    dlugosc_listy = len(moc_przekroj_standard)

    for i in range(dlugosc_listy-1):
        if(float(moc_przekroj_standard[i+1][0])<=float(zawartosc)):
            print(f"jestesmy w przedziale : {moc_przekroj_standard[i+1][0]}")
            kabel_zasilajacy = float(moc_przekroj_standard[i+1][2])
            try:
                zabezpieczenie = int(moc_przekroj_standard[i+1][3])
            except:
                zabezpieczenie = "0"
            zabezpieczenie_gG = int(moc_przekroj_standard[i + 1][4])


    label_z_tabeli_standard.config(text="Z tabeli (ustalone z szefem):\n"
                                        f"Kabel o przekroju: {kabel_zasilajacy} mm2\n"
                                        f"Zabezieczenie główne typu C: {zabezpieczenie}\n"
                                        f"Zabezpieczenie główne typu gG: {zabezpieczenie_gG}")
    label_z_tabeli_standard.grid(row=3, column=0)


    linia.create_line(2, 0, 2, 800, width=2, fill="black")
    linia.grid(row=3, rowspan=7, column=1)

    opis_wybor_przewodu_kablowego.config(text="wybierz przewod kablowy:\n"
                                              "(oto zaproponowany z listy)")
    opis_wybor_przewodu_kablowego.grid(row=4, column=0)

    #tu sa listy do wyboru elementow :
    # sprawdzenie ktory przewod kablowy ma trafic jako wybrany z listy
    index_proponowanego_przew_kablowego = 0
    for i in range(len(lista_prze_kabl)):
        if kabel_zasilajacy == lista_prze_kabl[i]:
            index_proponowanego_przew_kablowego = i
    proponowany_przew_kablowy.set(lista_prze_kabl[index_proponowanego_przew_kablowego])

    wybor_przewodu_kablowego.config(values=lista_prze_kabl , textvariable=proponowany_przew_kablowy)
    wybor_przewodu_kablowego.grid(row=5, column=0)
    #tu przypisanie wartosci do listy z zabezpieczeniami - dla wyboru od szefa

    index_proponowanego_zabezpieczenia = 0
    for i in range(len(zabezpieczenia_C_gG)-1):
        if float(zabezpieczenie) == float(zabezpieczenia_C_gG[i+1][0]):
            index_proponowanego_zabezpieczenia = i
            print("!!!!!!!!!!!!!!!!!!!!!")
        elif float(zabezpieczenie_gG) == float(zabezpieczenia_C_gG[i+1][0]):
            index_proponowanego_zabezpieczenia = i
    proponowane_zabezpieczenie_z_dobrane_przez_szefa.set(lista_zabezpieczen[index_proponowanego_zabezpieczenia])

    opis_zabezpieczenia_od_szefa.config(text="wybierz wielkosc zabezpieczenia:\n"
                                             "(oto zaproponowany z listy)")
    opis_zabezpieczenia_od_szefa.grid(row=6 , column=0)
    wybor_zabezpieczenia_od_szefa.config(values=lista_zabezpieczen , textvariable=proponowane_zabezpieczenie_z_dobrane_przez_szefa)
    wybor_zabezpieczenia_od_szefa.grid(row=7, column=0)
    opis_rodzaj_zabezpieczen_dla_szefa.config(text="Wybierz typ/rodzaj zabezpieczenia:")
    opis_rodzaj_zabezpieczen_dla_szefa.grid(row=8, column=0)
    print(f"index propnowanego zabezpieczenia to  {index_proponowanego_zabezpieczenia}")
    for i in range(4):
        if zabezpieczenia_C_gG[index_proponowanego_zabezpieczenia][i+1] != '':
            lista_dostepnych_zabezpieczen_z_A_wybrane_przez_szefa.append(zabezpieczenia_C_gG[0][i+1])

    rodzaj_zabezpieczen_dla_szefa.config(values=lista_dostepnych_zabezpieczen_z_A_wybrane_przez_szefa)
    rodzaj_zabezpieczen_dla_szefa.grid(row=9, column=0)

    pierwiastek_z_3 = math.sqrt(3)
    zawartosc_razy_1000 =float(zawartosc)*1000
    print(f"zawartosc {zawartosc_razy_1000}")
    mianownik = pierwiastek_z_3*400
    print(mianownik)
    prad_nom_urzadzenia = zawartosc_razy_1000/mianownik
    label_obliczenia.config(text="Z obliczen:\n"
                                 "\n"
                                 f"Moc urzadzenia : Q = {zawartosc} [kVAr]\n"
                                 f"\n"
                                 f"Prąd nominalny urządzenia obliczamy z wzoru :\n"
                                 "\n"
                                 "I(b)=S/(sqrt(3)*400 [A]\n"
                                 "\n"
                                 "gdzie S=sqrt(Q^2+P^2)\n"
                                 "\n"
                                 "podstawienie:\n"
                                 "\n"
                                 f"I(b)={zawartosc_razy_1000}/sqrt(3)*400 [A]\n"
                                 "\n"
                                 f"I(b)={prad_nom_urzadzenia} [A]\n"
                                 "\n"
                                 "wybierz wspolczynik k , gdzie k - 1.3 do 1.5 dlawiki \n"
                                 "k - 1.5 - 2.0 kondensatory ")
    label_obliczenia.grid(row=3, column=2)

    wybor_wspolczynik_k.config(values=wspolczynik_k)
    wybor_wspolczynik_k.grid(row=4, column=2)
    wybor_wspolczynik_k.bind("<<ComboboxSelected>>", obliczenia_po_wspolczyniku)

def obliczenia_po_wspolczyniku(event):
    print(" jest wybrany wsp:")
    global wybor_wspolczynik_k, wspolczynik_k, obliczenia_I_nom_przew, prad_nom_urzadzenia, zabezpieczenia_C_gG, dobrane_zabezpieczenie, dobrane_zab
    global lista_dostepne_zab, rodzaj_dost_zab
    lista_dostepne_zab.clear()
    wybrany_wsp_k= wybor_wspolczynik_k.current()
    wspolczynik_k_float = float(wspolczynik_k[wybrany_wsp_k])
    print(wspolczynik_k[wybrany_wsp_k])
    prad_nom_przew = prad_nom_urzadzenia * wspolczynik_k_float
    print(f"prad nominalny przewodu: {prad_nom_przew}")
    obliczenia_I_nom_przew.config(text="I(nominalne) >= k * I(b)\n"
                                       "podstawienie :\n"
                                       f"I(n) >= {wspolczynik_k_float} * {prad_nom_urzadzenia} [A]\n"
                                       f"I(n) >= {prad_nom_przew} [A]\n"
                                       "\n"
                                       "dostępne zabezpieczenia:\n")
    obliczenia_I_nom_przew.grid(row=5, column=2)
    dlugosc = len(zabezpieczenia_C_gG)
    index = 0
    for i in range(dlugosc-1):
        dobrane_zabezpieczenie = float(zabezpieczenia_C_gG[i+1][0])
        if (prad_nom_przew <= dobrane_zabezpieczenie):
            print(dobrane_zabezpieczenie)
            index = i+1
            break

    dobrane_zab.config(text= f"Zabezpieczenie dobrane z szeregu to : {dobrane_zabezpieczenie} [A]")
    dobrane_zab.grid(row=6, column=2)
    for i in range(5):
        if zabezpieczenia_C_gG[index][i+1] != '':
            lista_dostepne_zab.append(zabezpieczenia_C_gG[0][i+1]+zabezpieczenia_C_gG[index][i+1])
            print(lista_dostepne_zab)
    rodzaj_dost_zab.config(values=lista_dostepne_zab, width=50)
    rodzaj_dost_zab.grid(row=7, column=2)
    rodzaj_dost_zab.bind("<<ComboboxSelected>>", wybrane_zab_z_obliczen)

def wybrane_zab_z_obliczen(event):
    global sprawdzenie_warunku, lista_dostepne_zab, dobrane_zabezpieczenie, warunek
    index_wyb_zab = rodzaj_dost_zab.current()
    wspolczynik_k_dla_zabezpieczen = 0.0
    rodzaj_zab=lista_dostepne_zab[index_wyb_zab]
    rodzaj_zab=rodzaj_zab[15:24]
    if rodzaj_zab[0] == "C":
        wspolczynik_k_dla_zabezpieczen = 1.45

    else:
        print("mamy inne niz C")
        print(f"dobrane zabezpieczenie to:{dobrane_zabezpieczenie}")
        if dobrane_zabezpieczenie <= 4:
            wspolczynik_k_dla_zabezpieczen = 2
        elif dobrane_zabezpieczenie <= 16:
            wspolczynik_k_dla_zabezpieczen = 1.9
        elif dobrane_zabezpieczenie <= 630:
            wspolczynik_k_dla_zabezpieczen = 1.6

    dlugosc = len(przewody_B2)-1
    print(f"dlugosc listy z przewodami : {dlugosc}")
    index_przewod = 0
    for i in range(dlugosc):
        if float(przewody_B2[i+1][1]) >= dobrane_zabezpieczenie:
            przewod_kablowy_prad = przewody_B2[i+1][1]
            index_przewod = i+1
            print(f"index mamy {index_przewod}, a przeowd mamy: {przewod_kablowy_prad}")
            break
    print("break")
    print(f"to co idzie na float to: {przewody_B2[index_przewod][1]}")
    if float(przewody_B2[index_przewod][1]) == float(przewod_kablowy_prad):
        print("dlatego ze zostal wybrany 1.5 na 16 [A]")
        przewod_kablowy_prad = przewody_B2[index_przewod+1][1]
        print(f"kolejny to {przewod_kablowy_prad}")
        index_przewod = index_przewod + 1
        print(f"teraz mamy index {index_przewod}")

    print(f"przewod_kablowy to {przewody_B2[index_przewod][0]} o obciazalnosci {przewod_kablowy_prad} [A]")

    print(f"zabezpieczenie  {rodzaj_zab}, oraz wspolczynik k2 dla zabezpieczen to {wspolczynik_k_dla_zabezpieczen}")

    sprawdzenie_obciazalnosc_dlugotrwala = (float(wspolczynik_k_dla_zabezpieczen)*float(dobrane_zabezpieczenie))/1.45
    print(f"sprawdzenie obciazalnosc dlugotrwala I(z) = {sprawdzenie_obciazalnosc_dlugotrwala}")
    if sprawdzenie_obciazalnosc_dlugotrwala >= dobrane_zabezpieczenie:
        warunek = "Warunek spelniony"
    else :
        warunek = "Warunek niespelniony"

    sprawdzenie_warunku.config(text=f"wybrane zabezpieczenie to : {lista_dostepne_zab[index_wyb_zab]}\n"
                                    "\n"
                                    f"dobrany przewod kablowy to: {przewody_B2[index_przewod][0]} mm2\n"
                                    f"o obciazalnosci dlugotrwalej {przewod_kablowy_prad}\n"
                                    f"nalezy spelnic warunek:\n"
                                    "\n"
                                    "I(b) <= I(n) <= I(z)\n"
                                    "I(z) >= k2*I(n)/1.45\n"
                                    "\n"
                                    f"gdzie: "
                                    f"k2 - wspolczynik dla dobranych zabezpieczen {wspolczynik_k_dla_zabezpieczen}\n"
                                    f"sprawdzenie:\n"
                                    f"I(z) >= {wspolczynik_k_dla_zabezpieczen}*{dobrane_zabezpieczenie}/1.45 [A]\n"
                                    "\n"
                                    f"{prad_nom_urzadzenia} <= {dobrane_zabezpieczenie} <= {przewod_kablowy_prad}\n"
                                    f"I(z) >= {sprawdzenie_obciazalnosc_dlugotrwala}\n"
                                    f"{warunek}\n"
                                    "_________________")
    sprawdzenie_warunku.grid(row=8, column=2)

# Funkcja do uruchamiania programu
def uruchom_program(nazwa_pliku):
    try:
        os.startfile(nazwa_pliku)  # Działa na Windows
    except Exception as e:
        print(f"Błąd: {e}")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.geometry("600x1000")
root.title("dobor przewodu kablowego zasilajacego i zabezpieczen")

# ta zmienna musi byc po root :
proponowany_przew_kablowy = tk.StringVar()
proponowane_zabezpieczenie_z_dobrane_przez_szefa = tk.StringVar()

label_moc = tk.Label(root, text="wybierz typ urzadzenia ( jezeli szef wybrał na etapie-1 to jest automatycznie wybrane )")
label_moc.grid(row=0, column=0, columnspan=3)

lista_SVG = ttk.Combobox(root)
label_svg = tk.Label(root)

urzadzenia = ["SVG" , "SVC" , "STANDARD"]
combo1 = ttk.Combobox(root, values=urzadzenia)
combo1.grid(row=1, column= 0, columnspan=3)
combo1.bind("<<ComboboxSelected>>", on_select)

entry_moc_standard = tk.Entry(root)
#lewa czesc
label_z_tabeli_standard = tk.Label(root)
opis_wybor_przewodu_kablowego = tk.Label(root)
wybor_przewodu_kablowego = ttk.Combobox(root)
opis_zabezpieczenia_od_szefa = tk.Label(root)
wybor_zabezpieczenia_od_szefa = ttk.Combobox(root)
opis_rodzaj_zabezpieczen_dla_szefa = tk.Label(root)
rodzaj_zabezpieczen_dla_szefa = ttk.Combobox(root)
#srodek
linia = tk.Canvas(root, width=2, height=800)
# prawa czesc
label_obliczenia = tk.Label(root)
wybor_wspolczynik_k = ttk.Combobox(root)
obliczenia_I_nom_przew = tk.Label(root)
dobrane_zab = tk.Label(root)
rodzaj_dost_zab = ttk.Combobox(root)
sprawdzenie_warunku = tk.Label(root)

#pobranie danych o SVG do listy
svg_zabezpieczenia = load_csv_to_list('zabezpieczeniaSVGgG[1].csv')
moc_przekroj_standard = load_csv_to_list('moc_przekroj.csv')
zabezpieczenia_C_gG = load_csv_to_list('zabezpieczenia_C_gG.csv')
dlugosc_listy_z_zabezpieczeniami = len(zabezpieczenia_C_gG)-1
for i in range(dlugosc_listy_z_zabezpieczeniami):
    lista_zabezpieczen.append(zabezpieczenia_C_gG[i+1][0])
przewody_B2 = load_csv_to_list('przewody_miedziane_B2.csv')

"""
#lista dostepnych zabezpieczen :
dlugosc_listy_z_zabezpieczeniami = len(zabezpieczenia_C_gG)-1
for i in range(dlugosc_listy_z_zabezpieczeniami):
    if zabezpieczenia_C_gG[i+1][1] != "":
        lista_zabezpieczen.append("S ----- C"+zabezpieczenia_C_gG[i+1][1]+" A")
    if zabezpieczenia_C_gG[i + 1][2] != "":
        lista_zabezpieczen.append("gG NH00 "+zabezpieczenia_C_gG[i + 1][2]+" A")
    if zabezpieczenia_C_gG[i + 1][3] != "":
        lista_zabezpieczen.append("gG NH1  "+zabezpieczenia_C_gG[i + 1][3]+ " A")
    if zabezpieczenia_C_gG[i + 1][4] != "":
        lista_zabezpieczen.append("gG NH2  "+zabezpieczenia_C_gG[i + 1][4]+" A")
    if zabezpieczenia_C_gG[i + 1][5] != "":
        lista_zabezpieczen.append("gG NH3  "+zabezpieczenia_C_gG[i + 1][5]+ " A")

print(lista_zabezpieczen)
"""
#przyciski
przycisk1 = tk.Button(root, text="Dobrane Szef", command=lambda: uruchom_program("moc_przekroj.csv"))
przycisk1.grid(row=1, column=3)

przycisk2 = tk.Button(root, text="Dostepne zabezpieczenia", command=lambda: uruchom_program("zabezpieczenia_C_gG.csv"))
przycisk2.grid(row=2, column=3)

przycisk3 = tk.Button(root, text="Przewody_miedziane_B2", command=lambda: uruchom_program("przewody_miedziane_B2.csv"))
przycisk3.grid(row=3, column=3)

przycisk4 = tk.Button(root, text="zabezpieczenia SVG", command=lambda: uruchom_program("zabezpieczeniaSVGgG[1].csv"))
przycisk4.grid(row=4, column=3)

# Uruchomienie aplikacji
root.mainloop()