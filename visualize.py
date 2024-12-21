import numpy as np
import cv2
import pandas as pd
from tkinter import Tk, Label, Toplevel
from PIL import Image, ImageTk
from data import DataLoader
import tkinter as tk


# class Visualize:
#     def __init__(self, loader: DataLoader):
#         self.names, self.images = loader.load_folder()
#         self.dir_name = loader.dir_name
#         self.dataframe = pd.read_csv(f"{self.dir_name}.csv")
#
#     def __assign_idx(self, list1, list_ref):
#         result = np.zeros(len(list1))
#         for inx, name in enumerate(list1):
#             for i, nm in enumerate(list_ref):
#                 if name == nm:
#                     result[inx] = i
#         return result
#
#     def __draw_labels(self):
#         name_series = pd.Series(self.names)
#         name_frame = self.dataframe['name']
#         mask = self.__assign_idx(name_frame, name_series)
#         mask = mask.astype(int)
#         labeled_images = []
#         x_min = self.dataframe["x_min"]
#         y_min = self.dataframe["y_min"]
#         x_max = self.dataframe["x_max"]
#         y_max = self.dataframe["y_max"]
#
#         for i, u in enumerate(mask):
#             cv2.rectangle(self.images[u], (x_min[i], y_min[i]), (x_max[i], y_max[i]), (0, 0, 255), 2)
#             labeled_images.append(self.images[u])  # wcześniej był błąd - zmieniono na u
#
#         return labeled_images
#
#     def __convert_to_pil(self, labeled_images):
#         pil_images = []
#
#         for img in labeled_images:
#             opencv_image = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
#             pil_image = Image.fromarray(opencv_image)
#             pil_images.append(pil_image)
#         return pil_images
#
#     def __save_results(self, remove_list):
#         mask = self.dataframe['name'].isin(remove_list)
#         df2 = self.dataframe.copy()
#         df2 = self.dataframe[~mask]
#         # saving labels of correctly labbeled images
#         df2.to_csv(f"{self.dir_name}.csv", index=False)
#
#         frame_of_all_names = pd.DataFrame(self.names, columns=["name"])
#         merged = frame_of_all_names.merge(df2["name"], how='left', on='name', indicator=True)
#         df_diff = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
#         df_diff.to_csv(f"{self.dir_name}_wrong.csv", index=False)
#
#     def __view(self, pil_images):
#         remove_list = []
#
#         def display(name_frame):
#             # Odczytanie wartości zmiennej powiązanej z suwakiem
#             # name_frame = self.dataframe['name']
#             current_value = scale_var.get()
#             label.config(text=f"IMAGE NAME: {name_frame[current_value]}") # tu błąd możliwy
#             # label.config(text=f"IMAGE NAME: {self.names[current_value]}")  # tu błąd możliwy
#             print(f"current_value: {current_value}, self.names: {self.names[current_value]}")
#
#             global tk_image
#             tk_image = ImageTk.PhotoImage(pil_images[current_value])
#             label_photo.config(image=tk_image)
#
#         def on_button_click():
#             current_value = scale_var.get()
#             to_remove = self.names[current_value]
#             remove_list.append(to_remove)
#             txt = remove_list[-1]
#             listbox.insert(tk.END, txt)
#
#         def on_button_click2():
#             if remove_list:
#                 listbox.delete(tk.END)
#                 remove_list.pop()
#
#         name_frame = self.dataframe['name']
#
#         root = Tk()
#         root.title("RESULTS")
#
#         scale_var = tk.IntVar()
#
#         image = pil_images[scale_var.get()]
#         tk_image = ImageTk.PhotoImage(image)
#
#         # Utwórz etykietę do wyświetlenia obrazu
#         label_photo = Label(root, image=tk_image)
#         label_photo.pack()
#
#         left_frame = tk.Frame(root)
#         left_frame.pack(side="left", padx=10, pady=10)
#
#         listbox = tk.Listbox(left_frame, height=10, width=20, font=("Arial", 12))
#         for item in remove_list:
#             listbox.insert(tk.END, item)  # Insert each item from the list into the Listbox
#         listbox.pack()
#
#         scale = tk.Scale(
#             root,
#             from_=0,  # Minimalna wartość
#             to=len(pil_images) - 1,  # Maksymalna wartość
#             resolution=1,  # Krok zmiany
#             orient="horizontal",  # Orientacja pozioma
#             length=300,  # Długość suwaka
#             label="Choose number",  # Etykieta
#             variable=scale_var,  # Powiązanie z zmienną
#             command=lambda _: display(name_frame)  # Aktualizacja wyświetlenia
#         )
#         scale.pack(pady=10)
#
#         label = tk.Label(root, text=f"IMAGE: {self.names[0]}")
#         label.pack(pady=10)
#
#         button = tk.Button(root, text="Remove From Set", command=on_button_click)
#         button.pack(pady=10)
#
#         button2 = tk.Button(root, text="Redo Removal", command=on_button_click2)
#         button2.pack(padx=10)
#
#         root.mainloop()
#
#         return remove_list
#
#     def run(self):
#         labeled_images = self.__draw_labels()
#         pil_images = self.__convert_to_pil(labeled_images)
#         remove_list = self.__view(pil_images)
#         self.__save_results(remove_list)


