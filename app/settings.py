import os
from pathlib import Path

WORKING_DIR = os.getcwd()

MODEL_DIR = os.path.join(WORKING_DIR, 'voice_models')
VOICE_DIR = os.path.join(WORKING_DIR, 'audio/voice_recordings')
MEDIA_DIR = os.path.join(WORKING_DIR, 'audio/media')

RAW_AUDIO_DIR = os.path.join(Path(WORKING_DIR).parent, 'audiofiles/raw')
db_file = os.path.join(WORKING_DIR, 'db_file.db')
