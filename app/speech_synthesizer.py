import subprocess
from datetime import datetime
import os
import threading

from app.settings import GENERATED_DIR, GENERATED_TEMP_DIR


class SpeechSynthesizer:

    def __init__(self, model=None, model_path=None, config_path=None, temp=False):
        self.model = model
        self.model_path = model_path
        self.config_path = config_path
        self.stop_event = threading.Event()
        self.temp = temp

    def generate_audio(self, output_name, text, callback=None):
        if self.model:
            model_path = self.model['path_model']
            config_path = self.model['path_config']
        else:
            model_path = self.model_path
            config_path = self.config_path
        changed_text = f'\"{text}\"'
        self.synthesize_audio(changed_text, model_path, config_path, output_name, callback)

    def synthesize_audio(self, text, model_path, config_path, output_file, callback):
        process = subprocess.Popen(['tts', '--text', text, '--model_path', model_path, '--config_path', config_path,  '--out_path', output_file])
        while process.poll() is None:
            if self.stop_event.is_set():
                print('terminacja')
                process.terminate()
                self.stop_event = threading.Event()
        if callback:
            callback(output_file)

    def generate_sample_name(self):
        dt = datetime.now()
        if not self.temp:
            if not os.path.exists(GENERATED_DIR):
                os.makedirs(GENERATED_DIR)
            return os.path.join(GENERATED_DIR, f"{dt.strftime('%Y-%m-%d_%H:%M:%S')}.wav")
        if not os.path.exists(GENERATED_TEMP_DIR):
            os.makedirs(GENERATED_TEMP_DIR)
        return os.path.join(GENERATED_TEMP_DIR, f"{dt.strftime('%Y-%m-%d_%H:%M:%S')}.wav")
