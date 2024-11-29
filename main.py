import tkinter as tk

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


button_load_data = tk.Button(root, text='Load Data', command=lambda: 0)
button_preview = tk.Button(root, text='Preview', command=lambda: 0)
button_autolabel = tk.Button(root, text='Autolabel', command=lambda: 0)
button_view = tk.Button(root, text='View', command=lambda: 0)

button_load_data.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
button_preview.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
button_autolabel.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
button_view.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

root.mainloop()