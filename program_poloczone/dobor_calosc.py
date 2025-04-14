import tkinter as tk

# Tworzenie głównego okna
root = tk.Tk()
root.title("Puste okno")
root.geometry("400x300")  # Ustawienie rozmiaru okna


nazwa_klienta = tk.Label(text="Nazwa klienta")
nazwa_klienta.grid(row=0, column=0)

nazwa_klienta_entry = tk.Entry(root)
nazwa_klienta_entry.grid(row=1, column=0)

lokalizacja = tk.Label(text = "Lokalizacja")
lokalizacja.grid(row=2, column=0)

lokalizacja_entry = tk.Entry(root)
lokalizacja_entry.grid(row=3,column=0)


# Uruchomienie pętli głównej
root.mainloop()
