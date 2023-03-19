import tkinter as tk

from app.enums import Options
from app.views.basic.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, WIDTH, BUTTON_FONT
from app.views.choose_voice_model_view import ChooseVoiceModelView
from app.views.choose_audio_view import ChooseAudioView

RADIO_BUTTON_WIDTH = 150


class ChooseGenderLanguageView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, option):
        super(ChooseGenderLanguageView, self).__init__(root, voice_model_service, voice_recordings_service,
                                                       version_service)
        self.option = option
        self.language = tk.StringVar()
        self.language.set("polish")
        self.gender = tk.StringVar()
        self.gender.set("man")
        self.display_widgets()

    def display_widgets(self):
        language_label = tk.Label(self.root, bg='green', text="Wybierz język", font=BUTTON_FONT)
        language_label.place(x=WIDTH / 2 - 60, y=60)
        rb1 = tk.Radiobutton(self.root, text="polski", variable=self.language, value='polish', font=BUTTON_FONT)
        rb2 = tk.Radiobutton(self.root, text="angielski", variable=self.language, value='english', font=BUTTON_FONT)
        rb1.place(x=WIDTH / 2 - RADIO_BUTTON_WIDTH - 10, y=100, width=RADIO_BUTTON_WIDTH)
        rb2.place(x=WIDTH / 2 + 10, y=100, width=RADIO_BUTTON_WIDTH)
        gender_label = tk.Label(self.root, text="Wybierz płeć", bg='green', font=BUTTON_FONT)
        gender_label.place(x=WIDTH / 2 - 60, y=200)
        rb3 = tk.Radiobutton(self.root, text="kobieta", variable=self.gender, value='woman', font=BUTTON_FONT)
        rb4 = tk.Radiobutton(self.root, text="mężczyzna", variable=self.gender, value='man', font=BUTTON_FONT)
        rb3.place(x=WIDTH / 2 - RADIO_BUTTON_WIDTH - 10, y=230, width=RADIO_BUTTON_WIDTH)
        rb4.place(x=WIDTH / 2 + 10, y=230, width=RADIO_BUTTON_WIDTH)

        submit_button = tk.Button(self.root, text="Dalej", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                  command=self.switch_to_next_view)
        main_menu = tk.Button(self.root, text="Menu główne", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                              command=self.switch_to_main_view)
        main_menu.place(x=WIDTH / 2 - 300, y=450)
        submit_button.place(x=WIDTH / 2, y=450)

    def switch_to_next_view(self):
        if self.option == Options.generate_samples.value:
            self.switch_to_choose_audio()
        self.switch_to_choose_audio()

    def switch_to_choose_model(self):
        gender = self.gender.get()
        language = self.language.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        ChooseVoiceModelView(self.root, gender, language, self.voice_model_service, self.voice_recordings_service,
                             self.version_service, self.option)

    def switch_to_choose_audio(self):
        language = self.language.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        ChooseAudioView(self.root, language, self.voice_model_service, self.voice_recordings_service,
                        self.version_service, self.option, language)
