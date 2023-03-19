from lazy_import import lazy_module
from tkinter import messagebox
import os
from playsound import playsound
import tkinter as tk

from app.views.basic.basic_view import BasicView, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, BUTTON_HEIGHT_2, BUTTON_WIDTH_2, \
    PAGING, WIDTH, BUTTON_FONT, Y_FIRST_MODEL
from app.views.generate_recordings_view import GenerateRecordingsView

choose_voice_model_module = lazy_module('app.views.choose_voice_model_view')
PAD_Y = 40


class AllRecordingsModelView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service, version_service, model_id,
                 option):
        super(AllRecordingsModelView, self).__init__(root, voice_model_service, voice_recordings_service,
                                                     version_service)
        self.page = 0
        self.option = option
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.recordings_entities = self.voice_recordings_service.select_voice_recordings(model_id=model_id)
        self.recording_labels = []
        self.recording_buttons = []
        self.display_recordings()
        self.display_widgets()
        self.next_page_button = None
        if self.has_next_page():
            self.next_page_button = tk.Button(self.root, text="Następna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=WIDTH / 2 + 50, y=Y_FIRST_MODEL + PAGING * PAD_Y)

    def display_widgets(self):
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        back_button = tk.Button(self.root, text="Cofnij", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                                command=self.switch_to_choose_model)
        generate_new_sample_button = tk.Button(self.root, text="Generuj nową próbkę", width=BUTTON_WIDTH_1,
                                               height=BUTTON_HEIGHT_1, command=self.switch_to_generate_recording)

        main_menu_button.place(x=200, y=700)
        back_button.place(x=800, y=700)
        generate_new_sample_button.place(x=1400, y=700)

    def switch_to_choose_model(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_module.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                       self.voice_recordings_service,
                                                       self.version_service, self.option)

    def switch_to_generate_recording(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        GenerateRecordingsView(self.root, self.gender, self.language, self.voice_model_service,
                               self.voice_recordings_service, self.version_service, self.model_id, self.option)

    def display_recordings(self):
        recordings = self.recordings_entities[self.page * 10:self.page * 10 + 10]
        for recording in recordings:
            label = tk.Label(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                             text=recording["name"], bg='green', font=BUTTON_FONT)
            label.place(x=WIDTH / 2 - 200, y=Y_FIRST_MODEL + len(self.recording_labels) * PAD_Y)
            self.recording_labels.append(label)
            button = tk.Button(self.root, text="Odsłuchaj", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                               font=BUTTON_FONT, command=lambda: self.play_audio(recording['path']))
            button.place(x=WIDTH / 2 + 50, y=Y_FIRST_MODEL + len(self.recording_buttons) * PAD_Y)
            self.recording_buttons.append(button)

    def cancel_process(self):
        confirm = messagebox.askyesno("Przerwanie syntezowania", "Czy na pewno chcesz przerwać syntezę głosu?")

        if confirm:
            self.popup.destroy()
            self.stop = True
            self.speech_synthesizer.stop_event.set()

    def has_next_page(self):
        return len(self.recordings_entities) > (self.page * 10 + 10)

    def next_page(self):
        for label in self.recording_labels:
            label.destroy()
        for button in self.recording_buttons:
            button.destroy()
        self.recording_labels = []
        self.recording_buttons = []
        self.page += 1
        if self.page == 1:
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona", width=BUTTON_WIDTH_2,
                                                  height=BUTTON_HEIGHT_2,
                                                  command=self.previous_page, font=BUTTON_FONT)
            self.previous_page_button.place(x=WIDTH / 2 - 200, y=Y_FIRST_MODEL + PAGING * PAD_Y)

        if not self.has_next_page():
            self.next_page_button.destroy()
        self.display_recordings()

    def previous_page(self):
        for label in self.recording_labels:
            label.destroy()
        for button in self.recording_buttons:
            button.destroy()
        self.recording_labels = []
        self.recording_buttons = []
        if not self.has_next_page():  # check if there was a next page button before
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=WIDTH / 2 + 50, y=Y_FIRST_MODEL + PAGING * PAD_Y)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_recordings()

    def play_audio(self, path):
        if os.path.isfile(path):
            playsound(path)
        else:
            print('error')
