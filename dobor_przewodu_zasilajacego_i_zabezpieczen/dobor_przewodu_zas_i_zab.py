import tkinter as tk
from tkinter import ttk

def on_select(event):
    global lista_SVG
    selected_index = combo1.current()  # Uzyskanie indeksu wybranego elementu
    selected_index = int(selected_index)
    print(f"Index wybranego elementu: {selected_index}")

    if(selected_index == 0): #wybrane SVG
        moc_SVG = ["5kVAr" , "10kVAr", "20kVAr", "30kVAr" , "50kVar"]
        lista_SVG = ttk.Combobox(root, values=moc_SVG)
        lista_SVG.grid(row=2, column=0)
        lista_SVG.bind("<<ComboboxSelected>>", svg)

def svg(event):
    selected_index = lista_SVG.current()
    selected_index = int(selected_index)
    if (selected_index == 0):
        label_svg = tk.Label(root,
                         text=f"Na podstawie tabeli będą zabezpieczenia C")
        label_svg.grid(row=3, column=0)



# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.geometry("600x300")
root.title("dobor przewodu kablowego zasilajacego i zabezpieczen")

label_moc = tk.Label(root, text="wybierz typ urzadzenia ( jezeli szef wybrał na etapie-1 to jest automatycznie wybrane )")
label_moc.grid(row=0, column=0)

urzadzenia = ["SVG" , "SVC" , "STANDARD"]
combo1 = ttk.Combobox(root, values=urzadzenia)
combo1.grid(row=1, column= 0)
combo1.bind("<<ComboboxSelected>>", on_select)






# Uruchomienie aplikacji
root.mainloop()