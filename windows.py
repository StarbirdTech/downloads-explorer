import tkinter as tk
from PIL import Image, ImageTk
import random
from files import UniqueImagePaths


class ImageWindow:
    def __init__(self, root, images, screen_width, screen_height) -> None:
        self.root = root
        self.images = images
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width, self.height = 100, 100
        self.snap_to_mouse = False
        self.x_offset, self.y_offset = 0, 0
        self.window = tk.Toplevel(root)
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)
        self.image, self.new_width, self.new_height = self.get_image()
        self.label = tk.Label(
            self.window,
            image=self.image,
        )
        self.label.image = self.image
        self.label.pack(fill="both", expand=True)
        self.label.bind("<Button-1>", self.start_snap)
        self.label.bind("<ButtonRelease-1>", self.stop_snap)
        self.label.bind("<B1-Motion>", self.snap_window)
        self.move_to_random_position()
        print("Made a window")

    def get_image(self):
        image_path = self.images.get_unique_path()
        print(image_path)
        image = Image.open(image_path)

        # Get the image dimensions
        image_width, image_height = image.size

        # Calculate the maximum dimension for the image
        max_dimension = int(
            min(self.screen_width, self.screen_height) * random.randint(3, 9) / 10
        )

        # Calculate new dimensions while preserving aspect ratio
        if image_width > image_height:
            new_width = int(max_dimension)
            new_height = int((max_dimension / image_width) * image_height)
        else:
            new_height = int(max_dimension)
            new_width = int((max_dimension / image_height) * image_width)

        # Resize the image with LANCZOS resampling
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Convert the resized image to a format that tkinter can display
        return (
            ImageTk.PhotoImage(
                image=image,
                master=self.window,
            ),
            new_width,
            new_height,
        )

    def snap_window(self, event) -> None:
        if self.snap_to_mouse:
            self.window.geometry(
                f"{self.new_width}x{self.new_height}+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}"
            )

    def start_snap(self, event) -> None:
        self.snap_to_mouse = True
        self.x_offset, self.y_offset = (
            event.x_root - self.window.winfo_x(),
            event.y_root - self.window.winfo_y(),
        )

    def stop_snap(self, event) -> None:
        self.snap_to_mouse = False

    def move_to_random_position(self) -> None:
        x = int(random.randint(0, self.screen_width - self.width))
        y = int(random.randint(0, self.screen_height - self.height))
        self.window.geometry(f"{self.new_width}x{self.new_height}+{x}+{y}")
        self.window.after(
            random.randint(5000, 10000),
            lambda: self.move_to_random_position(),
        )


class Controller:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Control-l>", lambda e: self.list_image_windows())
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.label = tk.Label(self.root, text="Press Ctrl+L to list image windows")
        self.label.pack()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.images = UniqueImagePaths()
        self.image_windows = []
        self.root.after(random.randint(5000, 10000), lambda: self.create_image_window())
        self.root.mainloop()

    def create_image_window(self) -> None:
        try:
            self.image_windows.append(
                ImageWindow(
                    self.root, self.images, self.screen_width, self.screen_height
                )
            )
            self.root.after(
                random.randint(5000, 10000), lambda: self.create_image_window()
            )
        except StopIteration:
            print("All images have been used")

    def list_image_windows(self) -> None:
        for window in self.image_windows:
            print(window.window.winfo_x(), window.window.winfo_y())
