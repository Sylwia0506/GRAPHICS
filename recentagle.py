from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


class Rectangle:
    drawn_item = None

    def __init__(
        self, a_x=None, a_y=None, d_x=None, d_y=None
    ):
        try:
            self.a_x = int(a_x)
            self.a_y = int(a_y)
            self.d_x = int(d_x)
            self.d_y = int(d_y)
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Niepoprawnie podane dane, chcesz spróbować ponownie?"
            )

    def draw(self, canvas):
        self.drawn_item = canvas.create_rectangle(
            self.a_x, self.a_y, self.d_x, self.d_y
        )
        canvas.unbind("<Button-1>")

    def change_coordinates(self , a_x=None , a_y=None , d_x=None , d_y=None , canvas=None):
        try:
            self.a_x = a_x
            self.a_y = a_y
            self.d_x = d_x
            self.d_y = d_y
            canvas.coords(self.drawn_item , a_x , a_y , d_x , d_y)
            canvas.itemconfig(self.drawn_item , outline='black')
            canvas.unbind("<Button-1>")
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Nie ma figury do zmian, chcesz spróbować ponownie?"
            )
