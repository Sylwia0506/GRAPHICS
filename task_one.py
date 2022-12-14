import math
from tkinter import *
from tkinter import messagebox
from scipy.spatial import distance

from circle import Circle
from line import Line
from recentagle import Rectangle
from tkinter.ttk import *
from tkinter import filedialog as fd
import tkinter.colorchooser as cch

from PIL import Image, ImageTk


def open_file():
    filename = fd.askopenfilename()
    img = Image.open(filename)
    test = ImageTk.PhotoImage(img)

    label1 = Label(image=test)
    label1.image = test

    label1.place(x=300, y=78)


def save_file():
    files = [
        ("All Files", "*.*"),
    ]
    file = fd.asksaveasfile(filetypes=files, defaultextension=files)


class Menu:
    root = Tk()

    w = Canvas(root, width=600, height=500, background="white")
    w.create_text(300 , 50 , text="Grafika komputerowa" , fill="black" , font=('Helvetica 15 bold'))
    menu = Menu(root)
    submenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Plik", menu=submenu)

    submenu.add_command(label="Otwórz", command=open_file)
    submenu.add_command(label="Zapisz", command=save_file)

    root.config(menu=menu, width=50, height=30)

    mode = "none"
    mouse_line_start = None
    mouse_line_end = None

    mouse_rectangle_a = None
    mouse_rectangle_d = None

    mouse_circle_a = None
    mouse_circle_r = None

    mouse_move_selected_object = None
    mouse_move_selected_end_position = None

    lines = []
    rectangles = []
    circles = []

    def __init__(self):

        maincolor = "yellow"
        self.root.configure(bg=maincolor)
        style = Style()
        style.configure("TButton", font=("calibri", 10, "bold"), borderwidth="4")
        style.map(
            "TButton",
            foreground=[("active", "!disabled", "green")],
            background=[("active", "black")],
        )
        self.root.title("Sylwia Mościcka - zadanie 1")
        self.root.minsize(width=800, height=600)
        line_prompted = Button(
            self.root,
            width=15,
            command=self.line_prompt,
            text="Linia - tekstowe",
        )
        line_prompted.grid(row=0, column=10, sticky="N")
        rectangle_prompted = Button(
            self.root,
            width=15,
            command=self.rectangle_prompt,
            text="Prostokąt - tekstowe",
        )
        rectangle_prompted.grid(row=1, column=10, sticky="N")
        circle_prompted = Button(
            self.root,
            width=15,
            command=self.circle_prompt,
            text="Okrąg - tekstowe",
        )
        circle_prompted.grid(row=2, column=10, sticky="N")
        change_size_prompted = Button(
            self.root,
            width=15,
            command=self.change_size_prompted,
            text="Ksztalt - tekstowe",
        )
        change_size_prompted.grid(row=3, column=10, sticky="N", padx=10, pady=10)
        line_mouse = Button(
            self.root,
            width=15,
            command=self.line_mouse,
            text="Linia - mysz",
        )
        line_mouse.grid(row=0, column=1, sticky="N", padx=10, pady=10)
        rectangle_mouse = Button(
            self.root,
            width=15,
            command=self.rectangle_mouse,
            text="Prostokąt - mysz",
        )
        rectangle_mouse.grid(row=1, column=1, sticky="N", padx=10, pady=10)
        circle_mouse = Button(
            self.root,
            width=15,
            command=self.circle_mouse,
            text="Okrąg - mysz",
        )
        circle_mouse.grid(row=2, column=1, sticky="N", padx=10, pady=10)
        move_mouse = Button(
            self.root,
            width=15,
            command=self.move_mouse,
            text="Przesuwanie - mysz",
        )
        move_mouse.grid(row=3, column=1, sticky="N", padx=10, pady=10)
        change_size_mouse = Button(
            self.root,
            width=15,
            command=self.change_size_mouse,
            text="Ksztalt - mysz",
        )
        change_size_mouse.grid(row=4, column=1, sticky="N", padx=10, pady=10)
        self.w.grid(row=0, column=2, columnspan=2, rowspan=9, sticky=W + E + N + S)
        self.root.mainloop()

    def line_prompt_elements(self, **kwargs):
        r = Tk()
        r.title("Dane linia")
        r.geometry("500x100")
        Label(r, text="pkt początkowy x ").grid(column=1, row=0, sticky=W)
        Label(r, text="pkt początkowy y").grid(column=1, row=1, sticky=W)
        Label(r, text="pkt końcowy x").grid(column=3, row=0, sticky=W)
        Label(r, text="pkt końcowy y").grid(column=3, row=1, sticky=W)

        x_start_entry = Entry(r)
        y_start_entry = Entry(r)
        x_end_entry = Entry(r)
        y_end_entry = Entry(r)

        x_start_entry.insert(0, kwargs.get("x_start_value", ""))
        y_start_entry.insert(0, kwargs.get("y_start_value", ""))
        x_end_entry.insert(0, kwargs.get("x_end_value", ""))
        y_end_entry.insert(0, kwargs.get("y_end_value", ""))

        x_start_entry.grid(row=0, column=2)
        y_start_entry.grid(row=1, column=2)
        x_end_entry.grid(row=0, column=4)
        y_end_entry.grid(row=1, column=4)

        return r, x_start_entry, y_start_entry, x_end_entry, y_end_entry

    def line_prompt(self):
        (
            r,
            x_start_entry,
            y_start_entry,
            x_end_entry,
            y_end_entry,
        ) = self.line_prompt_elements()

        draw_line_button = Button(
            r,
            command=lambda: self.add_line(
                x_start_entry.get(),
                y_start_entry.get(),
                x_end_entry.get(),
                y_end_entry.get(),
            ),
            text="Rysuj",
        )
        draw_line_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

    def line_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")
        self.w.bind("<Button-1>", self.line_mouse_clicked)

    def line_mouse_clicked(self, event):
        if not self.mouse_line_start:
            self.mouse_line_start = {"x": event.x, "y": event.y}
        else:
            self.mouse_line_end = {"x": event.x, "y": event.y}
            self.add_line(
                self.mouse_line_start["x"],
                self.mouse_line_start["y"],
                self.mouse_line_end["x"],
                self.mouse_line_end["y"],
            )
            self.mouse_line_start = None
            self.mouse_line_end = None

    def add_line(self, x_start, y_start, x_end, y_end):
        line = Line(x_start, y_start, x_end, y_end)
        self.lines.append(line)
        line.draw(self.w)

    def rectangle_prompt_elements(self, **kwargs):
        r = Tk()
        r.title("Dane kwadrat")
        r.geometry("600x150")
        Label(r, text="A - wspołrzędna X").grid(column=1, row=0, sticky=W)
        Label(r, text="A - wspołrzędna Y").grid(column=3, row=0, sticky=W)
        Label(r, text="D - wspołrzędna X").grid(column=1, row=1, sticky=W)
        Label(r, text="D - wspołrzędna Y").grid(column=3, row=1, sticky=W)

        a_x = Entry(r)
        a_y = Entry(r)
        d_x = Entry(r)
        d_y = Entry(r)

        a_x.insert(0, kwargs.get("a_x_value", ""))
        a_y.insert(0, kwargs.get("a_y_value", ""))
        d_x.insert(0, kwargs.get("d_x_value", ""))
        d_y.insert(0, kwargs.get("d_y_value", ""))

        a_x.grid(row=0, column=2)
        a_y.grid(row=0, column=4)
        d_x.grid(row=1, column=2)
        d_y.grid(row=1, column=4)

        return r, a_x, a_y, d_x, d_y

    def rectangle_prompt(self):
        r, a_x, a_y, d_x, d_y = self.rectangle_prompt_elements()

        draw_button = Button(
            r,
            command=lambda: self.add_rectangle(
                a_x.get(), a_y.get(), d_x.get(), d_y.get()
            ),
            text="Rysuj",
        )
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def rectangle_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")
        self.w.bind("<Button-1>", self.rectangle_clicked)

    def rectangle_clicked(self, event):
        if not self.mouse_rectangle_a:
            self.mouse_rectangle_a = {"x": event.x, "y": event.y}
        else:
            self.mouse_rectangle_d = {"x": event.x, "y": event.y}
            self.add_rectangle(
                self.mouse_rectangle_a["x"],
                self.mouse_rectangle_a["y"],
                self.mouse_rectangle_d["x"],
                self.mouse_rectangle_d["y"],
            )
            self.mouse_rectangle_a = None
            self.mouse_rectangle_d = None

    def add_rectangle(self, a_x, a_y, d_x, d_y):
        rectangle = Rectangle(a_x, a_y, d_x, d_y)
        self.rectangles.append(rectangle)
        rectangle.draw(self.w)

    def circle_prompt_elements(self, **kwargs):
        r = Tk()
        r.title("Dane koło")
        r.geometry("600x150")
        Label(r, text="A - wspołrzędna X").grid(column=1, row=0, sticky=W)
        Label(r, text="A - wspołrzędna Y").grid(column=3, row=0, sticky=W)
        Label(r, text="Promien").grid(column=1, row=1, sticky=W)

        a_x = Entry(r)
        a_y = Entry(r)
        radius = Entry(r)

        a_x.insert(0, kwargs.get("a_x_value", ""))
        a_y.insert(0, kwargs.get("a_y_value", ""))
        radius.insert(0, kwargs.get("radius_value", ""))

        a_x.grid(row=0, column=2)
        a_y.grid(row=0, column=4)
        radius.grid(row=1, column=2)

        return r, a_x, a_y, radius

    def circle_prompt(self):
        r, a_x, a_y, radius = self.circle_prompt_elements()

        draw_button = Button(
            r,
            command=lambda: self.add_circle(a_x.get(), a_y.get(), radius.get()),
            text="Rysuj",
        )
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def circle_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")
        self.w.bind("<Button-1>", self.circle_clicked)

    def circle_clicked(self, event):
        if not self.mouse_circle_a:
            self.mouse_circle_a = {"x": event.x, "y": event.y}
        else:
            radius_distance = math.sqrt(
                ((self.mouse_circle_a["x"] - event.x) ** 2)
                + ((self.mouse_circle_a["y"] - event.y) ** 2)
            )
            self.mouse_circle_r = radius_distance
            self.add_circle(
                self.mouse_circle_a["x"], self.mouse_circle_a["y"], self.mouse_circle_r
            )
            self.mouse_circle_a = None
            self.mouse_circle_r = None

    def add_circle(self, a_x, a_y, r):
        circle = Circle(int(a_x), int(a_y), int(r))
        self.circles.append(circle)
        circle.draw(self.w)

    def change_size_prompted(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")
        self.w.bind("<Button-1>", self.change_size_prompt)

    def change_size_prompt(self, event):
        self.mouse_move_selected_object = self.get_closest_primitive(event.x, event.y)
        r = Tk()
        r.title("Zmiana ksztaltu")
        r.geometry("600x150")

        if self.mouse_move_selected_object.__class__.__name__ is "Rectangle":
            self.w.itemconfig(self.mouse_move_selected_object.drawn_item, outline="red")

            a_x = self.mouse_move_selected_object.a_x
            a_y = self.mouse_move_selected_object.a_y
            d_x = self.mouse_move_selected_object.d_x
            d_y = self.mouse_move_selected_object.d_y

            r, a_x, a_y, d_x, d_y = self.rectangle_prompt_elements(
                a_x_value=a_x, a_y_value=a_y, d_x_value=d_x, d_y_value=d_y
            )

            draw_button = Button(
                r,
                command=lambda: self.mouse_move_selected_object.change_coordinates(
                    a_x.get(), a_y.get(), d_x.get(), d_y.get(), self.w
                ),
                text="Zmien",
            )
            draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

        if self.mouse_move_selected_object.__class__.__name__ is "Line":
            self.w.itemconfig(self.mouse_move_selected_object.drawn_item, fill="red")
            a_x = self.mouse_move_selected_object.a_x
            a_y = self.mouse_move_selected_object.a_y
            b_x = self.mouse_move_selected_object.b_x
            b_y = self.mouse_move_selected_object.b_y

            (
                r,
                x_start_entry,
                y_start_entry,
                x_end_entry,
                y_end_entry,
            ) = self.line_prompt_elements(
                x_start_value=a_x, y_start_value=a_y, x_end_value=b_x, y_end_value=b_y
            )

            draw_line_button = Button(
                r,
                command=lambda: self.mouse_move_selected_object.change_coordinates(
                    x_start_entry.get(),
                    y_start_entry.get(),
                    x_end_entry.get(),
                    y_end_entry.get(),
                    self.w,
                ),
                text="Zmien",
            )
            draw_line_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

        if self.mouse_move_selected_object.__class__.__name__ is "Circle":
            self.w.itemconfig(self.mouse_move_selected_object.drawn_item, outline="red")
            a_x = self.mouse_move_selected_object.a_x
            a_y = self.mouse_move_selected_object.a_y
            radius_value = self.mouse_move_selected_object.r

            r, a_x, a_y, radius = self.circle_prompt_elements(
                a_x_value=a_x, a_y_value=a_y, radius_value=radius_value
            )

            draw_button = Button(
                r,
                command=lambda: self.mouse_move_selected_object.change_coordinates(
                    int(a_x.get()), int(a_y.get()), int(radius.get()), self.w
                ),
                text="Zmien",
            )
            draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def move_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")

        self.w.bind("<B1-Motion>", self.move_mouse_held)
        self.w.bind("<ButtonRelease-1>", self.move_mouse_released)

    def move_mouse_held(self, event):
        if not self.mouse_move_selected_object:
            self.mouse_move_selected_object = self.get_closest_primitive(
                event.x, event.y
            )
            if self.mouse_move_selected_object.__class__.__name__ is "Line":
                self.w.itemconfig(
                    self.mouse_move_selected_object.drawn_item, fill="red"
                )
            else:
                self.w.itemconfig(
                    self.mouse_move_selected_object.drawn_item, outline="red"
                )

        else:
            if self.mouse_move_selected_object.__class__.__name__ is "Rectangle":
                a_x = self.mouse_move_selected_object.a_x
                a_y = self.mouse_move_selected_object.a_y
                d_x = self.mouse_move_selected_object.d_x
                d_y = self.mouse_move_selected_object.d_y

                difference_d_x = event.x - int(a_x)
                difference_d_y = event.y - int(a_y)

                self.mouse_move_selected_object.change_coordinates(
                    event.x, event.y, d_x + difference_d_x, d_y + difference_d_y, self.w
                )
            elif self.mouse_move_selected_object.__class__.__name__ is "Line":
                a_x = self.mouse_move_selected_object.a_x
                a_y = self.mouse_move_selected_object.a_y
                b_x = self.mouse_move_selected_object.b_x
                b_y = self.mouse_move_selected_object.b_y

                difference_b_x = event.x - int(a_x)
                difference_b_y = event.y - int(a_y)

                self.mouse_move_selected_object.change_coordinates(
                    event.x, event.y, b_x + difference_b_x, b_y + difference_b_y, self.w
                )
            elif self.mouse_move_selected_object.__class__.__name__ is "Circle":
                radius = self.mouse_move_selected_object.r
                self.mouse_move_selected_object.change_coordinates(
                    event.x, event.y, radius, self.w
                )

    def move_mouse_released(self, event):
        self.mouse_move_selected_object = None
        self.w.unbind("<B1-Motion>")

    def change_size_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind("<ButtonRelease-1>")
        self.w.bind("<Button-1>", self.change_size_clicked)

    def closest_point(self, point, points):
        closest_index = distance.cdist([point], points).argmin()
        return closest_index

    def get_closest_primitive(self, clicked_point_x, clicked_point_y):
        points = []
        for index, value in enumerate(self.rectangles):
            points.append(
                {"id": index, "type": "rectangle", "x": value.a_x, "y": value.a_y}
            )
            points.append(
                {"id": index, "type": "rectangle", "x": value.d_x, "y": value.d_y}
            )

        for index, value in enumerate(self.lines):
            points.append({"id": index, "type": "line", "x": value.a_x, "y": value.a_y})
            points.append({"id": index, "type": "line", "x": value.b_x, "y": value.b_y})

        for index, value in enumerate(self.circles):
            points.append(
                {"id": index, "type": "circle", "x": value.a_x, "y": value.a_y}
            )

        point_coordinates = []
        for value in points:
            point_coordinates.append((value["x"], value["y"]))

        closest_point_index = self.closest_point(
            (clicked_point_x, clicked_point_y), point_coordinates
        )
        closest_point = points[closest_point_index]

        if closest_point["type"] is "rectangle":
            return self.rectangles[closest_point["id"]]
        if closest_point["type"] is "line":
            return self.lines[closest_point["id"]]
        if closest_point["type"] is "circle":
            return self.circles[closest_point["id"]]

    def change_size_clicked(self, event):
        try:
            if not self.mouse_move_selected_object:
                self.mouse_move_selected_object = self.get_closest_primitive(
                    event.x, event.y
                )
                if self.mouse_move_selected_object.__class__.__name__ is "Line":
                    self.w.itemconfig(
                        self.mouse_move_selected_object.drawn_item, fill="red"
                    )
                else:
                    self.w.itemconfig(
                        self.mouse_move_selected_object.drawn_item, outline="red"
                    )

            else:
                if self.mouse_move_selected_object.__class__.__name__ is "Rectangle":
                    if not self.mouse_rectangle_a:
                        self.mouse_rectangle_a = {"x": event.x, "y": event.y}
                    else:
                        self.mouse_rectangle_d = {"x": event.x, "y": event.y}
                        self.mouse_move_selected_object.change_coordinates(
                            self.mouse_rectangle_a["x"],
                            self.mouse_rectangle_a["y"],
                            self.mouse_rectangle_d["x"],
                            self.mouse_rectangle_d["y"],
                            self.w,
                        )
                        self.mouse_rectangle_a = None
                        self.mouse_rectangle_d = None
                        self.mouse_move_selected_object = None
                elif self.mouse_move_selected_object.__class__.__name__ is "Line":
                    if not self.mouse_line_start:
                        self.mouse_line_start = {"x": event.x, "y": event.y}
                    else:
                        self.mouse_line_end = {"x": event.x, "y": event.y}
                        self.mouse_move_selected_object.change_coordinates(
                            self.mouse_line_start["x"],
                            self.mouse_line_start["y"],
                            self.mouse_line_end["x"],
                            self.mouse_line_end["y"],
                            self.w,
                        )
                        self.mouse_line_start = None
                        self.mouse_line_end = None
                        self.mouse_move_selected_object = None
                elif self.mouse_move_selected_object.__class__.__name__ is "Circle":
                    if not self.mouse_circle_a:
                        self.mouse_circle_a = {"x": event.x, "y": event.y}
                    else:
                        x = self.mouse_circle_a["x"]
                        y = self.mouse_circle_a["y"]
                        radius_distance = math.sqrt(
                            ((self.mouse_circle_a["x"] - event.x) ** 2)
                            + ((self.mouse_circle_a["y"] - event.y) ** 2)
                        )
                        self.mouse_circle_r = radius_distance

                        self.mouse_move_selected_object.change_coordinates(
                            x, y, radius_distance, self.w
                        )
                        self.mouse_circle_a = None
                        self.mouse_circle_r = None
                        self.mouse_move_selected_object = None
        except ValueError:
            messagebox.askokcancel(
                "ostrzeżenie", "Nie ma figury do zmian, chcesz spróbować ponownie?"
            )


Menu()
