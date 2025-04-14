import tkinter as tk

# Tworzymy główne okno
root = tk.Tk()
root.title("Wybór opcji")

zabezpieczenia_zew = tk.Label(text="Wybierz rodzaj zabezpieczenia zewnetrznego")
zabezpieczenia_zew.grid(row=0, column=0)

# Zmienna do przechowywania wybranej wartości
wybor = tk.StringVar(value="typ S - C 3polowe")  # Domyślnie wybrana opcja

# Funkcja wywoływana po zmianie wyboru
def pokaz_wybor():
    print("Wybrano:", wybor.get())

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
    global miejsce_podlaczenia_zab, radio_buttons

    print("Wybrano:", wybor2.get())

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
        miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposób podłączenia zabezpieczenia łącznika tyrystorowego")
        miejsce_podlaczenia_zab.grid(row=7, column=0)

        for i, opcja in enumerate(opcje3):
            rb = tk.Radiobutton(root, text=opcja, variable=wybor3, value=opcja)
            rb.grid(row=i+8, column=0)
            radio_buttons.append(rb)  # Przechowujemy referencję do przycisku

# Zmienna do przechowywania wybranej wartości
wybor2 = tk.StringVar(value="tylko łącznik tyrystorowy i 3 dlawiki")
opcje2 = ["tylko łącznik tyrystorowy i 3 dlawiki", "dodatkowe stopnie"]
i = 5
for opcja2 in opcje2:

    tk.Radiobutton(root, text=opcja2, variable=wybor2, value=opcja2, command=pokaz_wybor2).grid(row=i , column=0)
    i = i+1

miejsce_podlaczenia_zab = tk.Label(text="Wybierz sposub podlaczenia zabezpieczenia lacznika tyrystorowego")







# Uruchomienie pętli głównej
root.mainloop()
