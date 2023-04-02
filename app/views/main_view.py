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
                       width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1, font=self.BUTTON_FONT)
        b2 = tk.Button(self.root, text="Dotrenuj model głosu", width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1,
                       command=self.switch_to_choose_gender_language_train_old,
                       font=self.BUTTON_FONT)
        b3 = tk.Button(self.root, text="Syntezuj mowę na podstawie modelu", width=self.BUTTON_WIDTH_1,
                       height=self.BUTTON_HEIGHT_1, font=self.BUTTON_FONT,
                       command=self.switch_to_choose_gender_language_synthesize)
        b4 = tk.Button(self.root, text="Wygeneruj próbki do uczenia", width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1,
                       command=self.switch_to_choose_language, font=self.BUTTON_FONT)

        b1.pack(pady=self.PAD_Y)
        b2.pack(pady=self.PAD_Y)
        b3.pack(pady=self.PAD_Y)
        b4.pack(pady=self.PAD_Y)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()
