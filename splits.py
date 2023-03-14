import os
import glob
import pydub
import pathlib
import argparse
import tempfile
import shutil
from typing import List

class FileSpliter:
	def __init__(self, source: str, destination: str, silence_threshs: List[int], min_silence_lens: List[int]):
		self.source = source
		self.destination = destination
		self.silence_threshs = silence_threshs
		self.min_silence_lens = min_silence_lens
		self.min_audio_len = 2500
		self.max_audio_len = 15000
		
	def split(self):
		# get tempdir
		tempdir = tempfile.TemporaryDirectory()
		
		chunk_nums_temp = {}
		chunk_nums_out = {}

		# move all files to tempdir
		audiofiles_src = glob.glob(self.source)
		for audiofile in audiofiles_src:
			stem = pathlib.Path(audiofile).stem
			dir_per_audio = os.path.join(tempdir.name, stem)
			os.mkdir(dir_per_audio)
			chunk_nums_temp[stem] = 1
			chunk_nums_out[stem] = 0
			shutil.move(audiofile, os.path.join(dir_per_audio, '0.wav'))
		
		for silence_thresh, min_silence_len in zip(self.silence_threshs, self.min_silence_lens):
			stems = chunk_nums_temp.keys()

			for stem in stems:
				print(stem)

				dir = os.path.join(tempdir.name, stem)
				audiofiles = glob.glob(dir + '/*.wav')
				
				for audiofile in audiofiles:
					signal = pydub.AudioSegment.from_file(audiofile, format='wav')
					chunks = pydub.silence.split_on_silence(signal, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=50)
					
					for chunk in chunks:
						if len(chunk) < self.min_audio_len:
							pass
						elif len(chunk) > self.max_audio_len:
							chunk_num_temp = chunk_nums_temp[stem]
							chunk.export(os.path.join(dir, f'{chunk_num_temp}.wav'), format='wav')
							chunk_nums_temp[stem] = chunk_num_temp + 1
						else:
							chunk_num_out = chunk_nums_out[stem]
							chunk.export(os.path.join(self.destination, f'{stem}-CHUNK-{chunk_num_out}.wav'), format='wav')
							chunk_nums_out[stem] = chunk_num_out + 1
					# delete file from tempdir
					os.remove(audiofile)

					# os.system(f"sox {file_path} {out_dir}/{stem}.wav --show-progress trim 0 8 : newfile : restart")

		# close tempdir
		tempdir.cleanup()
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = 'Splits',
		description = 'Splits wav files into chunks on silence.'
		)
	parser.add_argument('-t', '--thresholds', action='store', dest='silence_threshs', nargs="*", type=int,
		default=[-45], help='Threshold below which audio is considered silent. Default: [-45].')
	parser.add_argument('-l', '--lengths-silence', action='store', dest='min_silence_lens', nargs="*", type=int,
		default=[300], help='Length of silence in miliseconds on which splitting happens. Default: [300].')
	parser.add_argument('-s', '--source', action='store', dest='source', type=str,
		default='audiofiles/raw', help='Path to raw audio. Default: audiofiles/raw')
	parser.add_argument('-d', '--destiantion', action='store', dest='destination', type=str,
		default='audiofiles/splits', help='Path to director to store audio chunks. Default: audiofiles/splits')
	
	parsed = parser.parse_args()
	
	# check if good number of arguments are passed
	if len(parsed.silence_threshs) != len(parsed.min_silence_lens):
		print("List of --thresholds has to have same number of elements as --lengths-silence!")
		exit(1)
	
	
	# get tempdir
	tempdir = tempfile.TemporaryDirectory()
	
	# clear splits directory
	os.system(f"rm {parsed.destination}/*")
	
	# convert mp3 to proper wav
	os.system(f"find {parsed.source} -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .mp3 $f)\".wav -loglevel error; done' _ {{}} +")

	# convert wav to proper wav
	os.system(f"find {parsed.source} -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .wav $f)\".wav -loglevel error; done' _ {{}} +")
	
	# do split files
	fileSpliter = FileSpliter(source=f"{tempdir.name}/*.wav", destination=f"{parsed.destination}", silence_threshs=parsed.silence_threshs, min_silence_lens=parsed.min_silence_lens)
	fileSpliter.split()
	
	# close tempdir
	tempdir.cleanup()

