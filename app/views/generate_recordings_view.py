from lazy_import import lazy_module
import os
import pygame
import queue
import tkinter as tk
from tkinter import messagebox
import threading

from app.entities.voice_recording import VoiceRecording
from app.speech_synthesizer import SpeechSynthesizer
from app.views.basic.basic_view import BasicView

all_recordings_model_module = lazy_module('app.views.all_recordings_model_view')
choose_voice_model_module = lazy_module('app.views.choose_voice_model_view')


class GenerateRecordingsView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_records_service, version_service, model_id,
                 option):
        super(GenerateRecordingsView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.option = option
        self.PAD_Y_2 = 1.333*self.size_grid
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.model = self.voice_model_service.select_by_id(model_id)
        self.input_field = tk.Entry(root, width=60, font=self.BUTTON_FONT)
        self.input_field.place(x=3.333*self.size_grid, y=3 * self.PAD_Y)
        self.recording_entities = []
        self.recording_labels = []
        self.recording_buttons = []
        self.stop = False
        self.previous_page_button = None
        self.next_page_button = None
        self.speech_synthesizer = SpeechSynthesizer(self.model)
        self.popup = None
        self.page = 0
        self.event = threading.Event()
        self.thread = None
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()
        self.display_widgets()

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy chcesz zakmnąć program? "):
            self.root.destroy()
            self.event.set()
            self.thread.join()
            if self.speech_synthesizer:
                self.speech_synthesizer.stop_event.set()

    def display_widgets(self):
        label = tk.Label(self.root, text=f"Model {self.model['name']}", font=self.MAX_FONT, bg='green')
        label.place(x=4.16*self.size_grid, y=self.PAD_Y)
        label = tk.Label(self.root, text="Wpisz tekst, aby syntezować mowę", font=self.MAX_FONT, bg='green')
        label.place(x=4.16*self.size_grid, y=2 * self.PAD_Y)
        generate_button = tk.Button(self.root, text="Generuj audio", command=self.generate_audio, font=self.BUTTON_FONT)
        generate_button.place(x=10*self.size_grid, y=4 * self.PAD_Y)
        label = tk.Label(self.root, text="Wygenerowane próbki", font=self.MAX_FONT, bg='green')
        label.place(x=30*self.size_grid, y=self.PAD_Y)
        frame = tk.Frame(self.root, width=27.333*self.size_grid, height=16.667*self.size_grid, bg='white')
        frame.place(x=30*self.size_grid - 10, y=self.PAD_Y + 2*self.size_grid)  # place for files
        model_list_button = tk.Button(self.root, text="Lista modeli głosu", command=self.switch_to_choose_model,
                                      font=self.BUTTON_FONT, width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        main_menu_button = tk.Button(self.root, text="Menu główne", font=self.BUTTON_FONT, command=self.switch_to_main_view,
                                     width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        all_recordings_button = tk.Button(self.root, text="Wszystkie nagrania modelu",
                                          command=self.switch_to_recordings_of_model, font=self.BUTTON_FONT,
                                          width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        main_menu_button.place(x=6.667*self.size_grid, y=23.333*self.size_grid)
        all_recordings_button.place(x=26.667*self.size_grid, y=23.333*self.size_grid)
        model_list_button.place(x=46.667*self.size_grid, y=23.333*self.size_grid)

    def switch_to_main_view(self):
        self.event.set()
        self.thread.join()
        super().switch_to_main_view()

    def switch_to_choose_model(self):
        self.event.set()
        self.thread.join()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_module.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                       self.voice_recordings_service,
                                                       self.version_service, self.option)

    def switch_to_recordings_of_model(self):
        self.event.set()
        self.thread.join()
        for widget in self.root.winfo_children():
            widget.destroy()
        all_recordings_model_module.AllRecordingsModelView(self.root, self.gender, self.language,
                                                           self.voice_model_service,
                                                           self.voice_recordings_service, self.version_service,
                                                           self.model_id, self.option)

    def generate_audio(self):
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen which is app
        text = self.input_field.get()
        if not text:
            messagebox.showerror(title="Błąd", message="Nie wprowadzono tekstu do syntezy")
            return
        output_name = self.speech_synthesizer.generate_sample_name()
        self.q.put(lambda: self.speech_synthesizer.generate_audio(output_name, text, self.finish_sythesize), ())
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT)}+{int(x)}+{int(y)}")
        self.popup.title("Trwa proces")
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_process)
        label = tk.Label(self.popup, text="Aby przerwać syntezę kliknij anuluj.")
        label.pack(padx=10, pady=10)

        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_process)
        cancel_button.pack(padx=10, pady=10)

    def cancel_process(self):
        confirm = messagebox.askyesno("Przerwanie syntezowania", "Czy na pewno chcesz przerwać syntezę głosu?", parent=self.popup)

        if confirm:
            self.popup.destroy()
            self.stop = True
            self.speech_synthesizer.stop_event.set()

    def finish_sythesize(self, output_path):
        self.root.after(0, lambda: self.after_synthesis(output_path))

    def after_synthesis(self, output_path):
        if self.stop:
            self.stop = False
            return
        filename = os.path.basename(output_path)
        recording = {'name': filename, "path": output_path, "model_id": self.model_id}
        recording = self.save_recording_to_db(recording)
        self.recording_entities.append(recording)
        self.add_recording_label(recording)
        self.popup.destroy()

    def save_recording_to_db(self, recording):
        voice_recording = VoiceRecording(recording['name'], recording['path'], recording['model_id'])
        recording['id'] = self.voice_recordings_service.insert(voice_recording)
        return recording

    def add_recording_label(self, recording):
        if len(self.recording_entities) > ((self.page + 1) * self.PAGING):
            if self.next_page_button:
                return
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=self.BUTTON_WIDTH_2,
                                              height=self.BUTTON_HEIGHT_2,
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=45*self.size_grid, y=self.FIRST_MODEL + self.PAGING * self.PAD_Y_2)
            return
        self.display_recording(recording)

    def display_recording(self, recording):
        label = tk.Label(self.root, text=recording["name"], bg='white', font=self.BUTTON_FONT)
        label.place(x=30*self.size_grid, y=self.Y_FIRST_MODEL + len(self.recording_labels) * self.PAD_Y_2)
        self.recording_labels.append(label)
        button = tk.Button(self.root, text="Odsłuchaj", width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2,
                           font=self.BUTTON_FONT, command=lambda: self.play_audio(recording['id']))
        button.place(x=40*self.size_grid, y=self.Y_FIRST_MODEL + (len(self.recording_labels) - 1) * self.PAD_Y_2)
        button_2 = tk.Button(self.root, text="Usuń", width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2,
                             font=self.BUTTON_FONT, command=lambda: self.delete_recording(recording['id']))
        button_2.place(x=50*self.size_grid, y=self.Y_FIRST_MODEL + (len(self.recording_labels) - 1) * self.PAD_Y_2)
        self.recording_buttons.append(button)
        self.recording_buttons.append(button_2)

    def display_recordings(self):
        recordings = self.recording_entities[self.page * 10:self.page * 10 + 10]
        for recording in recordings:
            self.display_recording(recording)

    def delete_recording(self, recording_id):
        for entity in self.recording_entities:
            if entity['id'] == recording_id:
                self.recording_entities.remove(entity)
        self.delete_recording_from_db(recording_id)
        self.delete_all_recordings_labels_buttons()
        self.display_recordings()

    def delete_recording_from_db(self, recording_id):
        self.voice_recordings_service.delete_by_id(recording_id)

    def has_next_page(self):
        return len(self.recording_entities) > (self.page * 10 + 10)

    def delete_all_recordings_labels_buttons(self):
        for label in self.recording_labels:
            label.destroy()
        for button in self.recording_buttons:
            button.destroy()
        self.recording_labels = []
        self.recording_buttons = []

    def next_page(self):
        self.delete_all_recordings_labels_buttons()
        self.page += 1
        if self.page == 1:
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona", width=self.BUTTON_WIDTH_2,
                                                  height=self.BUTTON_HEIGHT_2,
                                                  command=self.previous_page, font=self.BUTTON_FONT)
            self.previous_page_button.place(x=38.333*self.size_grid, y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y_2)

        if not self.has_next_page():
            self.next_page_button.destroy()
        self.display_recordings()

    def previous_page(self):
        self.delete_all_recordings_labels_buttons()
        if not self.has_next_page():  # check if there was a next page button before
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=self.BUTTON_WIDTH_2,
                                              height=self.BUTTON_HEIGHT_2,
                                              command=self.next_page, font=self.BUTTON_FONT)
            self.next_page_button.place(x=45*self.size_grid, y=self.Y_FIRST_MODEL + self.PAGING * self.PAD_Y_2)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_recordings()

    def play_audio(self, recording_id):
        pygame.mixer.music.stop()
        if voice_recording := self.voice_recordings_service.select_by_id(recording_id):
            pygame.mixer.music.load(voice_recording['path'])
            pygame.mixer.music.play()
        else:
            print('error')

    def worker(self, q):
        while (True):
            if self.event.is_set():
                return
            try:
                func = q.get(block=False, timeout=5)
                if func is not None:
                    func()
                    q.task_done()
            except:
                pass
