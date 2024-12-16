import tkinter as tk
from data import DataLoader
from predict_with_dino import PredictWithDino
from visualize import Visualize
from preview import Preview
from tkinter import filedialog


def data_function():
    file_path = filedialog.askdirectory(title="Select a Folder")
    global loader
    loader = DataLoader(file_path)
    print("Chosen path:", file_path)


def preview_function():
    global loader
    preview = Preview(loader)
    global box_threshold
    global text_threshold
    global text
    box_threshold, text_threshold, text = preview.previewer()


def autolabel_function():
    global loader
    global box_threshold
    global text_threshold
    global text
    dframe = dino.predict_and_save(loader, 0.38, 0.01, "door.")
    dframe.to_csv(f"{loader.dir_name}.csv", index=False)

def view_function():
    global loader
    visualize = Visualize(loader)
    visualize.run()




if __name__ == '__main__':
    dino = PredictWithDino()

    root = tk.Tk()
    root.title('Hello World')
    root.geometry('500x500')

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)


    button_load_data = tk.Button(root, text='Load Data', command=lambda: data_function())
    button_preview = tk.Button(root, text='Preview', command=lambda: preview_function())
    button_autolabel = tk.Button(root, text='Autolabel', command=lambda: autolabel_function())
    button_view = tk.Button(root, text='View', command=lambda: view_function())

    button_load_data.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    button_preview.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    button_autolabel.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    button_view.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

    root.mainloop()
