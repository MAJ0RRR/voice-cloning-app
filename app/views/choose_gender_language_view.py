import tkinter as tk
from tkinter import messagebox
from lazy_import import lazy_module
from app.enums import Options
from app.views.basic.basic_view import BasicView

choose_audio_module = lazy_module('app.views.choose_audio_view')
choose_voice_module = lazy_module('app.views.choose_voice_model_view')


class ChooseGenderLanguageView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, option):
        super(ChooseGenderLanguageView, self).__init__(root, voice_model_service, voice_recordings_service,
                                                       version_service)
        self.option = option
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.language = tk.StringVar()
        self.RADIO_BUTTON_WIDTH = 5 * self.size_grid_x
        self.language.set("polish")
        self.gender = tk.StringVar()
        self.gender.set("man")
        self.display_widgets()

    def display_widgets(self):
        language_label = tk.Label(self.root, bg='green', text="Wybierz język", font=self.MAX_FONT)
        language_label.pack(pady=self.PAD_Y)
        rb1 = tk.Radiobutton(self.root, text="polski", variable=self.language, value='polish', font=self.BUTTON_FONT, width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2)
        rb2 = tk.Radiobutton(self.root, text="angielski", variable=self.language, value='english',
                             font=self.BUTTON_FONT,  width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2)
        rb1.place(x=self.WIDTH / 2 - self.size_grid_x * 7, y=5 * self.size_grid_y)
        rb2.place(x=self.WIDTH / 2 + self.size_grid_x * 4, y=5 * self.size_grid_y)
        if self.option != Options.generate_samples:
            gender_label = tk.Label(self.root, text="Wybierz płeć", bg='green', font=self.MAX_FONT)
            gender_label.pack(pady=self.PAD_Y)
            rb3 = tk.Radiobutton(self.root, text="kobieta", variable=self.gender, value='woman', font=self.BUTTON_FONT, width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2)
            rb4 = tk.Radiobutton(self.root, text="mężczyzna", variable=self.gender, value='man', font=self.BUTTON_FONT,width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2)
            rb3.place(x=self.WIDTH / 2 - self.size_grid_x * 7, y=13 * self.size_grid_y)
            rb4.place(x=self.WIDTH / 2 + self.size_grid_x * 4, y=13 * self.size_grid_y)
        submit_button = tk.Button(self.root, text="Dalej", width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1,
                                  command=self.switch_to_next_view)
        main_menu = tk.Button(self.root, text="Menu główne", width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1,
                              command=self.switch_to_main_view)
        main_menu.place(x=self.WIDTH / 2 - 10 * self.size_grid_x, y=20 * self.size_grid_y)
        submit_button.place(x=self.WIDTH / 2 +5* self.size_grid_x, y=20 * self.size_grid_y)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()

    def switch_to_next_view(self):
        if self.option == Options.generate_samples:
            self.switch_to_choose_audio()
        elif self.option == Options.train_new:
            self.switch_to_choose_audio()
        else:
            self.switch_to_choose_model()

    def switch_to_choose_model(self):
        gender = self.gender.get()
        language = self.language.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_module.ChooseVoiceModelView(self.root, gender, language, self.voice_model_service,
                                                 self.voice_recordings_service,
                                                 self.version_service, self.option)

    def switch_to_choose_audio(self):
        language = self.language.get()
        gender = None
        if self.option == Options.train_new:
            gender = self.language.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_audio_module.ChooseAudioView(self.root, self.voice_model_service, self.voice_recordings_service,
                                            self.version_service, self.option, language, gender)
