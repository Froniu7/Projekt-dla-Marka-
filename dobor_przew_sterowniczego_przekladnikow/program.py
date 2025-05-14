import tkinter as tk
from tkinter import ttk
import csv
import random

#zmienne
przekladnia = 0.0
VA = 0.0
przekroj = 0.0
dlugos_przewodu = 0.0
moc_w_sieci = 0.0
prad = 0.0
wybrany_przekladnik_szef = ""

def spelnienie_warunku():
    global przekladnia, VA, dlugos_przewodu, przekroj, prad
    if (przekladnia != 0.0 and VA != 0.0 and dlugos_przewodu != 0.0 and przekroj != 0.0):
        print("")
        print("Spelnienie warunku dla max pradu na uzwojeniu wtornym przekladnika:")


        #wyciagam przkladnie
        dlugosc_ciagu_znakow = len(przekladnia)
        uzwojenie_wtorne = int(przekladnia[dlugosc_ciagu_znakow-1])
        wartosc_z_uzwojenie_wtorne = int(uzwojenie_wtorne)
        #wyciagam przekroj kabla
        dlugosc_ciagu_znakow = len(przekroj)

        print("Przekroje przewodów sterujacych do przekladnika dobieramy za pomoca wzoru:")
        print("P = I*I*2L / qCu*56 [VA]")
        print("gdzie :")
        print("P - straty mocy na przewodzie miedzianym")
        print(f"I - max prad na uzwojeniu wtornym : {uzwojenie_wtorne} [A]")
        print(f"L - dlugosc przewodu : {dlugos_przewodu} [m]")
        przekroj_float= float(przekroj[2: dlugosc_ciagu_znakow-3])
        print(f"qCu - przekroj zyly przewodu Cu : {przekroj_float} [mm2]")
        Cu=56
        P = (wartosc_z_uzwojenie_wtorne*wartosc_z_uzwojenie_wtorne*2*dlugos_przewodu)/(przekroj_float*Cu)
        print(f"Obliczenia :")
        print(f"P= {uzwojenie_wtorne}*{uzwojenie_wtorne}*2{dlugos_przewodu} / {przekroj_float}*{Cu} [VA]")

        print(f"moc wydzielona na przewodzie kablowym P= {P} [VA]")
        if (float(VA) >= P):
            print("P(przekladnika)>P(przewod kablowy)")
            print("warunek spelniony")
            print("_________________")

        elif (float(VA) == P):
            print("P(przekladnika)=P(przewod kablowy)")
            print("warunek spelniony")
            print("_________________")

        else:
            print("P(przekladnika)<P(przewod kablowy)")
            print("warunek nie spelniony")
            print("")

    if (przekladnia != 0.0 and VA != 0.0 and dlugos_przewodu != 0.0 and przekroj != 0.0 and prad != 0.0):
        print("")
        print("Spelnienie warunku dla mocy wystepujacej w sieci : ")
        print("Przekroje przewodów sterujacych do przekladnika dobieramy za pomoca wzoru:")
        print("P = I*I*2L / qCu*56 [VA]")
        print("gdzie :")
        print("P - straty mocy na przewodzie miedzianym")

        #wyciagam przkladnie
        dlugosc_ciagu_znakow = len(przekladnia)
        uzwojenie_wtorne = int(przekladnia[dlugosc_ciagu_znakow-1])

        #print(f"wartosc na uzwojeniu wtornym to : {uzwojenie_wtorne}")
        uzwojenie_pierwotne = int(przekladnia[0:dlugosc_ciagu_znakow-2])
        #print(f"wartosc na uzwojeniu pierwitnym pradu to {uzwojenie_pierwotne}")

        przeklania_rzeczywista = int(uzwojenie_pierwotne/uzwojenie_wtorne)
        #print(f"rzeczywista przekladnia to : {przeklania_rzeczywista}")
        prad_max_na_wtornym = prad/przeklania_rzeczywista

        print(f"I - max prad na uzwojeniu wtornym : {prad_max_na_wtornym} [A],")
        print("    prad na uzwojeniu wtornym zostal policzony na podstawie danych z faktur.")
        print(f"L - dlugosc przewodu : {dlugos_przewodu} [m]")
        wartosc_z_uzwojenie_wtorne = int(uzwojenie_wtorne)
        #wyciagam przekroj kabla
        dlugosc_ciagu_znakow = len(przekroj)
        #print(f"dlugosc ciagu znakow dla przewodu kablowego to : {dlugosc_ciagu_znakow}")
        #print(f"przekroj {przekroj}")
        przekroj_float= float(przekroj[2: dlugosc_ciagu_znakow-3])
        print(f"qCu - przekroj zyly przewodu Cu : {przekroj_float} [mm2]")
        Cu=56
        P = (prad_max_na_wtornym*prad_max_na_wtornym*2*dlugos_przewodu)/(przekroj_float*Cu)
        print(f"Obliczenia :")
        print(f"P= {uzwojenie_wtorne}*{uzwojenie_wtorne}*2{dlugos_przewodu} / {przekroj_float}*{Cu} [VA]")
        print(f"moc wydzielona na przewodzie kablowym: {P} [VA]")
        if (float(VA) >= P):
            print("P(przekladnika)>P(przewod kablowy)")
            print("warunek spelniony")
            print("_________________")

        elif (float(VA) == P):
            print("P(przekladnika)=P(przewod kablowy)")
            print("warunek spelniony")
            print("_________________")
        else:
            print("warunek nie spelniony")
            print("")

