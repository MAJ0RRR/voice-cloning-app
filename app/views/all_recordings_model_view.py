from lazy_import import lazy_module
from tkinter import messagebox
import os
import pygame
import tkinter as tk

from app.views.basic.basic_view import BasicView
from app.views.generate_recordings_view import GenerateRecordingsView

choose_voice_model_module = lazy_module('app.views.choose_voice_model_view')


class AllRecordingsModelView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_recordings_service, version_service, model_id,
                 option):
        super(AllRecordingsModelView, self).__init__(root, voice_model_service, voice_recordings_service,
                                                     version_service)
        self.page = 0
        self.PAD_Y = 1.333 * self.size_grid_y
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.option = option
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.recordings_entities = self.voice_recordings_service.select_voice_recordings(model_id=model_id)
        self.recording_labels = []
        self.recording_buttons = []
        self.display_widgets()
        self.display_recordings()

        self.next_page_button = None
        if self.has_next_page():
            self.next_page_button = tk.Button(self.root, text="Następna strona", width=self.BUTTON_WIDTH_2,
                                              height=self.BUTTON_HEIGHT_2,
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=self.WIDTH / 2 + 1.66 * self.size_grid_x,
                                        y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y)

    def display_widgets(self):
        model = self.voice_model_service.select_by_id(self.model_id)
        label = tk.Label(self.root, bg=self.BACKGROUND_COLOR, font=self.MAX_FONT,
                         text=f"Wszystkie próbki modelu {model['name']}")
        label.pack(pady=self.PAD_Y)
        frame = tk.Frame(self.root, bg='white', width=15 * self.size_grid_x, height=self.size_grid_y * 17)
        frame.pack()  # place for models
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view)
        back_button = tk.Button(self.root, text="Cofnij",
                                command=self.switch_to_choose_model, font=self.BUTTON_FONT)
        generate_new_sample_button = tk.Button(self.root, text="Generuj nową próbkę",
                                               command=self.switch_to_generate_recording,
                                               font=self.BUTTON_FONT)

        main_menu_button.place(x=self.WIDTH / 2 - 3 * self.BUTTON_WIDTH_1 / 2 - self.size_grid_x * 2,
                               y=23.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        back_button.place(x=self.WIDTH / 2 - self.BUTTON_WIDTH_1 / 2, y=23.333 * self.size_grid_y,
                          width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        generate_new_sample_button.place(x=self.WIDTH / 2 + self.BUTTON_WIDTH_1 / 2 + self.size_grid_x * 2,
                                         y=23.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                                         height=self.BUTTON_HEIGHT_1)

    def switch_to_choose_model(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_module.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                       self.voice_recordings_service,
                                                       self.version_service, self.option)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()

    def switch_to_generate_recording(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        GenerateRecordingsView(self.root, self.gender, self.language, self.voice_model_service,
                               self.voice_recordings_service, self.version_service, self.model_id, self.option)

    def display_recordings(self):
        recordings = self.recordings_entities[self.page * 10:self.page * 10 + 10]
        for recording in recordings:
            label = tk.Label(self.root, activebackground='white', highlightthickness=0, highlightcolor='white',
                             text=recording["name"], bg='white', font=self.BUTTON_FONT)
            label.place(x=self.WIDTH / 2 - 7 * self.size_grid_x,
                        y=self.Y_FIRST_MODEL + len(self.recording_labels) * self.PAD_Y)
            self.recording_labels.append(label)
            button = tk.Button(self.root, text="Odsłuchaj",
                               font=self.BUTTON_FONT, command=lambda: self.play_audio(recording['path']))
            button.place(x=self.WIDTH / 2 + 1 * self.size_grid_x,
                         y=self.Y_FIRST_MODEL + len(self.recording_buttons) * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                         height=self.BUTTON_HEIGHT_2, )
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
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona",
                                                  command=self.previous_page, font=self.BUTTON_FONT)
            self.previous_page_button.place(x=self.WIDTH / 2 - 6.667 * self.size_grid_x,
                                            y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y, width=self.BUTTON_WIDTH_2,
                                            height=self.BUTTON_HEIGHT_2)

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
            self.next_page_button = tk.Button(self.root, text="Nastepna strona",
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=self.WIDTH / 2 + 1.667 * self.size_grid_x, width=self.BUTTON_WIDTH_2,
                                        height=self.BUTTON_HEIGHT_2,
                                        y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_recordings()

    def play_audio(self, path):
        if os.path.isfile(path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        else:
            print('error')
