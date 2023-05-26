import tkinter as tk
from tkinter import messagebox

from app.views.basic.basic_view import BasicView


class MainView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service):
        super(MainView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.display_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_widgets(self):
        b1 = tk.Button(self.root, text="Stwórz nowy model głosu",
                       command=self.switch_to_choose_gender_language_train_new,
                       font=self.BUTTON_FONT)
        b2 = tk.Button(self.root, text="Dotrenuj model głosu",
                       command=self.switch_to_choose_gender_language_train_old,
                       font=self.BUTTON_FONT)
        b3 = tk.Button(self.root, text="Syntezuj mowę na podstawie modelu",
                       font=self.BUTTON_FONT,
                       command=self.switch_to_choose_gender_language_synthesize)
        b4 = tk.Button(self.root, text="Wygeneruj próbki do uczenia",
                       command=self.switch_to_choose_language, font=self.BUTTON_FONT)

        b1.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=self.PAD_Y, width=self.BUTTON_WIDTH_1,
                 height=self.BUTTON_HEIGHT_1)
        b2.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=3 * self.PAD_Y + self.BUTTON_HEIGHT_1,
                 width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        b3.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=5 * self.PAD_Y + self.BUTTON_HEIGHT_1 * 2,
                 width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        b4.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=7 * self.PAD_Y + self.BUTTON_HEIGHT_1 * 3,
                 width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()
