from lazy_import import lazy_module
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import subprocess
import queue

from app.enums import Options
from app.samples_generator import SamplesGenerator
from app.views.basic.basic_view import BUTTON_WIDTH_1, BUTTON_HEIGHT_1, BUTTON_FONT, Y_MENU, ALLOWED_EXTENSIONS, WIDTH, \
    POPUP_WIDTH, HEIGHT, POPUP_HEIGHT, BasicView, PAD_Y
from app.views.train_view import TrainView
from app.settings import RAW_AUDIO_DIR
from app.enums import Options

choose_voice_model_view = lazy_module("app.views.choose_voice_model_view")


class ChooseAudioView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service, option, language, gender=None,
                 model_id=None):
        super(ChooseAudioView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.option = option
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.file_labels = []
        self.dir_labels = []
        self.gpu_ids = self.get_gpu_ids()
        self.choosen_gpu = tk.IntVar()
        self.VRAM = tk.IntVar()
        self.VRAM.set('1')
        try:
            self.choosen_model = tk.IntVar()
            self.choosen_model.set(self.gpu_ids[0])
        except ValueError:
            self.no_gpu_available()
        self.display_widgets()
        self.samples_generator = SamplesGenerator(self.language, self.version_service)
        self.q = queue.Queue()
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()
        self.stop = None

    def no_gpu_available(self):
        messagebox.showerror("Brak karty Nvidii", "Nie wykryto karty graficznej Nvidii. Zostaniesz przekierowany do menu głównego.")
        super().switch_to_main_view()

    def display_widgets_choose_gpu(self):
        counter = 0
        label = tk.Label(self.root, activebackground='green',
                                   text="Wybierz kartę graficzną", bg='green', font=BUTTON_FONT)
        label.place(x=1350, y=Y_MENU)
        for gpu_id in self.gpu_ids:
            label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                                   text=str(gpu_id), bg='green', font=BUTTON_FONT, variable=self.choosen_gpu,
                                   value=gpu_id)
            label.place(x=1350, y=Y_MENU + PAD_Y/2 * (counter+1))
            counter += 1

    def display_VRAM_widgets(self, x):
        label = tk.Label(self.root, activebackground='green',
                         text="VRAM", bg='green', font=BUTTON_FONT)
        label.place(x=x, y=Y_MENU)
        label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                               text="Poniżej 2  GB", bg='green', font=BUTTON_FONT, variable=self.VRAM,
                               value=1)
        label.place(x=x, y=Y_MENU + PAD_Y / 2 * 1)
        label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                               text="<2;5) GB", bg='green', font=BUTTON_FONT, variable=self.choosen_gpu,
                               value=3)
        label.place(x=x, y=Y_MENU + PAD_Y / 2 * 2)
        label = tk.Radiobutton(self.root, activebackground='green', highlightthickness=0, highlightcolor='green',
                               text="Powyżej 5 GB", bg='green', font=BUTTON_FONT, variable=self.choosen_gpu,
                               value=8)
        label.place(x=x, y=Y_MENU + PAD_Y / 2 * 3)

    def display_widgets(self):
        if len(self.gpu_ids):
            self.display_widgets_choose_gpu()
            self.display_VRAM_widgets(1150)
        else:
            self.display_VRAM_widgets(1350)
        continue_button = tk.Button(self.root, text="Rozpocznij proces", command=self.start_generate_samples,
                                    width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        continue_button.place(x=1550, y=943)
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        if self.option == Options.train_new:
            back_button = tk.Button(self.root, text="Wybierz ponownie model głosu", width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_choose_model, font=BUTTON_FONT)
        else:
            back_button = tk.Button(self.root, text="Wybierz ponownie język", width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1,
                                    command=self.switch_to_choose_gender_language, font=BUTTON_FONT)
        back_button.place(x=750, y=Y_MENU)
        main_menu_button.place(x=250, y=Y_MENU)
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
        self.event.set()
        self.thread.join()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_view.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                     self.voice_recordings_service, self.version_service, self.option)

    def get_gpu_ids(self):
        #output = subprocess.check_output(['nvidia-smi', '--query-gpu=index', '--format=csv,noheader'])
        #return [int(x) for x in output.decode().strip().split('\n') #uncomment after tests
        return [0,1]

    def switch_to_main_view(self):
        self.event.set()
        self.thread.join()
        super().switch_to_main_view()

    def switch_to_choose_language(self):
        self.event.set()
        self.thread.join()
        super().switch_to_choose_language()

    def warning_no_files(self):
        messagebox.showerror('Brak plików', 'Nie wybrano żadnych plików!')

    def start_generate_samples(self):
        n_files = self.copy_all_files_to_dir()
        if n_files == 0:
            self.warning_no_files()
            return
        version = self.version_service.get_version()
        self.samples_generator.stop_event = threading.Event()
        screen_pos = self.root.winfo_x()  # we need this to popup on the same screen which is app
        self.q.put(lambda: self.samples_generator.generate_samples(version, self.choosen_gpu.get(), self.VRAM.get(), self.finish_generating), ())
        x = (WIDTH - POPUP_WIDTH) // 2 + screen_pos
        y = (HEIGHT - POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        self.popup.title("Próbki są generowane")

        label = tk.Label(self.popup, text="Aby przerwać generowanie")
        label.pack(padx=10, pady=10)
        label = tk.Label(self.popup, text="próbek kliknij anuluj.")
        label.pack()

        cancel_button = tk.Button(self.popup, text="Anuluj", command=self.cancel)
        cancel_button.pack(padx=10, pady=10)

    def after_generating(self, version, path):
        self.popup.destroy()
        if self.stop:
            return
        self.version_service.update_version(version, version + 1)
        if self.option in [Options.train_old, Options.train_new]:
            self.switch_to_train()
        self.delete_all_file_and_dir_labels()
        self.inform_about_generated_samples(path)

    def switch_to_train(self):
        self.event.set()
        self.thread.join()
        gpu = self.choosen_gpu.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        dataset = f"dataset_{self.version_service.get_version()}"
        TrainView(self.root, self.voice_model_service, self.voice_recordings_service, self.version_service, self.gender, self.language, self.option, gpu, dataset, self.model_id)

    def finish_generating(self, version, path):
        self.root.after(0, lambda: self.after_generating(version, path))

    def inform_about_generated_samples(self, path):
        messagebox.showinfo("Zakończono generowanie próbek",
                            f"Próbki zostały wygenerowane i znajdują się w folderze: {path}")

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
        counter = 0
        for file in self.file_labels:
            source_path = file.cget("text")
            self.copy_file_to_dir(source_path)
            counter += 1
        for dir_label in self.dir_labels:
            dir = dir_label.cget("text")
            files = self.allowed_files_from_dir(dir)
            for file in files:
                self.copy_file_to_dir(file)
                counter += 1
        return counter

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
            if self.event.is_set():
                return
            try:
                func = q.get(block=False, timeout=5)
                if func is not None:
                    func()
                    q.task_done()
            except:
                pass
