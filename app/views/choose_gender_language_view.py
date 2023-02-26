import tkinter as tk

from lazy_import import lazy_module
from app.views.choose_voice_model_view import ChooseVoiceModelView

main_menu_module = lazy_module("app.views.main_view")

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PAD_Y = 50
WIDTH = 1920
HEIGHT = 1080
RADIO_BUTTON_WIDTH = 150


class ChooseGenderLanguageView:

    def __init__(self, root, voice_model_service, voice_records_service):
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_records_service = voice_records_service
        self.language = tk.StringVar()
        self.language.set("polish")
        language_label = tk.Label(root, bg='green', text="Wybierz język", font=("Helvetica", 14))
        language_label.place(x=WIDTH / 2 - 60, y=60)
        rb1 = tk.Radiobutton(root, text="polski", variable=self.language, value='polish', font=("Helvetica", 14))
        rb2 = tk.Radiobutton(root, text="angielski", variable=self.language, value='english', font=("Helvetica", 14))
        rb1.place(x=WIDTH / 2 - RADIO_BUTTON_WIDTH - 10, y=100, width=RADIO_BUTTON_WIDTH)
        rb2.place(x=WIDTH / 2 + 10, y=100, width=RADIO_BUTTON_WIDTH)
        self.gender = tk.StringVar()
        self.gender.set("man")
        gender_label = tk.Label(root, text="Wybierz płeć", bg='green', font=("Helvetica", 14))
        gender_label.place(x=WIDTH / 2 - 60, y=200)
        rb3 = tk.Radiobutton(root, text="kobieta", variable=self.gender, value='woman', font=("Helvetica", 14))
        rb4 = tk.Radiobutton(root, text="mężczyzna", variable=self.gender, value='man', font=("Helvetica", 14))
        rb3.place(x=WIDTH / 2 - RADIO_BUTTON_WIDTH - 10, y=230, width=RADIO_BUTTON_WIDTH)
        rb4.place(x=WIDTH / 2 + 10, y=230, width=RADIO_BUTTON_WIDTH)

        submit_button = tk.Button(self.root, text="Dalej", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                  command=self.switch_to_choose_model)
        main_menu = tk.Button(self.root, text="Menu główne", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                              command=self.switch_to_main_view)
        main_menu.place(x=WIDTH / 2 - 300, y=450)
        submit_button.place(x=WIDTH / 2, y=450)

    def switch_to_main_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_records_service)

    def switch_to_choose_model(self):
        gender = self.gender.get()
        language = self.language.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        ChooseVoiceModelView(self.root, gender, language, self.voice_model_service, self.voice_records_service)
