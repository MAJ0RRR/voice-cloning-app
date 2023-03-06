from noise import remove_noise
import os
from pathlib import Path
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox as mb

from app.settings import WORKING_DIR, RAW_AUDIO_DIR
from app.views.basic.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT, MAX_FONT
from whispertrans import create_transcription


class GenerateSamplesBasicView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service):
        super(GenerateSamplesBasicView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        label = tk.Label(self.root, font=MAX_FONT, text='Próbki są przygotowywane', bg='green')
        label.pack(pady=PAD_Y)
        cancel_button = tk.Button(self.root, text='Anuluj', font=BUTTON_FONT, command=self.cancel, width=BUTTON_WIDTH_1,
                                  height=BUTTON_HEIGHT_1)
        cancel_button.pack(pady=PAD_Y)
        self.stop_event = threading.Event()
        self.stop = False
        self.root.update()
        self.start_generate_samples()

    def cancel(self):
        res = mb.askquestion('Przerwanie tworzenia próbek', 'Czy na pewno chcesz zakończyć tworzenie próbek')
        if res == 'yes':
            self.stop = True
            self.stop_event.set()

    def generate_samples(self, callback, event):
        path = Path(WORKING_DIR)
        process = subprocess.Popen(["sh", "../splits.sh", path.parent.absolute()])
        while process.poll() is None:
            if event.is_set():
                process.terminate()
        if not event.is_set():
            version = self.version_service.get_version()
            path_splits = os.path.join(path.parent.absolute(), "audiofiles/splits")
            remove_noise(path_splits, f"dataset{version}", self.stop_event)
        if not event.is_set():
            create_transcription(path.parent.absolute(), f"dataset{version}", self.language, 10) #work on last 2 parameters
        self.version_service.update_version(version, version+1)
        self.delete_files_from_raw_dir()
        callback()


    def delete_files_from_raw_dir(self):
        for file_name in os.listdir(RAW_AUDIO_DIR):
            file_path = os.path.join(RAW_AUDIO_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
