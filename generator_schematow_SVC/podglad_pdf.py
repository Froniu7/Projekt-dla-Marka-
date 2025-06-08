import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import fitz  # PyMuPDF

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    current_dir = os.getcwd()

TEMP_PDF = os.path.join(current_dir, "schemat.pdf")

scale = 0.3
modyfikacja_scale = False

class PDFViewer:
    def __init__(self, master):
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
        global modyfikacja_scale, TEMP_PDF

        print(TEMP_PDF)
        print("Start update pdf")
        if not os.path.exists(TEMP_PDF):
            print("nie znaleziono pliku pdf")
            return
        else:
            print("znaleziono plik pdf")

        mtime = os.path.getmtime(TEMP_PDF)
        if (mtime == self.last_mtime) and (modyfikacja_scale==False):
            print("nie nastapiła zmiana")
            return  # brak zmian

        self.last_mtime = mtime

        try:
            print("otwieramy pdf")
            doc = fitz.open(TEMP_PDF)
            self.images.clear()
            for widget in self.frame.winfo_children():
                widget.destroy()

            self.page_widgets = []  # Przechowujemy ramki do ponownego ułożenia

            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Skala
                global scale
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

            self.relayout_pages()  # Ułóż je zgodnie z aktualną szerokością

        except Exception as e:
            print(f"Błąd podczas ładowania PDF: {e}")

        modyfikacja_scale = False

    def relayout_pages(self):
        if not self.page_widgets:
            return

        # Oblicz dostępną szerokość ramki
        frame_width = self.canvas.winfo_width()
        if frame_width <= 1:  # za wcześnie po starcie
            self.master.after(100, self.relayout_pages)
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
        self.update_pdf()
        self.master.after(1000, self.schedule_refresh)

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


def main():
    root = tk.Tk()

    # Ustawienie geometrii okna (szerokość 800px, wysokość 600px, pozycja na ekranie 10px od lewej i 10px od góry)
    root.geometry("800x600+491+5")

    # Otwórz przeglądarkę PDF
    PDFViewer(root)  # Funkcja otwierająca podgląd PDF

    # Rozpocznij pętlę aplikacji
    root.mainloop()

if __name__ == "__main__":
    main()
