import whisper
import os, os.path
import glob
import pandas as pd
 
from pathlib import Path
dataset_name="test-dataset"
wavs = ''+dataset_name+'/wavs'
 
model = whisper.load_model("medium.en")
paths = glob.glob(os.path.join(wavs, '*.wav'))
print(len(paths))
 
all_filenames = []
transcript_text = []
with open(''+dataset_name+'/metadata.csv', 'w', encoding='utf-8') as outfile:
	for filepath in paths:
		base = os.path.basename(filepath)
		all_filenames.append(base)
	for filepath in paths:
		result = model.transcribe(filepath)
		output = result["text"].lstrip()
		output = output.replace("\n","")
		thefile = str(os.path.basename(filepath).lstrip(".")).rsplit(".")[0]
		outfile.write(thefile + '|' + output + '|' + output + '\n')
		print(thefile + '|' + output + '|' + output + '\n')
