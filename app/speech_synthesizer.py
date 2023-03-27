import subprocess
from datetime import datetime
import os
import threading

from app.settings import GENERATED_DIR


class SpeachSynthesizer:

    def __init__(self, model=None, model_path=None, config_path=None):
        self.model = model
        self.model_path = model_path
        self.config_path = config_path
        self.stop_event = threading.Event()

    def generate_audio(self, output_name, text, callback=None):
        if self.model:
            print('checkpoint1')
            model_path = self.model['path_model']
            config_path = self.model['path_config']
        else:
            print('checkpoint2')
            model_path = self.model_path
            config_path = self.config_path
        print('checkpoint3')
        changed_text = f'\"{text}\"'
        self.synthesize_audio(changed_text, model_path, config_path, output_name, callback)

    def synthesize_audio(self, text, model_path, config_path, output_file, callback):
        process = subprocess.Popen(["sh", "../synthesize.sh", text, model_path, config_path, output_file])
        while process.poll() is None:
            if self.stop_event.is_set():
                process.kill()
                self.stop_event = threading.Event()
        if callback:
            callback(output_file)

    def generate_sample_name(self):
        dt = datetime.now()
        output_path = os.path.join(GENERATED_DIR, f"{dt.strftime('%Y-%m-%d_%H:%M:%S')}.wav")
        return output_path
