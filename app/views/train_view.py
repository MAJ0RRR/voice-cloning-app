from lazy_import import lazy_module
import os
import shutil
import subprocess
import threading
from time import sleep
import tkinter as tk
from tkinter import messagebox
import webbrowser

from app.enums import Options
from app.settings import OUTPUT_DIR, WORKING_DIR
from app.views.basic.basic_view import BasicView

after_train_module = lazy_module('app.views.after_train_view')
choose_audio_module = lazy_module('app.views.choose_audio_view')


class TrainView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, gender, language, option,
                 gpu, dataset, model_path, model_id=None):
        super(TrainView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.gender = gender
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.model_id = model_id
        self.option = option
        self.language = language
        self.dataset = dataset
        self.gpu = gpu
        self.model_path = model_path
        self.run_name = self.generate_run_name()
        self.popup = None
        self.process = None
        self.event = threading.Event()
        self.start_train()
        self.dir_with_result = ''
        self.thread = threading.Thread(target=self.wait_for_dir)
        self.thread.start()
        self.display_widgets()

    def on_closing(self):
        if messagebox.askokcancel("Wyjście",
                                  "Czy na pewno chcesz zamknąć program? Wszystkie efekty treningu zostaną stracone."):
            self.root.destroy()
            self.event.set()
            if self.thread:
                self.thread.join()
            if self.speech_synthesizer:
                self.speech_synthesizer.stop_event.set()
            if self.process:
                self.process.terminate()
            if self.process2.terminate():
                self.process2.terminate()

    def generate_run_name(self):
        return f"{self.gender}_{self.language}"

    def display_widgets(self):
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen where app is open
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT)}+{int(x)}+{int(y)}")
        self.popup.title("Rozpoczynanie trenowania")
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_before_train)
        label = tk.Label(self.popup, text="Trwa rozpoczynanie trenowania.")
        label.pack(padx=10, pady=10)
        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_before_train)
        cancel_button.pack(padx=10, pady=10)

    def cancel_before_train(self):
        confirm = messagebox.askyesno("Przerwanie przygotowywania trenowania",
                                      "Czy na pewno chcesz przerwać proces trenowania?", parent=self.popup)
        if confirm:
            self.event.set()
            self.popup.destroy()
            self.thread.join()
            self.process.terminate()
            if self.option == Options.retrain:
                self.switch_to_main_view()
            self.switch_to_choose_audio()

    def switch_to_choose_audio(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_audio_module.ChooseAudioView(self.root, self.voice_model_service, self.voice_recordings_service,
                                            self.version_service, self.option,
                                            self.language, self.gender, self.model_id)

    def wait_for_dir(self):
        for i in range(int(2 * 60 / 5)):
            sleep(5)  # check every 5 seconds if event is set or dir_with result is created
            if self.event.is_set():
                return
            self.find_path_to_dir_result()
            if self.dir_with_result:
                self.run_tensorboard()
                self.create_new_popup()
                break
        self.root.after(0, lambda: self.terminate_thread(self.dir_with_result))

    def terminate_thread(self, dir=None):
        if dir:
            self.dir_with_result = dir
        self.thread.join()
        self.thread = None

    def find_path_to_dir_result(self):
        paths = os.listdir(OUTPUT_DIR)
        for path in paths:
            if path.startswith(self.run_name):
                for path2 in os.listdir(os.path.join(OUTPUT_DIR, path)):
                    if path2.startswith('events'):
                        self.dir_with_result = os.path.join(OUTPUT_DIR, path)
                        return

    def run_tensorboard(self):
        self.process2 = subprocess.Popen(["tensorboard", f"--logdir={self.dir_with_result}"])

    def create_new_popup(self):
        for widget in self.popup.winfo_children():
            widget.destroy()
        self.popup.title('Trwa trenowanie głosu')
        link = tk.Label(self.popup, text="Sprawdź rezultat uczenia", fg="blue")
        link.pack(padx=10, pady=10)

        link.bind("<Button-1>", lambda e: self.open_url())
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_while_training)
        cancel_button = tk.Button(self.popup, text="Przerwij trening", command=self.cancel_while_training)
        cancel_button.pack(padx=10, pady=10)

    def open_url(self):
        webbrowser.open_new("http://localhost:6006")

    def cancel_while_training(self):
        confirm = messagebox.askyesno("Przerwanie przygotowywania trenowania",
                                      "Czy na pewno chcesz przerwać proces trenowania?", parent=self.popup)
        if confirm:
            self.popup.destroy()
            self.switch_to_after_train()

    def switch_to_after_train(self):
        self.process.terminate()  # uncomment it
        self.process2.terminate()
        for widget in self.root.winfo_children():
            widget.destroy()
        after_train_module.AfterTrainView(self.root, self.voice_model_service, self.voice_recordings_service,
                                          self.version_service, self.gender, self.language, self.dir_with_result,
                                          self.dataset, self.gpu)

    def start_train(self):
        language = 'pl' if self.language == 'polish' else 'en'
        dataset_path = os.path.join(WORKING_DIR, f'audiofiles/datasets/{self.dataset}')
        if self.model_path:
            self.process = subprocess.Popen(
                ["python", "train.py", '-m', self.model_path, '-n', self.run_name, '-l', language,
                 '-d', dataset_path, '-g', str(self.gpu)])
        else:
            self.process = subprocess.Popen(
                ["python", "train.py", '-n', self.run_name, '-l', language,
                 '-d', dataset_path, '-g', str(self.gpu)])
