import tkinter as tk
from tkinter import messagebox
import csv

def generate_csv():
    filename = filename_entry.get().strip()
    if not filename:
        messagebox.showerror("Błąd", "Nazwa pliku nie może być pusta.")
        return

    # Pobranie danych z pól
    data = []
    try:
        for row_frame in rows:
            row = [entry.get().strip() for entry in row_frame]
            data.append(row)
    except ValueError:
        messagebox.showerror("Błąd", "Wszystkie pola muszą zawierać liczby, być puste lub zawierać znak minus.")
        return

    filename_with_extension = f"{filename}.csv"
    try:
        with open(filename_with_extension, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(data)
        messagebox.showinfo("Sukces", f"Plik {filename_with_extension} został wygenerowany.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")

# Tworzenie głównego okna
root = tk.Tk()
root.title("Generator CSV")

# Siatka pól wejściowych
rows = []
for i in range(3):  # 3 wiersze
    row_frame = []
    for j in range(18):  # 18 kolumn
        entry = tk.Entry(root, width=10, justify='center')
        entry.grid(row=i, column=j, padx=2, pady=2)
        row_frame.append(entry)
    rows.append(row_frame)

# Pole na nazwę pliku
filename_label = tk.Label(root, text="Nazwa pliku:")
filename_label.grid(row=3, column=0, columnspan=9, pady=10, sticky='e')
filename_entry = tk.Entry(root, width=20)
filename_entry.grid(row=3, column=9, columnspan=9, pady=10, sticky='w')

# Przycisk generowania pliku CSV
generate_button = tk.Button(root, text="Generuj CSV", command=generate_csv)
generate_button.grid(row=4, column=0, columnspan=18, pady=20)

root.mainloop()