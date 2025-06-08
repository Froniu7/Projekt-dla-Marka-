import tkinter as tk
class ToolTip:

    def __init__(self, widget, text, delay=1000):
        self.widget = widget
        self.text = text
        self.delay = delay  # opóźnienie w ms
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hide_tip)

    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=5, ipady=2)

    def hide_tip(self, event=None):
        self.unschedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
