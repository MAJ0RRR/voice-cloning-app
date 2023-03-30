from lazy_import import lazy_module
from playsound import playsound
import shutil
import tkinter as tk

from app.enums import Options
from app.views.basic.basic_view import BasicView, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, BUTTON_HEIGHT_2, BUTTON_WIDTH_2, \
    PAGING, WIDTH, BUTTON_FONT, Y_FIRST_MODEL

choose_gender_language_module = lazy_module("choose_gender_language.view")
choose_audio_module = lazy_module("app.views.choose_audio_view")
generate_recordings_module = lazy_module("app.views.generate_recordings_view")
all_recording_module = lazy_module("app.views.all_recordings_model_view")
PAD_Y = 40


class ChooseVoiceModelView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service, version_service, option):
        super(ChooseVoiceModelView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.page = 0
        self.option = option
        self.gender = gender
        self.language = language
        self.model_entities = self.voice_model_service.select_gender_language(gender, language)
        self.choosen_model = tk.IntVar()
        if len(self.model_entities) >0:
            self.choosen_model.set(self.model_entities[0]['id'])  # default value
        self.model_labels = []
        self.model_buttons = []
        self.display_models()
        self.next_page_button = None
        if self.has_next_page():
            self.next_page_button = tk.Button(self.root, text="Następna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=WIDTH / 2 + 50, y=Y_FIRST_MODEL + PAGING * PAD_Y)
        self.display_widgets()

    def display_widgets(self):
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        back_button = tk.Button(self.root, text="Cofnij", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                command=self.switch_to_choose_gender_language)
        continue_button = tk.Button(self.root, text="Dalej", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_next_view)

        main_menu_button.place(x=200, y=700)
        back_button.place(x=800, y=700)
        continue_button.place(x=1400, y=700)

    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_gender_language_module.ChooseGenderLanguageView(self.root, self.voice_model_service,
                                                               self.voice_recordings_service, self.version_service,
                                                               self.option)

    def switch_to_next_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        model_id = self.choosen_model.get()
        if self.option == Options.synthesize_speech:
            generate_recordings_module.GenerateRecordingsView(self.root, self.gender, self.language,
                                                          self.voice_model_service,
                                                          self.voice_recordings_service, self.version_service, model_id,
                                                          self.option)
        else:
            if self.option == Options.train_new:
                model_id = None
        choose_audio_module.ChooseAudioView(self.root, self.voice_model_service, self.voice_recordings_service,
                                                self.version_service, self.option,
                                                self.language,  self.gender,model_id)


    def display_models(self):
        models = self.model_entities[self.page * 10:self.page * 10 + 10]
        for model in models:
            label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                                   text=model["name"], bg='green', font=BUTTON_FONT, variable=self.choosen_model,
                                   value=model["id"])
            label.place(x=WIDTH / 2 - 350, y=Y_FIRST_MODEL + len(self.model_labels) * PAD_Y)
            self.model_labels.append(label)
            id = model['id']
            button = tk.Button(self.root, text="Odsłuchaj", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                               font=BUTTON_FONT, command=self.create_play_audio_function(id))
            button.place(x=WIDTH / 2 - 100, y=Y_FIRST_MODEL + (len(self.model_labels) - 1) * PAD_Y)
            button_2 = tk.Button(self.root, text="Więcej próbek", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                                 font=BUTTON_FONT, command=self.create_switch_to_recordings_function(id))
            button_2.place(x=WIDTH / 2 + 200, y=Y_FIRST_MODEL + (len(self.model_labels) - 1) * PAD_Y)
            self.model_buttons.append(button)
            self.model_buttons.append(button_2)

    def create_play_audio_function(self, id):
        def play_audio_function():
            self.play_audio(id)

        return play_audio_function

    def create_switch_to_recordings_function(self, id):
        def switch_to_recordings_function():
            self.switch_to_recordings_of_model(id)

        return switch_to_recordings_function

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
                                                  command=self.previous_page, font=BUTTON_FONT)
            self.previous_page_button.place(x=WIDTH / 2 - 200, y=Y_FIRST_MODEL + PAGING * PAD_Y)

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
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=WIDTH / 2 + 50, y=Y_FIRST_MODEL + PAGING * PAD_Y)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_models()

    def switch_to_recordings_of_model(self, model_id):
        for widget in self.root.winfo_children():
            widget.destroy()
        all_recording_module.AllRecordingsModelView(self.root, self.gender, self.language, self.voice_model_service,
                               self.voice_recordings_service, self.version_service, model_id, self.option)

    def play_audio(self, id):
        if voice_recording := self.voice_recordings_service.select_voice_recordings(name='basic', model_id=id)[0]:
            playsound(voice_recording['path'])
        else:
            print('error')
