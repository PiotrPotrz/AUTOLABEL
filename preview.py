import tkinter as tk
from tkinter import Tk, Label, Entry, Button, Toplevel
from PIL import Image, ImageTk
import cv2
import numpy as np
import pandas as pd
import random

from predict_with_dino import PredictWithDino


class Preview:
    def __init__(self, loader):
        self.loader = loader
        self.names, self.images = loader.load_folder()
        self.pil_images = self.__load()
        self.dino = PredictWithDino()
        self.idx = 0  # Dodanie atrybutu do przechowywania indeksu obrazów
        self.tk_image = None  # Dodanie atrybutu do przechowywania aktualnego obrazu

    def previewer(self):
        text = ""

        def show_pred():
            image = self.pil_images[self.idx]
            image_array = np.array(image)
            opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            pred = self.dino.preview(opencv_image, text, box_var.get(), text_var.get(), self.loader)
            if isinstance(pred, pd.DataFrame) and not pred.empty:
                for _, row in pred.iterrows():
                    label, score, x_min, y_min, x_max, y_max = row
                    cv2.rectangle(opencv_image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 0, 255), 2)
                    cv2.putText(opencv_image, label, (int(x_min), int(y_max)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                2)
                rgb_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image)
                self.tk_image = ImageTk.PhotoImage(pil_image)  # Przechowuj obraz jako atrybut instancji
                label_photo.config(image=self.tk_image)

        def display():
            self.idx = random.randint(0, len(self.pil_images) - 1)  # Aktualizuj atrybut instancji
            self.tk_image = ImageTk.PhotoImage(self.pil_images[self.idx])  # Przechowuj obraz jako atrybut instancji
            label_photo.config(image=self.tk_image)

        def get_input():
            nonlocal text  # Użycie nonlocal zamiast global
            user_input = entry.get()
            text = user_input
            label.config(text=user_input)

        root = Tk()
        root.title("Preview")
        root.geometry("1000x700")

        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=2)
        root.grid_columnconfigure(2, weight=2)
        root.grid_rowconfigure(0, weight=3)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=2)
        root.grid_rowconfigure(3, weight=1)
        root.grid_rowconfigure(4, weight=1)

        # Wyświetl pierwszy obraz
        self.tk_image = ImageTk.PhotoImage(self.pil_images[0])  # Przechowuj obraz jako atrybut instancji
        label_photo = Label(root, image=self.tk_image)
        label_photo.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        box_var = tk.DoubleVar()
        text_var = tk.DoubleVar()

        scale = tk.Scale(
            root,
            from_=0, to=1, resolution=0.001,
            orient="horizontal", length=300,
            label="Boxes threshold", variable=box_var,
            command=lambda _: None
        )
        scale.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        scale2 = tk.Scale(
            root,
            from_=0, to=1, resolution=0.001,
            orient="horizontal", length=300,
            label="Text threshold", variable=text_var,
            command=lambda _: None
        )
        scale2.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)

        label = tk.Label(root, text="Input class names divided by .")
        label.grid(row=1, column=1)

        entry = tk.Entry(root, width=30)
        entry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        button = tk.Button(root, text="SAVE", command=get_input)
        button.grid(row=3, column=2, sticky="nsew", padx=5, pady=5, rowspan=2)

        button2 = tk.Button(root, text="ANOTHER\nIMAGE", command=display)
        button2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5, rowspan=2)

        button3 = tk.Button(root, text="PREVIEW", command=show_pred)
        button3.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        tk.mainloop()

        box_thresh = box_var.get()
        txt_thresh = text_var.get()

        return box_thresh, txt_thresh, text

    def __load(self):
        pil_images = []
        for img in self.images:
            opencv_image = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(opencv_image)
            pil_images.append(pil_image)
        return pil_images
