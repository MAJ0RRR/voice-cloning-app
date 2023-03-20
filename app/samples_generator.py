import os
import subprocess

from app.settings import WORKING_DIR, RAW_AUDIO_DIR
from whispertrans import create_transcription


class SamplesGenerator:

    def __init__(self, language, version_service):
        self.files = None
        self.stop_event = None
        self.language = 'en' if language == 'english' else 'pl'
        self.version_service = version_service

    def generate_samples(self, version, callback):
        source_1 = os.path.join(WORKING_DIR, "audiofiles/raw")
        dest_1 = os.path.join(WORKING_DIR, "audiofiles/splits")
        process = subprocess.Popen(["python", "../splits_equal.py", "-s", source_1, "-d", dest_1])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.terminate()
                self.finish_generating(callback)
        print("after 1 ")
        process = subprocess.Popen(["python", "../noise.py", "--destination", f"dataset{version}"])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.terminate()
                self.finish_generating(callback)
        print("after 2")
        create_transcription(WORKING_DIR, f"dataset{version}", self.language, 1)
        print("after 3")
        root = os.path.join(WORKING_DIR, f'audiofiles/datasets/dataset{version}')
        process = subprocess.Popen(["python", "../discard_transcriptions.py", self.language, root])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.terminate()
                self.finish_generating(callback)
        path = f'audiofiles/datasets/dataset{version}'
        self.finish_generating(version, callback, path)

    def finish_generating(self, version, callback, path):
        self.delete_files_from_raw_dir()
        callback(version, path)

    def delete_files_from_raw_dir(self):
        for file_name in os.listdir(RAW_AUDIO_DIR):
            file_path = os.path.join(RAW_AUDIO_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
