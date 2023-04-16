from lazy_import import lazy_module
import pygame
import shutil
import tkinter as tk
from tkinter import messagebox

from app.enums import Options
from app.views.basic.basic_view import BasicView

choose_gender_language_module = lazy_module("choose_gender_language.view")
choose_audio_module = lazy_module("app.views.choose_audio_view")
generate_recordings_module = lazy_module("app.views.generate_recordings_view")
all_recording_module = lazy_module("app.views.all_recordings_model_view")


class ChooseVoiceModelView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service, version_service, option):
        super(ChooseVoiceModelView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.page = 0
        self.PAD_Y = 1.333 * self.size_grid_y
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.option = option
        self.gender = gender
        self.language = language
        self.model_entities = self.voice_model_service.select_gender_language(gender, language)
        self.choosen_model = tk.IntVar()
        if len(self.model_entities) > 0:
            self.choosen_model.set(self.model_entities[0]['id'])  # default value
        self.model_labels = []
        self.model_buttons = []
        self.display_widgets()
        self.display_models()
        self.next_page_button = None
        if self.has_next_page():
            self.next_page_button = tk.Button(self.root, text="Następna strona", width=self.BUTTON_WIDTH_2,
                                              height=self.BUTTON_HEIGHT_2,
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=self.WIDTH / 2 + 1.666 * self.size_grid_x,
                                        y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()

    def display_widgets(self):
        label = tk.Label(self.root, bg=self.BACKGROUND_COLOR, font=self.MAX_FONT, text='Wybierz model głosu')
        label.pack(pady=self.PAD_Y)
        frame = tk.Frame(self.root, width=self.size_grid_x * 25, height=16.5 * self.size_grid_y, bg='white')
        frame.pack()  # place for models
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     font=self.BUTTON_FONT)
        back_button = tk.Button(self.root, text="Cofnij", command=self.switch_to_choose_gender_language,
                                font=self.BUTTON_FONT)
        continue_button = tk.Button(self.root, text="Dalej",
                                    command=self.switch_to_next_view, font=self.BUTTON_FONT)

        main_menu_button.place(x=self.WIDTH / 2 - 3 * self.BUTTON_WIDTH_1 / 2 - self.size_grid_x * 2,
                               y=23.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1, )
        back_button.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=23.333 * self.size_grid_y,
                          width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1, )
        continue_button.place(x=self.WIDTH / 2 + self.BUTTON_WIDTH_1 / 2 + self.size_grid_x * 2,
                              y=23.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1, )

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
                                                              self.voice_recordings_service, self.version_service,
                                                              model_id,
                                                              self.option)
        else:
            if self.option == Options.train_new:
                model_id = None
            choose_audio_module.ChooseAudioView(self.root, self.voice_model_service, self.voice_recordings_service,
                                                self.version_service, self.option,
                                                self.language, self.gender, model_id)

    def display_models(self):
        models = self.model_entities[self.page * 10:self.page * 10 + 10]
        for model in models:
            label = tk.Radiobutton(self.root, activebackground='white', highlightthickness=0, highlightcolor='white',
                                   text=model["name"], bg='white', font=self.BUTTON_FONT, variable=self.choosen_model,
                                   value=model["id"])
            label.place(x=self.WIDTH / 2 - 11 * self.size_grid_x,
                        y=self.Y_FIRST_MODEL + len(self.model_labels) * self.PAD_Y)
            self.model_labels.append(label)
            id = model['id']
            button = tk.Button(self.root, text="Odsłuchaj",
                               font=self.BUTTON_FONT, command=self.create_play_audio_function(id))
            button.place(x=self.WIDTH / 2 - 2 * self.size_grid_x,
                         y=self.Y_FIRST_MODEL + (len(self.model_labels) - 1) * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                         height=self.BUTTON_HEIGHT_2, )
            button_2 = tk.Button(self.root, text="Więcej próbek",
                                 font=self.BUTTON_FONT, command=self.create_switch_to_recordings_function(id))
            button_2.place(x=self.WIDTH / 2 + 5 * self.size_grid_x,
                           y=self.Y_FIRST_MODEL + (len(self.model_labels) - 1) * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                           height=self.BUTTON_HEIGHT_2, )
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
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona",
                                                  command=self.previous_page, font=self.BUTTON_FONT)
            self.previous_page_button.place(x=self.WIDTH / 2 - 8 * self.size_grid_x,
                                            y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                                            height=self.BUTTON_HEIGHT_2, )

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
            self.next_page_button = tk.Button(self.root, text="Nastepna strona",
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=self.WIDTH / 2 + 3 * self.size_grid_x,
                                        y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                                        height=self.BUTTON_HEIGHT_2, )
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_models()

    def switch_to_recordings_of_model(self, model_id):
        for widget in self.root.winfo_children():
            widget.destroy()
        all_recording_module.AllRecordingsModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                    self.voice_recordings_service, self.version_service, model_id,
                                                    self.option)

    def play_audio(self, id):
        pygame.mixer.music.stop()
        if voice_recording := self.voice_recordings_service.select_voice_recordings(name='basic', model_id=id)[0]:
            pygame.mixer.music.load(voice_recording['path'])
            pygame.mixer.music.play()
        else:
            print('error')
