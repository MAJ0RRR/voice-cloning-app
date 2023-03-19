import os
import subprocess

from app.settings import WORKING_DIR, RAW_AUDIO_DIR
from whispertrans import create_transcription


class SamplesGenerator:

    def __init__(self, language):
        self.files = None
        self.stop_event = None
        self.language = language

    def generate_samples(self, callback):
        process = subprocess.Popen(["python", "../splits_equal.py"])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.terminate()
                self.finish_generating(callback)
        version = self.version_service.get_version()
        process = subprocess.Popen(["python", "../noise.py", "--destination", f"dataset{version}"])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.terminate()
                self.finish_generating(callback)
        create_transcription(WORKING_DIR, f"dataset{version}", self.language, 10)
        self.version_service.update_version(version, version + 1)
        # discard tranription
        path = f'audiofiles/datasets/dataset{version}'
        self.finish_generating(callback, path)

    def finish_generating(self, callback, path):
        self.delete_files_from_raw_dir()
        callback(path)

    def delete_files_from_raw_dir(self):
        for file_name in os.listdir(RAW_AUDIO_DIR):
            file_path = os.path.join(RAW_AUDIO_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
