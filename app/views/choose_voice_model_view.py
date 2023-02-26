import tkinter as tk
from playsound import playsound

from lazy_import import lazy_module

choose_gender_language_module = lazy_module("app.views.choose_gender_language_view")
main_menu_module = lazy_module("app.views.main_view")
WIDTH = 1920
BUTTON_WIDTH_1 = 30
BUTTON_HEIGHT_1 = 3
BUTTON_WIDTH_2 = 17
BUTTON_HEIGHT_2 = 1
PAD_Y = 40
MODELS_ON_PAGE = 10


class ChooseVoiceModelView:

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service):
        self.page = 0
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_recordings_service = voice_recordings_service
        self.choosen_model = tk.IntVar()
        self.choosen_model.set("1")  # default value
        self.model_entities = self.voice_model_service.select_gender_language(gender, language)
        self.model_labels = []
        self.model_buttons = []
        self.display_models()
        self.next_page_button = tk.Button(width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        if self.has_next_page():
            self.next_page_button = tk.Button(self.root, text="Następna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=("Helvetica", 14))
            self.next_page_button.place(x=WIDTH / 2 + 50, y=150 + MODELS_ON_PAGE * PAD_Y)

        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_menu,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        back_button = tk.Button(self.root, text="Cofnij", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                command=self.switch_to_choose_gender_language_view)
        continue_button = tk.Button(self.root, text="Dalej", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_choose_audio_view)

        main_menu_button.place(x=200, y=700)
        back_button.place(x=800, y=700)
        continue_button.place(x=1400, y=700)

    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_gender_language_module.ChooseGenderLanguageView(self.root, self.voice_model_service,
                                                               self.voice_recordings_service)

    def switch_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_recordings_service)

    def switch_to_choose_audio_view(self):
        pass

    def display_models(self):
        models = self.model_entities[self.page * 10:self.page * 10 + 10]
        for model in models:
            label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                                   text=model["name"], bg='green', font=("Helvetica", 14), variable=self.choosen_model,
                                   value=model["id"])
            label.place(x=WIDTH / 2 - 200, y=150 + len(self.model_labels * PAD_Y))
            self.model_labels.append(label)
            button = tk.Button(self.root, text="Odsłuchaj", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                               font=("Helvetica", 14), command=lambda: self.play_audio(model['id']))
            button.place(x=WIDTH / 2 + 50, y=150 + len(self.model_buttons) * PAD_Y)
            self.model_buttons.append(button)

    def has_next_page(self):
        return len(self.model_entities) > (self.page * 10 + 10)

    def next_page(self):
        for label in self.model_labels:
            label.destroy()
        for button in self.model_buttons:
            button.destroy()
        self.model_labels = []
        self.model_buttons = []
        self.page += 1
        if self.page == 1:
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona", width=BUTTON_WIDTH_2,
                                                  height=BUTTON_HEIGHT_2,
                                                  command=self.previous_page, font=("Helvetica", 14))
            self.previous_page_button.place(x=WIDTH / 2 - 200, y=150 + MODELS_ON_PAGE * PAD_Y)

        if not self.has_next_page():
            self.next_page_button.destroy()
        self.display_models()

    def previous_page(self):
        for label in self.model_labels:
            label.destroy()
        for button in self.model_buttons:
            button.destroy()
        self.model_labels = []
        self.model_buttons = []
        if not self.has_next_page():  # check if there was a next page button before
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=("Helvetica", 14))
            self.next_page_button.place(x=WIDTH / 2 + 50, y=150 + MODELS_ON_PAGE * PAD_Y)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_models()


def play_audio(self, id):
    if voice_recording := self.voice_recordings_service.select_voice_recordings(name='basic', model_id=id)[0]:
        playsound(voice_recording['path'])
    else:
        print('error')
