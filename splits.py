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
		
		# move all files to tempdir
		audiofiles_src = glob.glob(self.source)
		for audiofile in audiofiles_src:
			basename = os.path.basename(audiofile)
			shutil.move(audiofile, os.path.join(tempdir.name, basename))
		
		for silence_thresh, min_silence_len in zip(self.silence_threshs, self.min_silence_lens):
			audiofiles = glob.glob(tempdir.name + '/*.wav')
			
			for audiofile in audiofiles:
				print(audiofile)
			
				# self.__split_file(audiofile, self.destination)
				signal = pydub.AudioSegment.from_file(audiofile, format='wav')
				chunks = pydub.silence.split_on_silence(signal, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=50)
				
				stem = pathlib.Path(audiofile).stem
				
				for i, chunk in enumerate(chunks):
					file_name = f'CHUNK-{i}-{stem}.wav'
					if len(chunk) < self.min_audio_len:
						pass
					elif len(chunk) > self.max_audio_len:
						chunk.export(os.path.join(tempdir.name, file_name), format='wav')
					else:
						chunk.export(os.path.join(self.destination, file_name), format='wav')
				# delete file from tempdir
				os.remove(audiofile)
		
		# close tempdir
		tempdir.cleanup()
		
	'''	
	def __split_file(self, file_path: str, out_dir: str) -> (int, int):
		signal = pydub.AudioSegment.from_file(file_path, format='wav')
		chunks = pydub.silence.split_on_silence(signal, min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh, keep_silence=50)
		
		stem = pathlib.Path(file_path).stem
		
		for i, chunk in enumerate(chunks):
			file_name = f'CHUNK-{i}-{stem}.wav'
			chunk.export(os.path.join(out_dir, file_name), format='wav')
		
		return 0, 0	
		
		#os.system(f"sox {file_path} {out_dir}/{stem}.wav --show-progress trim 0 8 : newfile : restart")
	'''

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

