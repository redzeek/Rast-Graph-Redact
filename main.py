import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageFont, ImageGrab

class risovalka:
    def __init__(self, root):
        self.root = root
        self.root.title("risovalka")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.active_button = None

        self.drawing_color = "black"
        self.brush_size = 3
        self.last_x, self.last_y = None, None
        self.start_x, self.start_y = None, None
        self.current_shape = None
        self.image = Image.new("RGB", (800, 600), "white")


        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_brush)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        toolbar = tk.Frame(root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        color_button = tk.Button(toolbar, text="Цвет", command=self.change_color)
        color_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(toolbar, text="Очистка", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_button = tk.Button(toolbar, text="Сохранить", command=self.save_image_from_canvas)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        load_button = tk.Button(toolbar, text="Загрузить", command=self.load_image)
        load_button.pack(side=tk.LEFT, padx=5, pady=5)

        brush_size_label = tk.Label(toolbar, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.brush_size_var = tk.IntVar(value=self.brush_size)
        brush_size_slider = tk.Scale(toolbar, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.brush_size_var)
        brush_size_slider.pack(side=tk.LEFT, padx=5, pady=5)

        text_button = tk.Button(toolbar, text="Текст", command=lambda: self.add_text("text",text_button))
        text_button.pack(side=tk.LEFT, padx=5, pady=5)

        shape_menu = tk.Menubutton(toolbar, text="Фигуры", relief=tk.RAISED)
        shape_menu.menu = tk.Menu(shape_menu, tearoff=0)
        shape_menu["menu"] = shape_menu.menu
        shape_menu.menu.add_radiobutton(label="Линия", command=lambda: self.set_shape("line",shape_menu))
        shape_menu.menu.add_radiobutton(label="Прямоугольник", command=lambda: self.set_shape("rectangle",shape_menu))
        shape_menu.menu.add_radiobutton(label="Овал", command=lambda: self.set_shape("oval",shape_menu))
        shape_menu.pack(side=tk.LEFT, padx=5, pady=5)

        brush_button = tk.Button(toolbar, text="Кисть", command=lambda: self.set_shape("brush", brush_button))
        brush_button.pack(side=tk.LEFT, padx=5, pady=5)

        eraser_button = tk.Button(toolbar, text="Ластик", command=lambda: self.set_shape("eraser", eraser_button))
        eraser_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.text_size = 16  # Размер текста по умолчанию

        text_size_label = tk.Label(toolbar, text="Размер текста:")
        text_size_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.text_size_var = tk.IntVar(value=self.text_size)
        text_size_slider = tk.Scale(toolbar, from_=8, to=48, orient=tk.HORIZONTAL, variable=self.text_size_var)
        text_size_slider.pack(side=tk.LEFT, padx=5, pady=5)

    def set_shape(self, shape, button=None):
        if self.current_shape == "text":
            self.canvas.bind("<Button-1>", self.start_draw)
        self.current_shape = shape
        self.set_active_button(button)

    def set_active_button(self, button):
        if self.active_button:
            self.active_button.config(bg="SystemButtonFace")

        if button is not None:
            button.config(bg="lightblue")

        self.active_button = button  # Запоминаем активную кнопку



    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.last_x, self.last_y = event.x, event.y

        self.canvas.delete("temp")

    def draw_brush(self, event):
        if self.current_shape == "brush":
            brush_size = self.brush_size_var.get()

            if self.last_x and self.last_y:
                # Рисуем линию между последней точкой и текущей
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill=self.drawing_color, width=brush_size, capstyle=tk.ROUND, smooth=True)

            # Запоминаем текущие координаты для следующего шага
            self.last_x, self.last_y = event.x, event.y

        elif self.current_shape == "eraser":
            brush_size = self.brush_size_var.get()

            if self.last_x and self.last_y:
                # Рисуем линию между последней точкой и текущей
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill="white", width=brush_size, capstyle=tk.ROUND, smooth=True)

            # Запоминаем текущие координаты для следующего шага
            self.last_x, self.last_y = event.x, event.y

        elif self.current_shape in ["line", "rectangle", "oval"]:
            # При рисовании фигуры, удаляем старую фигуру
            self.canvas.delete("temp")

            if self.current_shape == "line":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color,
                                        width=self.brush_size_var.get(), tags="temp")
            elif self.current_shape == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.drawing_color,
                                             width=self.brush_size_var.get(), tags="temp")
            elif self.current_shape == "oval":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.drawing_color,
                                        width=self.brush_size_var.get(), tags="temp")

    def stop_draw(self, event):
        self.canvas.delete("temp")

        if self.current_shape == "brush" or self.current_shape == "eraser":
            self.canvas.update()
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            self.clear_canvas()
            self.image.paste(screenshot, (0, 0))
            self.canvas_image = ImageTk.PhotoImage(screenshot)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

        elif self.current_shape == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=self.drawing_color, width=self.brush_size_var.get())
        elif self.current_shape == "rectangle":
            x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
            x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
            self.canvas.create_rectangle(x0, y0, x1, y1,
                                         outline=self.drawing_color, width=self.brush_size_var.get())
        elif self.current_shape == "oval":
            x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
            x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
            self.canvas.create_oval(x0, y0, x1, y1,
                                    outline=self.drawing_color, width=self.brush_size_var.get())
        self.start_x, self.start_y = None, None
        self.last_x, self.last_y = None, None

    def change_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_image_from_canvas(self):
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            screenshot.save(file_path)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")])
        if file_path:
            loaded_image = Image.open(file_path)
            self.image.paste(loaded_image, (0, 0))
            self.canvas_image = ImageTk.PhotoImage(loaded_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

    def add_text(self, shape, button):
        self.canvas.bind("<Button-1>", self.place_text)
        self.set_shape(shape, button)

    def place_text(self, event):
        # Удаляем предыдущее поле ввода, если оно существует
        if hasattr(self, "text_entry") and self.text_entry:
            self.text_entry.destroy()

        # Создаем поле для ввода текста
        self.text_entry = tk.Entry(self.root, font=("Arial", self.text_size_var.get()))
        self.text_entry.place(x=event.x, y=event.y)
        self.text_entry.focus_set()

        # Привязываем действие на нажатие Enter
        self.text_entry.bind("<Return>", lambda e: self.draw_text(self.text_entry.get(), event.x, event.y))

    def draw_text(self, text, x, y):
        if text:
            font_size = self.text_size_var.get()
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

            # Рисуем текст на Canvas (не центрируем, а выводим прямо в место клика)
            self.canvas.create_text(x, y, text=text, fill=self.drawing_color, font=("Arial", font_size), anchor=tk.NW)



        # Удаляем поле ввода
        if hasattr(self, "text_entry") and self.text_entry:
            self.text_entry.destroy()
            self.text_entry = None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.set_shape(None, None)


if __name__ == "__main__":
    root = tk.Tk()
    app = risovalka(root)
    root.mainloop()
