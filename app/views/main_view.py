import tkinter as tk


from app.views.choose_gender_language_view import ChooseGenderLanguageView

WIDTH = 1920
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PAD_Y = 80


class MainView:

    def __init__(self, root):
        self.root = root
        self.root.configure(bg='green')
        b1 = tk.Button(self.root, text="Stwórz nowy model głosu", command=self.switch_to_choose_gender_language_view, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        b2 = tk.Button(self.root, text="Dotrenuj model głosu",width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        b3 = tk.Button(self.root, text="Syntezuj mowę na podstawie modelu",width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        b4 = tk.Button(self.root, text="Wygeneruj próbki do uczenia",width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        b1.pack(pady=PAD_Y)
        b2.pack(pady=PAD_Y)
        b3.pack(pady=PAD_Y)
        b4.pack(pady=PAD_Y)


    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        ChooseGenderLanguageView(self.root)

