import tkinter as tk


from app.views.choose_gender_language_view import ChooseGenderLanguageView
from app.components.listbox_with_button import ListBoxWithButton
WIDTH = 1920
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PAD_Y = 80


class ChooseVoiceModelView:

    def __init__(self, root, gender, language, voice_service):
        self.root = root
        models = voice_service.select_gender_language(gender, language)

        self.listbox = ListBoxWithButton()
        counter = 0
        for model in models:

            self.listbox(counter,models['name'], path)


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
            widget.destroy()
        ChooseGenderLanguageView(self.root)

    def switch_to_main_menu(self):
        pass

    def switch_to_previous_view(self):
        pass

    def switch_to_choose_audio_view(self):
        pass


