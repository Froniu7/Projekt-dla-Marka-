import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import argparse

import sys
import os

if getattr(sys, 'frozen', False):
    # Program uruchomiony jako .exe
    current_dir = os.path.dirname(sys.executable)
else:
    # Program uruchomiony jako .py
    current_dir = os.path.dirname(os.path.abspath(__file__))

#TEMP_PDF = os.path.join(current_dir, "schemat.pdf")
TEMP_PDF = ""


scale = 0.3
modyfikacja_scale = False
jest_schemat = 0
pierwsze_otwarcie = 0
data_utworzenia = 0

class PDFViewer:
    def __init__(self, master, pdf_path):
        global TEMP_PDF
        TEMP_PDF = pdf_path
        self.master = master
        self.window = master
        self.window.title("Podgląd PDF (wszystkie strony)")

        # Kontener z przewijanym płótnem
        self.canvas = tk.Canvas(self.window, bg="white")
        self.scroll_y = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(self.window, orient="horizontal", command=self.canvas.xview)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.last_mtime = 0
        self.images = []  # przechowuje PhotoImage, by nie zostały usunięte przez GC

        self.update_pdf()
        self.schedule_refresh()
        # Obsługa przewijania kółkiem myszy
        #self.canvas.bind_all("<Control-MouseWheel>", self._on_ctrl_mousewheel)
        self.window.bind_all("<MouseWheel>", self._on_mousewheel)


        self.page_widgets = []
        self.window.bind("<Configure>", lambda e: self.relayout_pages())
        self.ctrl_pressed = False
        self.window.bind_all("<Control_L>", self._ctrl_down)
        self.window.bind_all("<KeyRelease-Control_L>", self._ctrl_up)
        self.window.bind_all("<Control_R>", self._ctrl_down)
        self.window.bind_all("<KeyRelease-Control_R>", self._ctrl_up)

    def update_pdf(self):
        global modyfikacja_scale, TEMP_PDF, scale



        try:
            print("otwieramy pdf")
            doc = fitz.open(TEMP_PDF)
            self.images.clear()
            for widget in self.frame.winfo_children():
                widget.destroy()

            self.page_widgets = []

            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                new_width = max(1, int(img.width * scale))
                new_height = max(1, int(img.height * scale))
                img = img.resize((new_width, new_height), Image.LANCZOS)

                tk_img = ImageTk.PhotoImage(img)
                self.images.append(tk_img)

                border_frame = tk.Frame(self.frame, bg="#999", padx=2, pady=2)
                label = tk.Label(border_frame, image=tk_img, bg="white", bd=2, relief="solid")
                label.pack()

                self.page_widgets.append(border_frame)

            doc.close()
            print("start funkcji reload_pages")
            self.relayout_pages()

        except Exception as e:
            print(f"Błąd podczas ładowania PDF: {e}")

        modyfikacja_scale = False

    def relayout_pages(self):
        if not self.page_widgets:
            print("return bo nie zostaly zaladowane strony pdf ")
            return

        # Oblicz dostępną szerokość ramki
        frame_width = self.canvas.winfo_width()
        if frame_width <= 1:  # za wcześnie po starcie
            self.master.after(100, self.relayout_pages)
            print("return")
            return

        # Zakładamy, że wszystkie strony mają ten sam rozmiar
        example = self.page_widgets[0]
        example.update_idletasks()
        page_width = example.winfo_width() + 30  # margines

        cols = max(1, frame_width // page_width)

        for idx, widget in enumerate(self.page_widgets):
            row = idx // cols
            col = idx % cols
            widget.grid(row=row, column=col, padx=10, pady=10)


    def schedule_refresh(self):
        global modyfikacja_scale, data_utworzenia, pierwsze_otwarcie
        print(f"wartosci zmiennych data_utworzenia : {data_utworzenia}")

        if data_utworzenia != pobierz_date_modyfikacji(TEMP_PDF):
            print("data utworzenia się zmieniła")
            data_utworzenia = pobierz_date_modyfikacji(TEMP_PDF)
            print(f"nowa data utworzenia : {data_utworzenia}")
            self.update_pdf()
            self.master.after(1000, self.schedule_refresh)
        if jest_schemat == 1 and pierwsze_otwarcie == 0:
            print("otwieramy bo - nowy schemat")
            pierwsze_otwarcie = 1
            self.master.after(100, self.update_pdf)
            self.master.after(200, self.update_pdf)
            self.master.after(1000, self.schedule_refresh)
        else:
            print("nic nie robimy")
            self.master.after(1000, self.schedule_refresh)
        '''
        try:
            if os.path.exists(TEMP_PDF):
                mtime = os.path.getmtime(TEMP_PDF)
                if mtime != self.last_mtime or modyfikacja_scale:
                    print("➡️ Zmiana wykryta – odświeżam PDF")
                    self.update_pdf()
                    self.last_mtime = mtime
                    modyfikacja_scale = False
                else:
                    print("⏸️ Brak zmian – nie odświeżam")
        except Exception as e:
            print(f"Błąd podczas sprawdzania zmian w pliku: {e}")

        self.master.after(1000, self.schedule_refresh)
        '''

    def _on_mousewheel(self, event):
        global scale, modyfikacja_scale
        if self.ctrl_pressed:
            delta = 0.05 if event.delta > 0 else -0.05
            direction = "up" if event.delta > 0 else "down"
            print(f"Wciśnięto Ctrl + myszka {direction}")
            new_scale = scale + delta
            print(f"nowa skala to: {new_scale}")
            if 0.1 <= new_scale <= 2.0:
                print("odpalamy funkcje")
                scale = new_scale
                modyfikacja_scale = True
                self.update_pdf()
                self.relayout_pages()
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _ctrl_down(self, event):
        self.ctrl_pressed = True

    def _ctrl_up(self, event):
        self.ctrl_pressed = False


import argparse
import os
import tkinter as tk

def main():
    global jest_schemat, TEMP_PDF, data_utworzenia

    parser = argparse.ArgumentParser(description="Podgląd PDF z argumentami.")
    parser.add_argument("--sciezka", type=str, help="Pełna ścieżka do pliku PDF", required=True)
    parser.add_argument("--schemat_ready", type=int, help="Flaga informująca czy schemat gotowy (1 = tak)", default=0)

    args = parser.parse_args()

    if args.schemat_ready == 1:
        print("Schemat gotowy, uruchamiamy tryb podglądu.")
        jest_schemat = args.schemat_ready

    TEMP_PDF = args.sciezka

    # Weryfikacja, czy plik istnieje
    if not os.path.isfile(TEMP_PDF):
        print(f"❌ Plik nie istnieje: {TEMP_PDF}")
        exit(1)

    print(f"✅ Plik do podglądu: {TEMP_PDF}")
    data_utworzenia = pobierz_date_modyfikacji(TEMP_PDF)


    root = tk.Tk()
    root.geometry("800x600+491+5")

    PDFViewer(root, TEMP_PDF)  # Zakładamy, że funkcja przyjmuje ścieżkę

    root.mainloop()

import os
import platform
import datetime


def pobierz_date_modyfikacji(sciezka):
    if not os.path.exists(sciezka):
        raise FileNotFoundError(f"Plik nie istnieje: {sciezka}")

    timestamp = os.path.getmtime(sciezka)
    return datetime.datetime.fromtimestamp(timestamp)



if __name__ == "__main__":
    main()
