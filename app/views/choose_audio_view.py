from lazy_import import lazy_module
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import queue

from app.enums import Options
from app.samples_generator import SamplesGenerator
from app.views.basic.basic_view import BUTTON_WIDTH_1, BUTTON_HEIGHT_1, BUTTON_FONT, Y_MENU, ALLOWED_EXTENSIONS, WIDTH, \
    POPUP_WIDTH, HEIGHT, POPUP_HEIGHT, BasicView
from app.views.train_view import TrainView
from app.settings import RAW_AUDIO_DIR
from app.enums import Options

choose_voice_model_view = lazy_module("app.views.choose_voice_model_view")


class ChooseAudioView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service, option, language, gender=None,
                 model_id=None):
        super(ChooseAudioView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.option = option
        self.display_widgets()
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.file_labels = []
        self.dir_labels = []
        self.samples_generator = SamplesGenerator(self.language, self.version_service)
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()
        self.stop = None

    def display_widgets(self):
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        if self.option == Options.train:
            back_button = tk.Button(self.root, text="Wybierz ponownie model głosu", width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_choose_gender_language_train, font=BUTTON_FONT)
        else:
            back_button = tk.Button(self.root, text="Wybierz ponownie język", width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_choose_language, font=BUTTON_FONT)
        back_button.place(x=750, y=Y_MENU)
        continue_button = tk.Button(self.root, text="Rozpocznij proces", command=self.start_generate_samples,
                                    width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        main_menu_button.place(x=250, y=Y_MENU)
        continue_button.place(x=1250, y=Y_MENU)
        directory_button = tk.Button(self.root, text="Select directory", command=self.open_directory,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        file_button = tk.Button(self.root, text="Select file", command=self.open_file, width=BUTTON_WIDTH_1,
                                height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        directory_button.place(x=950, y=100)
        file_button.place(x=150, y=100)
        delete_dir_button = tk.Button(self.root, text="Delete last directory", command=self.delete_dir,
                                      width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        delete_file_button = tk.Button(self.root, text="Delete last file", command=self.delete_file,
                                       width=BUTTON_WIDTH_1,
                                       height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        delete_dir_button.place(x=1350, y=100)
        delete_file_button.place(x=550, y=100)

    def switch_to_choose_model(self):
        self.thread.join()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_view.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                     self.voice_recordings_service, self.version_service, self.option)

    def switch_to_choose_language(self):
        self.thread.join()
        super().switch_to_choose_language()

    def start_generate_samples(self):
        version = self.version_service.get_version()
        self.copy_all_files_to_dir()
        self.samples_generator.stop_event = threading.Event()
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen which is app
        self.q.put(lambda: self.samples_generator.generate_samples(version, self.after_generating), ())
        x = (WIDTH - POPUP_WIDTH) // 2 + screen_pos
        y = (HEIGHT - POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        self.popup.title("Trwa proces")

        label = tk.Label(self.popup, text="Aby przerwać generowanie próbek kliknij anuluj.")
        label.pack(padx=10, pady=10)

        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel)
        cancel_button.pack(padx=10, pady=10)

    def after_generating(self, version, path):
        self.popup.destroy()
        if self.stop:
            return
        self.version_service(version, version+1)
        if self.option == Options.train:
            self.switch_to_train()
        self.delete_all_file_and_dir_labels()
        self.inform_about_generated_samples(path)

    def inform_about_generated_samples(self, path):
        messagebox.showinfo("Zakończono generowanie próbek",
                            f"Próbki zostały wygenerowane i znajdują się w folderze: {path}")

    def switch_to_train(self):
        pass

    def open_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            label_dir = tk.Label(self.root, text=directory_path, bg='green', font=BUTTON_FONT)
            self.dir_labels.append(label_dir)
            label_dir.place(x=950, y=160 + len(self.dir_labels) + 20)

    def open_file(self):
        allowed_extensions = self.allowed_extensions()
        file_path = filedialog.askopenfilename(filetypes=(("Audio files", allowed_extensions),))
        if file_path:
            label_file = tk.Label(self.root, text=file_path, bg='green', font=BUTTON_FONT)
            self.file_labels.append(label_file)
            label_file.place(x=150, y=160 + len(self.file_labels) * 20)

    def delete_all_file_and_dir_labels(self):
        for _ in self.file_labels:
            self.delete_file()
        for _ in self.dir_labels:
            self.delete_dir()

    def delete_file(self):
        if self.file_labels:
            self.file_labels[-1].destroy()
            self.file_labels = self.file_labels[:-1]

    def delete_dir(self):
        if self.dir_labels:
            self.dir_labels[-1].destroy()
            self.dir_labels = self.dir_labels[:-1]

    def copy_all_files_to_dir(self):
        for file in self.file_labels:
            source_path = file.cget("text")
            self.copy_file_to_dir(source_path)
        for dir_label in self.dir_labels:
            dir = dir_label.cget("text")
            files = self.allowed_files_from_dir(dir)
            for file in files:
                self.copy_file_to_dir(file)

    def allowed_files_from_dir(self, dir):
        ret = []
        for file in os.listdir(dir):
            filename, extension = os.path.splitext(file)
            if extension in ALLOWED_EXTENSIONS:
                ret.append(os.path.join(dir, file))
        return ret

    def cancel(self):
        res = messagebox.askquestion('Przerwanie generowania próbek',
                                     'Czy na pewno chcesz zakończyć generowanie próbek')
        if res == 'yes':
            self.stop = True
            self.samples_generator.stop_event.set()

    def allowed_extensions(self):
        ret = ""
        for extension in ALLOWED_EXTENSIONS:
            ret += f"{extension} "
        return ret[:-1]

    def copy_file_to_dir(self, source_path):
        filename = os.path.basename(source_path)
        dest_path = os.path.join(RAW_AUDIO_DIR, filename)
        shutil.copy(source_path, dest_path)

    def worker(self, q):
        while True:
            print('work work')
            func = q.get()
            if func is not None:
                func()
                q.task_done()
