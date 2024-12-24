import tkinter as tk

class risovalka:
    def __init__(self, root):
        self.root = root
        self.root.title("risovalka")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.drawing_color = "black"
        self.brush_size = 3
        self.last_x, self.last_y = None, None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        toolbar = tk.Frame(root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        color_button = tk.Button(toolbar, text="Цвет", command=self.change_color)
        color_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(toolbar, text="Очистка", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                     fill=self.drawing_color, width=self.brush_size)
        self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        self.last_x, self.last_y = None, None

    def change_color(self):
        from tkinter.colorchooser import askcolor
        color = askcolor()[1]
        if color:
            self.drawing_color = color

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = risovalka(root)
    root.mainloop()
