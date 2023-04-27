from lazy_import import lazy_module
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
import queue

from app.samples_generator import SamplesGenerator
from app.views.basic.basic_view import BasicView
from app.settings import RAW_AUDIO_DIR, OUTPUT_DIR
from app.enums import Options

choose_voice_model_view = lazy_module("app.views.choose_voice_model_view")
train_module = lazy_module("app.views.train_view")


class ChooseAudioView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service, option, language, gender=None,
                 model_id=None):
        super(ChooseAudioView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
            self.choosen_gpu = tk.IntVar()
            self.choosen_gpu.set(self.gpu_ids[0])
        except IndexError:
            self.no_gpu_available()
            return
        self.display_widgets()
        self.samples_generator = SamplesGenerator(self.language, self.version_service)
        self.q = queue.Queue()
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.worker, args=(self.q,))
        self.thread.start()
        self.stop = None
        self.files = []

    def no_gpu_available(self):
        messagebox.showerror("Brak karty Nvidii",
                             "Nie wykryto karty graficznej Nvidii. Zostaniesz przekierowany do menu głównego.")
        super().switch_to_main_view()

    def display_widgets_choose_gpu(self):
        counter = 0
        label = tk.Label(self.root, activebackground=self.BACKGROUND_COLOR,
                         text="Wybierz kartę graficzną", bg=self.BACKGROUND_COLOR, font=self.MAX_FONT)
        label.place(x=48.333 * self.size_grid_x, y=self.Y_MENU - 10 * self.size_grid_y)
        for gpu_id in self.gpu_ids:
            label = tk.Radiobutton(self.root, activebackground=self.BACKGROUND_COLOR, highlightthickness=0,
                                   highlightcolor=self.BACKGROUND_COLOR,
                                   text=str(gpu_id), bg=self.BACKGROUND_COLOR, font=self.MAX_FONT,
                                   variable=self.choosen_gpu,
                                   value=gpu_id)
            label.place(x=48.333 * self.size_grid_x, y=self.Y_MENU + self.PAD_Y * (counter + 1) - 10 * self.size_grid_y)
            counter += 1

    def display_VRAM_widgets(self, x):
        label = tk.Label(self.root, activebackground=self.BACKGROUND_COLOR,
                         text="VRAM", bg=self.BACKGROUND_COLOR, font=self.MAX_FONT)
        label.place(x=x, y=self.Y_MENU - 10 * self.size_grid_y)
        label = tk.Radiobutton(self.root, activebackground=self.BACKGROUND_COLOR, highlightthickness=0,
                               highlightcolor=self.BACKGROUND_COLOR,
                               text="Poniżej 2  GB", bg=self.BACKGROUND_COLOR, font=self.MAX_FONT, variable=self.VRAM,
                               value=1)
        label.place(x=x, y=self.Y_MENU + self.PAD_Y * 1 - 10 * self.size_grid_y)
        label = tk.Radiobutton(self.root, activebackground=self.BACKGROUND_COLOR, highlightthickness=0,
                               highlightcolor=self.BACKGROUND_COLOR,
                               text="<2;5) GB", bg=self.BACKGROUND_COLOR, font=self.MAX_FONT, variable=self.VRAM,
                               value=3)
        label.place(x=x, y=self.Y_MENU + self.PAD_Y * 2 - 10 * self.size_grid_y)
        label = tk.Radiobutton(self.root, activebackground=self.BACKGROUND_COLOR, highlightthickness=0,
                               highlightcolor=self.BACKGROUND_COLOR,
                               text="Powyżej 5 GB", bg=self.BACKGROUND_COLOR, font=self.MAX_FONT, variable=self.VRAM,
                               value=8)
        label.place(x=x, y=self.Y_MENU + self.PAD_Y * 3 - 10 * self.size_grid_y)

    def display_widgets(self):
        label = tk.Label(self.root, font=self.MAX_FONT, text='Wybierz audio do uczenia modelu',
                         bg=self.BACKGROUND_COLOR)
        label.pack(pady=self.PAD_Y / 2)
        frame = tk.Frame(self.root, width=14.333 * self.size_grid_x, height=18.333 * self.size_grid_y, bg='white')
        frame.place(x=3.5 * self.size_grid_x, y=6 * self.size_grid_y)  # place for files
        frame = tk.Frame(self.root, width=14.333 * self.size_grid_x, height=10 * self.size_grid_y, bg='white')
        frame.place(x=30.5 * self.size_grid_x, y=6 * self.size_grid_y)  # place for dirs
        if len(self.gpu_ids):
            self.display_widgets_choose_gpu()
            self.display_VRAM_widgets(33.33 * self.size_grid_x)
        else:
            self.display_VRAM_widgets(45 * self.size_grid_x)
        continue_button = tk.Button(self.root, text="Rozpocznij proces", command=self.start_generate_samples,
                                    font=self.BUTTON_FONT)
        continue_button.place(x=51.667 * self.size_grid_x, y=31.34 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                              height=self.BUTTON_HEIGHT_1)
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     font=self.BUTTON_FONT)
        if self.option == Options.train_new:
            back_button = tk.Button(self.root, text="Wybierz ponownie model głosu",
                                    command=self.switch_to_choose_model, font=self.BUTTON_FONT)
        else:
            back_button = tk.Button(self.root, text="Wybierz ponownie język",
                                    command=self.switch_to_choose_gender_language, font=self.BUTTON_FONT)
        back_button.place(x=18.333 * self.size_grid_x, y=self.Y_MENU, width=self.BUTTON_WIDTH_1,
                          height=self.BUTTON_HEIGHT_1)
        main_menu_button.place(x=5 * self.size_grid_x, y=self.Y_MENU, width=self.BUTTON_WIDTH_1,
                               height=self.BUTTON_HEIGHT_1)
        directory_button = tk.Button(self.root, text="Select directory", command=self.open_directory,
                                     font=self.BUTTON_FONT)
        file_button = tk.Button(self.root, text="Select file", command=self.open_file, font=self.BUTTON_FONT)
        directory_button.place(x=31.667 * self.size_grid_x, y=3.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                               height=self.BUTTON_HEIGHT_1)
        file_button.place(x=5 * self.size_grid_x, y=3.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                          height=self.BUTTON_HEIGHT_1)
        delete_dir_button = tk.Button(self.root, text="Delete last directory", command=self.delete_dir,
                                      font=self.BUTTON_FONT)
        delete_file_button = tk.Button(self.root, text="Delete last file", command=self.delete_file,
                                       font=self.BUTTON_FONT)
        delete_dir_button.place(x=45 * self.size_grid_x, y=3.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                                height=self.BUTTON_HEIGHT_1)
        delete_file_button.place(x=18.333 * self.size_grid_x, y=3.333 * self.size_grid_y, width=self.BUTTON_WIDTH_1,
                                 height=self.BUTTON_HEIGHT_1)

    def switch_to_choose_model(self):
        self.event.set()
        self.thread.join()
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_view.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                     self.voice_recordings_service, self.version_service, self.option)

    def get_gpu_ids(self):
        try:
            output = subprocess.check_output(['nvidia-smi', '--query-gpu=index', '--format=csv,noheader'])
            return [int(x) for x in output.decode().strip().split('\n')]
        except subprocess.CalledProcessError:
            return []
        except FileNotFoundError:
            return []
        # return [0]  # for test without nvidia

    def switch_to_main_view(self):
        self.event.set()
        self.thread.join()
        super().switch_to_main_view()

    def switch_to_choose_language(self):
        self.event.set()
        self.thread.join()
        super().switch_to_choose_language()

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć program?"):
            self.root.destroy()

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
        self.q.put(lambda: self.samples_generator.generate_samples(version, self.choosen_gpu.get(), self.VRAM.get(),
                                                                   self.finish_generating), ())
        x = (self.WIDTH - self.POPUP_WIDTH) // 2 + screen_pos
        y = (self.HEIGHT - self.POPUP_HEIGHT) // 2
        self.popup = tk.Toplevel(self.root)
        self.popup.geometry(f"{int(self.POPUP_WIDTH)}x{int(self.POPUP_HEIGHT + self.size_grid_y)}+{int(x)}+{int(y)}")
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
            return
        self.delete_all_file_and_dir_labels()
        self.inform_about_generated_samples(path)

    def switch_to_train(self):
        self.event.set()
        self.thread.join()
        gpu = self.choosen_gpu.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        dataset = f"dataset_{self.version_service.get_version() - 1}"
        model_path, config_path = self.copy_model_to_output_dir()
        train_module.TrainView(self.root, self.voice_model_service, self.voice_recordings_service, self.version_service,
                               self.gender, self.language, self.option, gpu, dataset, model_path, self.model_id)

    def copy_model_to_output_dir(self):
        if not self.model_id:
            return None, None
        voice_model = self.voice_model_service.select_by_id(self.model_id)
        path_model, path_config = voice_model['path_model'], voice_model['path_config']
        if not os.path.exists(os.path.join(OUTPUT_DIR, voice_model['name'])):
            os.mkdir(os.path.join(OUTPUT_DIR, voice_model['name']))
        model_name = os.path.basename(path_model)
        config_name = os.path.basename(path_config)
        dst_model = os.path.join(OUTPUT_DIR, voice_model['name'], model_name)
        dst_config = os.path.join(OUTPUT_DIR, voice_model['name'], config_name)
        shutil.copy(path_model, dst_model)
        shutil.copy(path_config, dst_config)
        return f'{voice_model["name"]}/{model_name}', f'{voice_model["name"]}/{config_name}'

    def finish_generating(self, version, path):
        self.root.after(0, lambda: self.after_generating(version, path))

    def inform_about_generated_samples(self, path):
        messagebox.showinfo("Zakończono generowanie próbek",
                            f"Próbki zostały wygenerowane i znajdują się w folderze: {path}")

    def open_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            label_dir = tk.Label(self.root, text=directory_path, font=self.SMALL_FONT)
            self.dir_labels.append(label_dir)
            label_dir.place(x=30.55 * self.size_grid_x, y=5.667 * self.size_grid_y + len(self.dir_labels) + 15)

    def open_file(self):
        allowed_extensions = self.allowed_extensions()
        file_path = filedialog.askopenfilename(filetypes=(("Audio files", allowed_extensions),))
        if file_path:
            filename = file_path.split('/')[-1]
            label_file = tk.Label(self.root, text=filename, font=self.SMALL_FONT)
            self.file_labels.append(label_file)
            self.files.append(file_path)
            label_file.place(x=3.55 * self.size_grid_x, y=5.667 * self.size_grid_y + len(self.file_labels) * 15)

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
        for file in self.files:
            self.copy_file_to_dir(file)
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
            if extension in self.ALLOWED_EXTENSIONS:
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
        for extension in self.ALLOWED_EXTENSIONS:
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
