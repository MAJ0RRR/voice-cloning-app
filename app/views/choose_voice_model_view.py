import tkinter as tk
import playsound

from lazy_import import lazy_module
from app.components.listbox_with_button import ListBoxWithButton


choose_gender_language_module = lazy_module("app.views.choose_gender_language_view")
main_menu_module = lazy_module("app.views.main_view")
WIDTH = 1920
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PLAY_BUTTON_WIDTH = 10
PLAY_BUTTON_HEIGHT = 1
PAD_Y = 40
MODELS_ON_PAGE = 10


class ChooseVoiceModelView:

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service):
        self.page = 0
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_recordings_service = voice_recordings_service
        self.model_entities = self.voice_model_service.select_gender_language(gender, language)
        self.model_labels = []
        self.model_buttons = []
        self.display_models()
        if self.has_next_page():
            pass # create button

        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_menu, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        back_button = tk.Button(self.root, text="Cofnij",width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.switch_to_choose_gender_language_view)
        continue_button = tk.Button(self.root, text="Dalej",width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.switch_to_choose_audio_view)
#
        main_menu_button.place(x=200, y=700)
        back_button.place(x=800, y=700)
        continue_button.place(x=1400, y=700)

    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_gender_language_module.ChooseGenderLanguageView(self.root)

    def switch_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_records_service)

    def switch_to_choose_audio_view(self):
        pass

    def display_models(self):
       models =self.model_entities[self.page*10:self.page*10+10]
       for model in models:
           label = tk.Label(self.root, text=model["name"], bg='green', font=("Helvetica", 14))
           label.place(x=WIDTH/2-200, y=150+len(self.model_labels*PAD_Y))
           self.model_labels.append(label)
           button = tk.Button(self.root, text="Odsłuchaj", width=PLAY_BUTTON_WIDTH, height=PLAY_BUTTON_HEIGHT,font=("Helvetica", 14), command=lambda: self.play_audio(model.id))
           button.place(x=WIDTH/2+50, y=150 + len(self.model_buttons)*PAD_Y)
           self.model_buttons.append(button)

    def has_next_page(self):
        return len(self.model_entities) > (self.page * 10 + 10)

    def next_page(self):
        pass
        #delete all models labels and buttons
        #increase self.page
        #check if need to add previous page
        #check if need to destroy next_page_button
        #display models


    def previous_page(self):
        pass
    # delete all models labels and buttons
    # idecrease self.page
    # check if need to add next page
    # check if need to destroy previous_page_button
    # display models


    def play_audio(self, id):
        if voice_recording := self.voice_recordings_service.select_voice_recordings(name='basic', model_id=id):
            playsound(voice_recording['path'])
        else:
            print('error')