class Visualize:
    def __init__(self, loader: DataLoader):
        self.names, self.images = loader.load_folder()
        self.dir_name = loader.dir_name
        self.dataframe = pd.read_csv(f"{self.dir_name}.csv")

    def __assign_idx(self, list1, list_ref):
        result = np.zeros(len(list1))
        for inx, name in enumerate(list1):
            for i, nm in enumerate(list_ref):
                if name == nm:
                    result[inx] = i
        return result

    def __draw_labels(self):
        name_series = pd.Series(self.names)
        name_frame = self.dataframe['name']
        # print("name series len  ", len(name_series))
        # print("name frame len  ", len(name_frame))

        mask = self.__assign_idx(name_frame, name_series)
        mask = mask.astype(int)
        labeled_images = []
        # print(mask)
        # print("mask len  ", len(mask))
        x_min = self.dataframe["x_min"]
        y_min = self.dataframe["y_min"]
        x_max = self.dataframe["x_max"]
        y_max = self.dataframe["y_max"]

        for i, u in enumerate(mask):
            cv2.rectangle(self.images[u], (x_min[i], y_min[i]), (x_max[i], y_max[i]), (0, 0, 255), 2)
            labeled_images.append(self.images[u])  # wcześniej był błąd - zmieniono na u

        # print("labeled images len  ",len(labeled_images))
        return labeled_images

    def __convert_to_pil(self, labeled_images):
        pil_images = []

        for img in labeled_images:
            opencv_image = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(opencv_image)
            pil_images.append(pil_image)
        # print("pil images len  ", len(pil_images))
        return pil_images

    # def __save_results(self, remove_list):
    #     mask = self.dataframe['name'].isin(remove_list)
    #     df2 = self.dataframe.copy()
    #     df2 = self.dataframe[~mask]
    #     # saving labels of correctly labbeled images
    #     df2.to_csv(f"{self.dir_name}.csv", index=False)

    #     frame_of_all_names = pd.DataFrame(self.names, columns=["name"])
    #     merged = frame_of_all_names.merge(df2["name"], how='left', on='name', indicator=True)
    #     df_diff = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    #     df_diff.to_csv(f"{self.dir_name}_wrong.csv", index=False)

    def __save_results(self, remove_list):
        # poprawiona wersja
        mask = self.dataframe.index.isin(remove_list)

        df2 = self.dataframe.copy()
        df2 = df2[~mask]
        # saving labels of correctly labbeled images
        df2.to_csv(f"{self.dir_name}.csv", index=False)

        frame_of_all_names = pd.DataFrame(self.names, columns=["name"])
        merged = frame_of_all_names.merge(df2["name"], how='left', on='name', indicator=True)
        df_diff = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
        df_diff.to_csv(f"{self.dir_name}_wrong.csv", index=False)

    def __view(self, pil_images):
        remove_list = []

        def display(name_frame):
            # Odczytanie wartości zmiennej powiązanej z suwakiem
            # name_frame = self.dataframe['name']
            current_value = scale_var.get()
            # label.config(text=f"IMAGE NAME: {name_frame[current_value]}")
            label.config(text=f"INDEX: {current_value}")
            # label.config(text=f"IMAGE NAME: {self.names[current_value]}")
            # print(f"current_value: {current_value}, name frame: {name_frame[current_value]}")

            global tk_image
            tk_image = ImageTk.PhotoImage(pil_images[current_value])
            label_photo.config(image=tk_image)

        def on_button_click():
            current_value = scale_var.get()
            # to_remove = self.names[current_value]
            to_remove = current_value
            remove_list.append(to_remove)
            txt = remove_list[-1]
            listbox.insert(tk.END, txt)

        def on_button_click2():
            if remove_list:
                listbox.delete(tk.END)
                remove_list.pop()

        name_frame = self.dataframe['name']

        root = Tk()
        root.title("RESULTS")

        scale_var = tk.IntVar()

        image = pil_images[scale_var.get()]
        tk_image = ImageTk.PhotoImage(image)

        # Utwórz etykietę do wyświetlenia obrazu
        label_photo = Label(root, image=tk_image)
        label_photo.pack()

        left_frame = tk.Frame(root)
        left_frame.pack(side="left", padx=10, pady=10)

        listbox = tk.Listbox(left_frame, height=10, width=20, font=("Arial", 12))
        for item in remove_list:
            listbox.insert(tk.END, item)  # Insert each item from the list into the Listbox
        listbox.pack()

        scale = tk.Scale(
            root,
            from_=0,  # Minimalna wartość
            to=len(pil_images) - 1,  # Maksymalna wartość
            resolution=1,  # Krok zmiany
            orient="horizontal",  # Orientacja pozioma
            length=300,  # Długość suwaka
            label="Choose number",  # Etykieta
            variable=scale_var,  # Powiązanie z zmienną
            command=lambda _: display(name_frame)  # Aktualizacja wyświetlenia
        )
        scale.pack(pady=10)

        label = tk.Label(root, text=f"IMAGE: {self.names[0]}")
        label.pack(pady=10)

        button = tk.Button(root, text="Remove From Set", command=on_button_click)
        button.pack(pady=10)

        button2 = tk.Button(root, text="Redo Removal", command=on_button_click2)
        button2.pack(padx=10)

        root.mainloop()

        return remove_list

    def run(self):
        labeled_images = self.__draw_labels()
        pil_images = self.__convert_to_pil(labeled_images)
        remove_list = self.__view(pil_images)
        self.__save_results(remove_list)