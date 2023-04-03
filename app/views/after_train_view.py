from lazy_import import lazy_module
import os
import shutil
from pathlib import Path
import playsound
import pygame
import threading
import tkinter as tk
from tkinter import messagebox
import queue

from app.entities.voice_model import VoiceModel
from app.entities.voice_recording import VoiceRecording
from app.settings import WORKING_DIR, MODEL_DIR_GENERATED, OUTPUT_DIR, GENERATED_DIR, GENERATED_TEMP_DIR
from app.speech_synthesizer import SpeechSynthesizer
from app.views.basic.basic_view import BasicView

train_module = lazy_module("app.views.train_view")


class AfterTrainView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, version_service, gender, language,
                 dir_with_result, dataset, gpu):
        super(AfterTrainView, self).__init__(root, voice_model_service, voice_recordings_service, version_service)
        self.X_MODELS = 3.33 * self.size_grid_x
        self.POPUP_WIDTH = 16.666 * self.size_grid_x
        self.POPUP_HEIGHT = 5 * self.size_grid_y
        self.gender = gender
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.gpu = gpu
        self.dataset = dataset
        self.dir_with_result = dir_with_result
        self.language = language
        self.choosen_model = tk.IntVar()
        self.choosen_model.set("0")  # default value
        self.event = threading.Event()
        self.speech_synthesizer = None
        self.stop = False
        self.paths_to_generated_voice_models = self.find_paths_to_generated_voice_models()
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()
        self.paths_to_basic_audio = []
        self.config_file_path = os.path.join(OUTPUT_DIR, "config.json")
        self.popup = None
        self.start_synthesize_basic_audio()
        self.input_field = tk.Entry(root, width=60, font=self.BUTTON_FONT)
        self.input_field.place(x=33.33 * self.size_grid_x, y=2 * self.PAD_Y)
        self.display_widgets()
        self.audio_text = ''
        self.audio_model = ''
        self.audio_path = ''
        self.entry2 = None

    def on_closing(self):
        if messagebox.askokcancel("Wyjście",
                                  "Czy na pewno chcesz zamknąc program? Wszystkie niezapisane zmiany zostaną usunięte."):
            self.root.destroy()
            self.event.set()
            self.thread.join()
            if self.speech_synthesizer:
                self.speech_synthesizer.stop_event.set()

    def start_synthesize_basic_audio(self):
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen which is app
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT)}+{int(x)}+{int(y)}")
        self.popup.title("Trwa generowanie audio")
        self.popup.grab_set()
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_process)
        label = tk.Label(self.popup, text="Trwa proces generowania audio dla wygenerowanych modeli.")
        label.pack(padx=10, pady=10)
        label = tk.Label(self.popup,
                         text="Jeżeli przerwiesz, rezultat uczenia zostanie utracony.")
        label.pack(padx=10, pady=10)
        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_process)
        cancel_button.pack(padx=10, pady=10)
        self.q.put(self.synthesize_basic_audio_for_models)
        pass

    def cancel_process(self):
        confirm = messagebox.askyesno("Przerwanie syntezowania audio",
                                      "Po skończeniu syntezowania cały proces uczenia zostanie utracony. Czy jesteś pewien?",
                                      parent=self.popup)
        if confirm:
            self.stop = True
            self.event.set()
            if self.speech_synthesizer:
                self.speech_synthesizer.stop_event.set()
            self.thread.join()
            self.switch_to_main_view()

    def cancel_synthesize(self):
        confirm = messagebox.askyesno("Przerwanie syntezowania audio",
                                      "Czy jesteś pewien, że chcesz przerwać syntezowanie audio?", parent=self.popup)
        if confirm:
            self.popup.destroy()
            self.stop = True
            self.speech_synthesizer.stop_event.set()

    def synthesize_basic_audio_for_models(self):
        '''Synthesize basic audio for each generated models and returns path to it'''
        text = "Hello. I am from Poland. Nice to meet you." if self.language == "english" else "Cześć. Jestem z Polskim. Miło Cię poznać."
        for voice_model_path in self.paths_to_generated_voice_models:
            if not self.stop:
                self.paths_to_basic_audio.append(self.generate_basic_audio(voice_model_path, text))
        if not self.stop:
            self.popup.destroy()
            self.root.after(0, self.display_models)

    def generate_basic_audio(self, voice_model_path, text):
        self.speech_synthesizer = SpeechSynthesizer(model_path=voice_model_path, config_path=self.config_file_path,
                                                    temp=True)
        output_name = self.speech_synthesizer.generate_sample_name()
        self.speech_synthesizer.generate_audio(output_name, text)
        return output_name

    def synthesize_audio(self):
        voice_model_path = self.paths_to_generated_voice_models[self.choosen_model.get()]
        text = self.input_field.get()
        if not text:
            messagebox.showerror(title="Błąd", message="Nie wprowadzono tekstu do syntezy")
            return
        if text == self.audio_text and self.choosen_model.get() == self.audio_model:
            self.play_audio(self.audio_path)
            return
        self.speech_synthesizer = SpeechSynthesizer(model_path=voice_model_path, config_path=self.config_file_path,
                                                    temp=True)
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen where the app is open
        output_name = self.speech_synthesizer.generate_sample_name()
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.grab_set()
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT)}+{int(self.x)}+{int(self.y)}")
        self.popup.title("Trwa generowanie audio")
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_synthesize)
        label = tk.Label(self.popup, text="Trwa proces generowania audio dla wybranego modelu.")
        label.pack(padx=10, pady=10)
        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel_synthesize)
        cancel_button.pack(padx=10, pady=10)
        self.q.put(lambda: self.speech_synthesizer.generate_audio(output_name, text, self.finish_synthesize), ())

    def finish_synthesize(self, audio_path):
        self.popup.destroy()
        if not self.stop:
            self.play_audio(audio_path)
            self.audio_path = audio_path
            self.audio_model = self.choosen_model.get()
            self.audio_text = self.input_field.get()
        self.stop = False

    def find_paths_to_generated_voice_models(self):
        paths = []
        for f in os.listdir(self.dir_with_result):
            if f.startswith('checkpoint'):
                paths.append(os.path.join(self.dir_with_result, f))
        return paths

    def display_widgets(self):
        label = tk.Label(self.root, font=self.MAX_FONT, text="Wytrenowane modele:", bg='green')
        label.place(x=self.X_MODELS, y=self.PAD_Y)
        frame = tk.Frame(self.root, width=self.size_grid_x * 15.5, height=16.5 * self.size_grid_y, bg='white')
        frame.place(x=self.X_MODELS - 10, y=self.PAD_Y + 2.3 * self.size_grid_y)  # place for files
        label = tk.Label(self.root, font=self.MAX_FONT, text="Wpisz tekst", bg='green')
        label.place(x=35 * self.size_grid_x, y=self.PAD_Y)
        # on the bottom is menu to save mdoel, go to main menu(with popup to be sure) and continue training
        play_button = tk.Button(self.root, text="Odsłuchaj", command=self.synthesize_audio,
                                width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2)
        play_button.place(x=43.3 * self.size_grid_x, y=3 * self.PAD_Y)
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=self.BUTTON_WIDTH_1, height=self.BUTTON_HEIGHT_1)
        save_button = tk.Button(self.root, text="Zapisz wybrany model", width=self.BUTTON_WIDTH_1,
                                height=self.BUTTON_HEIGHT_1,
                                command=self.display_window_to_enter_name_for_model)
        continue_training_button = tk.Button(self.root, text="Dotrenuj model", width=self.BUTTON_WIDTH_1,
                                             height=self.BUTTON_HEIGHT_1, command=self.continue_training)

        main_menu_button.place(x=6.6 * self.size_grid_x, y=23.3 * self.size_grid_y)
        save_button.place(x=26.6 * self.size_grid_x, y=23.3 * self.size_grid_y)
        continue_training_button.place(x=46.6 * self.size_grid_x, y=23.3 * self.size_grid_y)
        pass

    def display_window_to_enter_name_for_model(self):
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen which is app
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT)}+{int(x)}+{int(y)}")
        self.popup.title("Wpisz nazwę")
        self.popup.grab_set()
        label = tk.Label(self.popup, text="Wpisz nazwę dla modelu:")
        label.pack()

        self.entry2 = tk.Entry(self.popup, width=50)
        self.entry2.pack()

        cancel_button = tk.Button(self.popup, text="Anuluj", command=lambda: self.destroy_popup())
        cancel_button.pack(side=tk.LEFT, pady=self.PAD_Y / 2, padx=(160, 40))
        ok_button = tk.Button(self.popup, text="Zapisz", command=lambda: self.save_model(self.entry2.get()))
        ok_button.pack(side=tk.LEFT, pady=self.PAD_Y / 2)

    def save_model(self, name):
        if name == '':
            messagebox.showerror("Uzupełnij nazwę modelu!")
            return
        if self.model_name_exists(name):
            messagebox.showerror("Model z taką nazwą już istnieje!")
            return
        path_model, path_config = self.copy_model_to_saved_models(name)
        voice_model = VoiceModel(name, path_model, path_config, self.gender, self.language)
        model_id = self.voice_model_service.insert(voice_model)

        self.save_recording(model_id)
        self.popup.destroy()
        messagebox.showinfo(message="Model głosu został zapisany.")

    def save_recording(self, model_id):
        path_audio = self.paths_to_basic_audio[self.choosen_model.get()]
        new_path = shutil.copy(path_audio, GENERATED_DIR)
        name = 'basic'
        voice_recording = VoiceRecording(name, new_path, model_id)
        self.voice_recordings_service.insert(voice_recording)

    def model_name_exists(self, name):
        language = 'PL' if self.language == 'polish' else 'EN'
        gender = "MALE" if self.gender == 'man' else "FEMALE"
        directory = os.path.join(OUTPUT_DIR, f"{language}/{gender}")
        file_path = os.path.join(directory, name)
        path = Path(file_path)
        return path.is_file()

    def copy_model_to_saved_models(self, name):
        language = 'PL' if self.language == 'polish' else 'EN'
        gender = "MALE" if self.gender == 'man' else "FEMALE"
        path_model = self.paths_to_generated_voice_models[self.choosen_model.get()]
        path_config = self.config_file_path
        filename = os.path.basename(path_model)

        dest_dir = os.path.join(MODEL_DIR_GENERATED, f"{language}/{gender}/{name}")
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
        dest_path_model = os.path.join(dest_dir, filename)
        dest_path_config = os.path.join(dest_dir, "config.json")
        shutil.copy(path_model, dest_dir)
        shutil.copy(path_config, dest_dir)
        return dest_path_model, dest_path_config

    def switch_to_main_view(self):
        confirm = messagebox.askyesno("Powrót do menu głównego",
                                      "Po powrocie do menu głównego wszystkie niezapisane modele zostaną usuniete. Czy jesteś pewien?")

        if confirm:
            self.event.set()
            self.thread.join()
            self.destroy_all_files_in_dir(OUTPUT_DIR)
            super().switch_to_main_view()

    def destroy_all_files_in_dir(self, directory, model_path=None):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if not (model_path and (model_path == file_path or file_path == self.config_file_path)):
                        os.remove(file_path)
                except OSError as e:
                    print(str(e))
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except OSError as e:
                    print(str(e))

    def destroy_popup(self):
        self.popup.destroy()

    def continue_training(self):
        confirm = messagebox.askyesno("Kontunuowanie treningu",
                                      "Po wznowieniu trenowania wszystkie pozostałe niezapisane modele zostaną usunięte. Czy jesteś pewien?")

        if confirm:
            path_to_model = self.choosen_model.get()
            shutil.copy(path_to_model, OUTPUT_DIR)
            self.destroy_all_files_in_dir(MODEL_DIR_GENERATED, path_to_model)
            self.destroy_all_files_in_dir(OUTPUT_DIR, path_to_model)
            self.event.set()
            self.thread.join()
            self.train_model(path_to_model)

    def rm_all_files_from_output_dir_except_model(self, model_filename):
        for filename in os.listdir(OUTPUT_DIR):
            if filename in ["config.json", model_filename]:
                continue
            file_path = os.path.join(OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def train_model(self, model_path):
        model_filename = os.path.basename(model_path)
        dest_dir = os.path.join(OUTPUT_DIR, model_filename)
        shutil.move(model_path, dest_dir)
        for widget in self.root.winfo_children():
            widget.destroy()
        train_module.TrainView(self.root, self.voice_model_service, self.voice_recordings_service, self.version_service,
                               self.gender, self.language, self.option, self.gpu, self.dataset, model_path)

    def display_models(self):
        model_labels = []
        counter = 0
        for _ in self.paths_to_generated_voice_models:
            label = tk.Radiobutton(self.root, activebackground='white', highlightthickness=0, highlightcolor='white',
                                   text=f"model_{counter}", bg='white', font=self.BUTTON_FONT,
                                   variable=self.choosen_model,
                                   value=len(
                                       model_labels))  # value is index in self.paths_to_generated_voice_models list
            label.place(x=self.X_MODELS, y=self.Y_FIRST_MODEL + len(model_labels) * self.PAD_Y)
            model_labels.append(label)
            audio_path = self.paths_to_basic_audio[counter]
            button = tk.Button(self.root, text="Odsłuchaj", width=self.BUTTON_WIDTH_2, height=self.BUTTON_HEIGHT_2,
                               font=self.BUTTON_FONT, command=lambda: self.play_audio(audio_path))
            button.place(x=self.X_MODELS + 250, y=self.Y_FIRST_MODEL + (len(model_labels) - 1) * self.PAD_Y)
            counter += 1

    def play_audio(self, path_to_audio):
        if os.path.isfile(path_to_audio):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path_to_audio)
            pygame.mixer.music.play()

    def worker(self, q):
        while True:
            if self.event.is_set():
                return
            try:
                func = q.get(block=True, timeout=5)
                if func is not None:
                    func()
                    q.task_done()
            except Exception as e:
                print(str(e))
