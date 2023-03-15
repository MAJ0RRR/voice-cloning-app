from lazy_import import lazy_module
import os
import playsound
import queue
import tkinter as tk
from tkinter import messagebox
import threading

from app.entities.voice_recording import VoiceRecording
from app.speech_synthesizer import SpeachSynthesizer
from app.views.basic.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT, MAX_FONT, PAGING, \
    BUTTON_HEIGHT_2, BUTTON_WIDTH_2, Y_FIRST_MODEL, WIDTH, POPUP_WIDTH, HEIGHT, POPUP_HEIGHT

all_recordings_model_module = lazy_module('app.views.all_recordings_model_view')
choose_voice_model_module = lazy_module('app.views.choose_voice_model_view')

PAD_Y_2 = 40


class GenerateRecordingsView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_records_service, version_service, model_id,
                 option):
        super(GenerateRecordingsView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.option = option
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.model = self.voice_model_service.select_by_id(model_id)
        self.input_field = tk.Entry(root, width=60, font=BUTTON_FONT)
        self.input_field.place(x=100, y=3 * PAD_Y)

        self.recording_entities = []
        self.recording_labels = []
        self.recording_buttons = []
        self.stop = False
        self.previous_page_button = None
        self.next_page_button = None
        self.speech_synthesizer = SpeachSynthesizer(self.model)
        self.popup = None
        self.page = 0
        self.thread = None
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()

    def display_widgets(self):
        label = tk.Label(self.root, text=f"Model {self.model['name']}", font=MAX_FONT, bg='green')
        label.place(x=290, y=PAD_Y)
        label = tk.Label(self.root, text="Wpisz tekst, aby syntezować mowę", font=MAX_FONT, bg='green')
        label.place(x=125, y=2 * PAD_Y)
        generate_button = tk.Button(self.root, text="Generuj audio", command=self.generate_audio, font=BUTTON_FONT)
        generate_button.place(x=300, y=4 * PAD_Y)
        label = tk.Label(self.root, text="Wygenerowane próbki", font=MAX_FONT, bg='green')
        label.place(x=900, y=PAD_Y)
        model_list_button = tk.Button(self.root, text="Lista modeli głosu", command=self.switch_to_choose_model,
                                      font=BUTTON_FONT, width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        main_menu_button = tk.Button(self.root, text="Menu główne", font=BUTTON_FONT, command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        all_recordings_button = tk.Button(self.root, text="Wszystkie nagrania modelu",
                                          command=self.switch_to_recordings_of_model, font=BUTTON_FONT,
                                          width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1)
        main_menu_button.place(x=200, y=700)
        all_recordings_button.place(x=800, y=700)
        model_list_button.place(x=1400, y=700)

    def switch_to_choose_model(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_module.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                       self.voice_recordings_service,
                                                       self.version_service, self.option)

    def switch_to_recordings_of_model(self):
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
        x = (WIDTH - POPUP_WIDTH) // 2 + screen_pos
        y = (HEIGHT - POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        self.popup.title("Trwa proces")

        label = tk.Label(self.popup, text="Aby przerwać syntezę kliknij anuluj.")
        label.pack(padx=10, pady=10)

        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_process)
        cancel_button.pack(padx=10, pady=10)

    def cancel_process(self):
        confirm = messagebox.askyesno("Przerwanie syntezowania", "Czy na pewno chcesz przerwać syntezę głosu?")

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
        if len(self.recording_entities) > ((self.page + 1) * PAGING):
            if self.next_page_button:
                return
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=1350, y=Y_FIRST_MODEL + PAGING * PAD_Y_2)
            return
        self.display_recording(recording)

    def display_recording(self, recording):
        label = tk.Label(self.root, text=recording["name"], bg='green', font=BUTTON_FONT)
        label.place(x=900, y=Y_FIRST_MODEL + len(self.recording_labels) * PAD_Y_2)
        self.recording_labels.append(label)
        button = tk.Button(self.root, text="Odsłuchaj", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                           font=BUTTON_FONT, command=lambda: self.play_audio(recording['id']))
        button.place(x=1200, y=Y_FIRST_MODEL + (len(self.recording_labels) - 1) * PAD_Y_2)
        button_2 = tk.Button(self.root, text="Usuń", width=BUTTON_WIDTH_2, height=BUTTON_HEIGHT_2,
                             font=BUTTON_FONT, command=lambda: self.delete_recording(recording['id']))
        button_2.place(x=1500, y=Y_FIRST_MODEL + (len(self.recording_labels) - 1) * PAD_Y_2)
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
            self.previous_page_button = tk.Button(self.root, text="Poprzednia strona", width=BUTTON_WIDTH_2,
                                                  height=BUTTON_HEIGHT_2,
                                                  command=self.previous_page, font=BUTTON_FONT)
            self.previous_page_button.place(x=1150, y=Y_FIRST_MODEL + PAGING * PAD_Y_2)

        if not self.has_next_page():
            self.next_page_button.destroy()
        self.display_recordings()

    def previous_page(self):
        self.delete_all_recordings_labels_buttons()
        if not self.has_next_page():  # check if there was a next page button before
            self.next_page_button = tk.Button(self.root, text="Nastepna strona", width=BUTTON_WIDTH_2,
                                              height=BUTTON_HEIGHT_2,
                                              command=self.next_page, font=BUTTON_FONT)
            self.next_page_button.place(x=1350, y=Y_FIRST_MODEL + PAGING * PAD_Y_2)
        self.page -= 1
        if self.page == 0:
            self.previous_page_button.destroy()
        self.display_recordings()

    def play_audio(self, recording_id):
        if voice_recording := self.voice_recordings_service.select_by_id(recording_id):
            playsound.playsound(voice_recording['path'])
        else:
            print('error')

    def worker(self, q):
        while True:
            func = q.get()
            if func is not None:
                func()
                q.task_done()