# Wczytanie danych z pliku CSV
def load_data_from_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Aktualizacja zmiennych po wyborze elementu
def on_select(event):
    selected_index = combo1.current()  # Uzyskanie indeksu wybranego elementu
    #print(f"Index wybranego elementu: {selected_index}")
    # Zapisz indeks do zmiennej
    label_result.config(text=f"Wybrany element: {data[selected_index]}")
    pobieranie_wiersza_przekladniki("dane.csv", selected_index)
    spelnienie_warunku()

def on_select2(event):
    selected_index = combo2.current()  # Uzyskanie indeksu wybranego elementu
    #print(f"Index wybranego elementu dla przewody: {selected_index}")
    # Zapisz indeks do zmiennej
    label_result2.config(text=f"Wybrany element: {przewody[selected_index]}")
    pobieranie_wiersza_przewody("przewody.csv", selected_index)
    spelnienie_warunku()

def on_entry_change(event):
    global dlugos_przewodu
    wpisana_wartosc = entry.get()
    try:
        dlugos_przewodu = float(wpisana_wartosc)
        print(f"dlugosc przewodu kablowego to : {wpisana_wartosc}")
        spelnienie_warunku()
    except:
        print(f"dlugosc przewodu kablowego to, podaj wartosc typu float (czesc ulamkowa oddzielona kropka) : {wpisana_wartosc}")

def obliczenie_pradu_na_fazie(event):
    global moc_w_sieci, prad, przekladnia
    wpisana_wartosc = entry_moc.get()
    try:
        moc_w_sieci = float(wpisana_wartosc)
        print(f"moc w sieci to : {wpisana_wartosc}")
        prad = ((moc_w_sieci*1000)/3)/230
        print(f"prad na fazie to : {prad} [A]")
        label_prad.config(text=f"wartosc pradu na faze to : {prad} [A]")
        if (przekladnia != 0.0):
            pass
        print("")
    except:
        print(f"dlugosc przewodu kablowego to, podaj wartosc typu float (czesc ulamkowa oddzielona kropka) : {wpisana_wartosc}")

def pobieranie_wiersza_przekladniki(file_path, index_wiersza):
    global przekladnia, VA
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))  # Konwersja czytnika CSV na listę
        if 0 <= index_wiersza < len(reader):  # Sprawdzenie, czy indeks jest w zakresie
            przekladnia = reader[index_wiersza][1]
            print(f"przekladnia : {przekladnia}")
            VA = reader[index_wiersza][2]
            print(f"VA : {VA}")
            okno = reader[index_wiersza][3]
            print(f"okno : {okno} mm")
        else:
            print("Błąd: Indeks poza zakresem!")

def pobieranie_wiersza_przewody(file_path, index_wiersza):
    global przekroj
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))  # Konwersja czytnika CSV na listę
        if 0 <= index_wiersza < len(reader):  # Sprawdzenie, czy indeks jest w zakresie
            przekroj = reader[index_wiersza][1]
            print(f"przekroj wynosi : {przekroj}")
        else:
            print("Błąd: Indeks poza zakresem!")


def wygenerowanie_przekladnik(data):
    global wybrany_przekladnik_szef
    liczba = random.randint(1, 5)
    wybrany_przekladnik_szef = data[liczba][1]
    print(f"Symulacja sytuacji gdy mamy juz dobor - etap pierwszy")
    print(f"przekladnik wybrany przez Szefa to: {wybrany_przekladnik_szef}")
    print("")

# Ścieżka do pliku CSV
csv_file = "dane.csv"
data = load_data_from_csv(csv_file)
przewody_plik = "przewody.csv"
przewody = load_data_from_csv(przewody_plik)
wygenerowanie_przekladnik(data)

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.geometry("400x300")
root.title("Wybór przekładnika")

# Podaj wartosc mocy zamowionej
label_moc = tk.Label(root, text="Podaj wartosc mocy wystepujacej w sieci:\n (możesz podac wartosc zamowioną bądz wartosc max wystepującą))")
label_moc.grid(row=0, column=0)
entry_moc = tk.Entry(root)
entry_moc.grid(row=1, column=0)
entry_moc.bind("<KeyRelease>", obliczenie_pradu_na_fazie)  # Automatyczne wywołanie po każdej zmianie

label_prad = tk.Label(root, text="")
label_prad.grid(row=2, column=0)

# Etykieta instrukcyjna
label = tk.Label(root, text="Wybierz przekładnik:")
label.grid(row=3, column= 0)

# Lista rozwijana- po wybraniu elementu z listry zoistanie wywyłana funkcja on_select
combo1 = ttk.Combobox(root, values=data)
combo1.grid(row=4, column= 0)
combo1.bind("<<ComboboxSelected>>", on_select)

# Etykieta do wyświetlania wyników
label_result = tk.Label(root, text="")
label_result.grid(row=5, column=0)

# Etykieta instrukcyjna
label = tk.Label(root, text="Wybierz przewod:")
label.grid(row=6, column= 0)

# Lista rozwijana- po wybraniu elementu z listry zoistanie wywyłana funkcja on_select
combo2 = ttk.Combobox(root, values=przewody)
combo2.grid(row=7, column= 0)
combo2.bind("<<ComboboxSelected>>", on_select2)

# Etykieta do wyświetlania wyników
label_result2 = tk.Label(root, text="")
label_result2.grid(row=8, column=0)

# Etykieta do wyświetlania wyników
label_result2 = tk.Label(root, text="Podaj dlugosc przewodu kablwego ( zmienna typu float ):")
label_result2.grid(row=9, column=0)
# Pole tekstowe z automatycznym wywołaniem funkcji
entry = tk.Entry(root)
entry.grid(row=10, column=0)
entry.bind("<KeyRelease>", on_entry_change)  # Automatyczne wywołanie po każdej zmianie

# Uruchomienie aplikacji
root.mainloop()