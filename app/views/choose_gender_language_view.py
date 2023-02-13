import tkinter as tk
from abc import ABC


class ChooseGenderLanguageView(ABC):

    def __init__(self, root):
        self.root = root
        b1 = tk.Button(self.root, text="Button 1")
        b2 = tk.Button(self.root, text="Button 2")
        b3 = tk.Button(self.root, text="Button 3")
        b4 = tk.Button(self.root, text="Button 4")

        b1.pack(side='left', padx=960 / 2 - 100)
        b2.pack(side='left', padx=960 / 2 - 100)
        b3.pack(side='right', padx=960 / 2 - 100)
        b4.pack(side='right', padx=960 / 2 - 100)



    def switch_to_main_view(self):
        from .main_view import MainView
        self.root.destroy()
        root = tk.Tk()
        root.geometry("1920x1080")
        MainView(root)
        root.mainloop()

