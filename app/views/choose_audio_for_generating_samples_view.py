import tkinter as tk
from tkinter import filedialog
from lazy_import import lazy_module
from app.components.listbox_with_button import ListBoxWithButton


choose_gender_language_module = lazy_module("app.views.choose_gender_language_view")
main_menu_module = lazy_module("app.views.main_view")
WIDTH = 1920
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PAD_Y = 80
ENABLED_EXTENSIONS = ('.mp3', '.mp4', '.wav')


class ChooseAudioForGeneratingSamples:

    def __init__(self, root, voice_model_service, voice_records_service):
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_records_service = voice_records_service
        self.file_labels = []
        self.dir_labels = []
        directory_button = tk.Button(self.root, text="Select directory", command=self.open_directory, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=("Helvetica", 14))
        file_button = tk.Button(self.root, text="Select file", command=self.open_file,  width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=("Helvetica", 14))
        directory_button.place(x=WIDTH / 2 - 520 , y=100)
        file_button.place(x=WIDTH / 2 + 120, y=100)
        delete_dir_button = tk.Button(self.root, text="Delete last directory", command=self.delete_dir,
                                     width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=("Helvetica", 14))
        delete_file_button = tk.Button(self.root, text="Delete last file", command=self.delete_file, width=BUTTON_WIDTH,
                                height=BUTTON_HEIGHT, font=("Helvetica", 14))
        delete_dir_button.place(x=550, y=700)
        delete_file_button.place(x=950, y=700)
        main_menu_button = tk.Button(self.root, text="Main menu", command=self.switch_to_main_menu,
                                     width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=("Helvetica", 14))
        continue_button = tk.Button(self.root, text="Generate samples", command=self.open_file, width=BUTTON_WIDTH,
                                height=BUTTON_HEIGHT, font=("Helvetica", 14))
        main_menu_button.place(x=150, y=700)
        continue_button.place(x=1350, y=700)



    def open_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            label_dir = tk.Label(self.root, text=directory_path, bg='green', font=("Helvetica", 14))
            self.dir_labels.append(label_dir)
            label_dir.place(x=WIDTH / 2 - 520, y=160+len(self.dir_labels)+20)

    def open_file(self):
        enabled_extensions = ChooseAudioForGeneratingSamples.enabled_extensions()
        file_path = filedialog.askopenfilename(filetypes = (("Audio files", enabled_extensions), ))
        self.n_files += 1
        if file_path:
            label_file = tk.Label(self.root, text=file_path, bg='green', font=("Helvetica", 14))
            self.file_labels.append(label_file)
            label_file.place(x=WIDTH / 2 + 120, y=160 + len(self.file_labels) * 20)

    def delete_file(self):
        if self.file_labels:
            self.file_labels[-1].destroy()
            self.file_labels = self.file_labels[:-1]

    def delete_dir(self):
        if self.dir_labels:
            self.dir_labels[-1].destroy()
            self.dir_labels = self.dir_labels[:-1]

    def switch_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_records_service)


    @staticmethod
    def enabled_extensions():
        ret = ""
        for extension in ENABLED_EXTENSIONS:
            ret += f"{extension} "
        return ret[:-1]

