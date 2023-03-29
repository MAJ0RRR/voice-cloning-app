import os
import shutil
import subprocess
import threading
from time import sleep
import tkinter as tk
from tkinter import messagebox

from app.settings import OUTPUT_DIR, WORKING_DIR
from app.views.basic.basic_view import BasicView, WIDTH, HEIGHT, POPUP_HEIGHT, POPUP_WIDTH


class TrainView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, gender, language, option, gpu, dataset,
                 model_id=None):
        super(TrainView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.dataset = dataset
        self.gpu = gpu
        self.run_name = self.generate_run_name()
        self.popup = None
        self.model_path, self.config_path = self.copy_model_to_output_dir()
        self.process = None
        self.start_train()
        self.thread = threading.Thread(target=self.wait_for_dir)
        self.thread.start()
        self.display_widgets()

    def copy_model_to_output_dir(self):
        voice_model = self.voice_model_service.select_by_id(self.model_id)
        path_model, path_config = voice_model['path_model'], voice_model['path_config']
        model_name = os.path.basename(path_model)
        config_name = os.path.basename(path_config)
        dst_model = os.path.join(OUTPUT_DIR, model_name)
        dst_config = os.path.join(OUTPUT_DIR, config_name)
        shutil.copy(path_model, dst_model)
        shutil.copy(path_config, dst_config)
        return dst_model, dst_config

    def generate_run_name(self):
        return f"{self.gender}_{self.language}_{self.model_id}"

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
        while():
            sleep(2*60) #creating this files lasts about 2 minutes
            dir_exists = False
            for dir in os.listdir(path):
                if dir.startswith(self.run_name):
                    dir_exists = True  #maybe later also check if in this dir is file that Pawel mentioned
                    break
            if dir_exists:
                self.run_tensorboard()
                self.create_new_popup()
                break
        self.root.after(0, self.terminate_thread)


    def terminate_thread(self):
        self.thread.join()

    def run_tensoboard(self):
        self.process2 = subprocess.Popen() #todo
        #kill process after finishing training

    def create_new_popup(self):
        for widget in self.popup.winfo_children():
            widget.destroy()
        self.popup.title('Trwa trenowanie głosu')
        self.link = tk.Hyperlink(
            self.popup,
            text="Sprawdź rezultat uczenia",
            url="localhost:6006",
        )
        self.link.pack(pady=10)
        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_before_train)
        cancel_button.pack(padx=10, pady=10)

    def start_train(self):
        language = 'pl' if self.language == 'polish' else 'en'
        self.process = subprocess.Popen([["python", "../train.py", '-m', self.model_path, '-r', WORKING_DIR, '-n', self.run_name, '-l', language, '-d', self.dataset, '-g', self.gpu]])




