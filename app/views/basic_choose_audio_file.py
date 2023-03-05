import os
import shutil
import tkinter as tk
from tkinter import filedialog

from app.views.basic_view import BasicView, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, ALLOWED_EXTENSIONS, BUTTON_FONT
from app.settings import RAW_AUDIO_DIR


class BasicChooseAudioFile(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service):
        super(BasicChooseAudioFile, self).__init__(root, voice_model_service, voice_records_service)
        self.file_labels = []
        self.dir_labels = []
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

    def open_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            label_dir = tk.Label(self.root, text=directory_path, bg='green', font=BUTTON_FONT)
            self.dir_labels.append(label_dir)
            label_dir.place(x=950, y=160 + len(self.dir_labels) + 20)

    def open_file(self):
        allowed_extensions = BasicChooseAudioFile.allowed_extensions()
        file_path = filedialog.askopenfilename(filetypes=(("Audio files", allowed_extensions),))
        if file_path:
            label_file = tk.Label(self.root, text=file_path, bg='green', font=BUTTON_FONT)
            self.file_labels.append(label_file)
            label_file.place(x=150, y=160 + len(self.file_labels) * 20)

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
            files = BasicChooseAudioFile.allowed_files_from_dir(dir)
            for file in files:
                self.copy_file_to_dir(file)

    @staticmethod
    def allowed_files_from_dir(dir):
        ret = []
        for file in os.listdir(dir):
            filename, extension = os.path.splitext(file)
            if extension in ALLOWED_EXTENSIONS:
                ret.append(os.path.join(dir,file))
        return ret
            

    @staticmethod
    def allowed_extensions():
        ret = ""
        for extension in ALLOWED_EXTENSIONS:
            ret += f"{extension} "
        return ret[:-1]

    def copy_file_to_dir(self, source_path):
        filename = os.path.basename(source_path)
        dest_path = os.path.join(RAW_AUDIO_DIR, filename)
        shutil.copy(source_path, dest_path)
