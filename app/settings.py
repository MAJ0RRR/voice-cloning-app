import os
from pathlib import Path

WORKING_DIR = Path(os.getcwd()).parent

MODEL_DIR = os.path.join(WORKING_DIR, 'voice_models')
GENERATED_DIR = os.path.join(WORKING_DIR, 'audiofiles/generated')

RAW_AUDIO_DIR = os.path.join(WORKING_DIR, 'audiofiles/raw')
db_file = os.path.join(WORKING_DIR, 'app/db_file.db')
