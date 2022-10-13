class Line:
    drawn_item = None

    def __init__(self, a_x=None, a_y=None, b_x=None, b_y=None):
        try:
            self.a_x = int(a_x)
            self.a_y = int(a_y)
            self.b_x = int(b_x)
            self.b_y = int(b_y)
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Niepoprawnie podane dane, chcesz spróbować ponownie?"
            )

    def draw(self, canvas):
        self.drawn_item = canvas.create_line(
            self.a_x,
            self.a_y,
            self.b_x,
            self.b_y,
            fill="black",
        )
        canvas.unbind("<Button-1>")

    def change_coordinates(
        self,
        a_x=None,
        a_y=None,
        b_x=None,
        b_y=None,
        canvas=None,
    ):
        try:
            self.a_x = a_x
            self.a_y = a_y
            self.b_x = b_x
            self.b_y = b_y
            canvas.coords(self.drawn_item, a_x, a_y, a_x, a_y)
            canvas.itemconfig(self.drawn_item, fill="black")
            canvas.unbind("<Button-1>")
        except ValueError:
            messagebox.askokcancel(
                "askokcancel", "Nie ma figury do zmian, chcesz spróbować ponownie?"
            )
