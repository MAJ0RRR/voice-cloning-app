import os
from pathlib import Path

WORKING_DIR = Path(os.getcwd()).parent

# dir for voice models
MODEL_DIR = os.path.join(WORKING_DIR, 'voice_models')

# dir for synthesized audio
GENERATED_DIR = os.path.join(WORKING_DIR, 'audiofiles/generated')

# dir to put raw audio to generate samples
RAW_AUDIO_DIR = os.path.join(WORKING_DIR, 'audiofiles/raw')

# path to db_file
db_file = os.path.join(WORKING_DIR, 'app/db_file.db')

#path to output dir
OUTPUT_DIR = os.path.join(WORKING_DIR, "output")
