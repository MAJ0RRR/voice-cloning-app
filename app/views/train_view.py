from lazy_import import lazy_module
import os
import shutil
import subprocess
import threading
from time import sleep
import tkinter as tk
from tkinter import messagebox
import webbrowser

from app.settings import OUTPUT_DIR, WORKING_DIR
from app.views.basic.basic_view import BasicView, WIDTH, HEIGHT, POPUP_HEIGHT, POPUP_WIDTH

after_train_module = lazy_module('app.views.after_train_view')


class TrainView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, gender, language, option,
                 gpu, dataset,
                 model_path):
        super(TrainView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.gender = gender
        self.option = option
        self.language = language
        self.dataset = dataset
        self.gpu = gpu
        self.model_path = model_path
        self.run_name = self.generate_run_name()
        self.popup = None
        self.process = None
        self.start_train()
        self.dir_with_result = './output/tescik-March-27-2023_07+02PMf71a482'
        self.thread = threading.Thread(target=self.wait_for_dir)
        self.thread.start()
        self.display_widgets()


    def generate_run_name(self):
        return f"{self.gender}_{self.language}"

    def display_widgets(self):
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen where app is open
        x = (WIDTH - POPUP_WIDTH) // 2 + screen_pos
        y = (HEIGHT - POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        self.popup.title("Rozpoczynanie trenowania")
        label = tk.Label(self.popup, text="Trwa rozpoczynanie trenowania.")
        label.pack(padx=10, pady=10)
        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_before_train)
        cancel_button.pack(padx=10, pady=10)

    def cancel_before_train(self):
        confirm = messagebox.askyesno("Przerwanie przygotowywania trenowania",
                                      "Czy na pewno chcesz przerwać proces trenowania?")
        if confirm:
            self.popup.destroy()
            self.thread.join()
            self.switch_to_choose_audio()

    def switch_to_choose_audio(self):
        pass

    def wait_for_dir(self):
        while (True):
            sleep(30)  # creating this files lasts about 2 minutes uncommment
            self.find_path_to_dir_result()
            if self.dir_with_result:
                self.run_tensorboard()
                self.create_new_popup()
                break
        self.root.after(0, self.terminate_thread)

    def terminate_thread(self):
        self.thread.join()

    def find_path_to_dir_result(self):
        paths = os.listdir(OUTPUT_DIR)
        for path in paths:
            if path.startswith(self.run_name):
                return path

    def run_tensorboard(self):
        self.dir_with_result = self.find_path_to_dir_result()
        self.process2 = subprocess.Popen(["tensorboard", f"--logdir={self.dir_with_result}"])
        # kill process after finishing training

    def create_new_popup(self):
        for widget in self.popup.winfo_children():
            widget.destroy()
        self.popup.title('Trwa trenowanie głosu')
        link = tk.Label(self.popup, text="Sprawdź rezultat uczenia", fg="blue")
        link.pack(padx=10, pady=10)

        link.bind("<Button-1>", lambda e: self.open_url())
        cancel_button = tk.Button(self.popup, text="Przerwij trening", command=self.cancel_while_training)
        cancel_button.pack(padx=10, pady=10)

    def open_url(self):
        webbrowser.open_new("http://localhost:6006")

    def cancel_while_training(self):
        confirm = messagebox.askyesno("Przerwanie przygotowywania trenowania",
                                      "Czy na pewno chcesz przerwać proces trenowania?")
        if confirm:
            self.popup.destroy()
            self.switch_to_after_train()

    def switch_to_after_train(self):
        self.process.terminate()
        self.process2.terminate()
        for widget in self.root.winfo_children():
            widget.destroy()
        after_train_module.AfterTrainView(self.root, self.voice_model_service, self.voice_recordings_service,
                                          self.version_service, self.gender, self.language, self.dir_with_result,
                                          self.dataset, self.gpu)

    def start_train(self):
        language = 'pl' if self.language == 'polish' else 'en'
        if self.model_path:
            parts = self.model_path.split("/")
            relative_path_to_model = "/".join(parts[-2:]).lstrip("/")
            self.process = subprocess.Popen(
                ["python", "../train.py", '-m', relative_path_to_model, '-r', WORKING_DIR, '-n', self.run_name, '-l', language,
                 '-d', self.dataset, '-g', str(self.gpu)])
        else:
            self.process = subprocess.Popen(
                ["python", "../train.py", '-r', WORKING_DIR, '-n', self.run_name, '-l', language,
                 '-d', self.dataset, '-g', str(self.gpu)])  #uncomment after tests
