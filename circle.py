class Circle:
    drawn_item = None

    def __init__(self, a_x=None, a_y=None, r=None):
        try:
            self.a_x = int(a_x)
            self.a_y = int(a_y)
            self.r = int(r)
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Niepoprawnie podane dane, chcesz spróbować ponownie?"
            )

    def draw(self, canvas):
        self.drawn_item = canvas.create_oval(
            self.a_x - self.r, self.a_y - self.r, self.a_x + self.r, self.a_y + self.r
        )
        canvas.unbind("<Button-1>")

    def change_coordinates(self, a_x=None, a_y=None, r=None, canvas=None):
        try:
            self.a_x = a_x
            self.a_y = a_y
            self.r = r
            canvas.coords(
                self.drawn_item,
                self.a_x - self.r,
                self.a_y - self.r,
                self.a_x + self.r,
                self.a_y + self.r,
            )
            canvas.itemconfig(self.drawn_item, outline="black")
            canvas.unbind("<Button-1>")
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Nie ma figury do zmian, chcesz spróbować ponownie?"
            )
