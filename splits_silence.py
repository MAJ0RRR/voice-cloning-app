import os
import glob
import pydub
import pathlib
import argparse
import tempfile
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
		# iterate over all files
		audiofiles_src = glob.glob(self.source)
		for audiofile in audiofiles_src:
			stem = pathlib.Path(audiofile).stem
			chunk_num_out = 0
			signal = pydub.AudioSegment.from_file(audiofile, format='wav')
			chunks = [signal]
			for silence_thresh, min_silence_len in zip(self.silence_threshs, self.min_silence_lens):
				chunks_new_iter = []
				for chunk in chunks:
					new_chunks = pydub.silence.split_on_silence(chunk, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=50)
					for new_chunk in new_chunks:
						if len(new_chunk) < self.min_audio_len:
							pass
						elif len(new_chunk) > self.max_audio_len:
							chunks_new_iter.append(new_chunk)
						else:
							new_chunk.export(os.path.join(self.destination, f'{stem}-CHUNK-{chunk_num_out}.wav'), format='wav')
							chunk_num_out = chunk_num_out + 1
				chunks = chunks_new_iter	

		# os.system(f"sox {file_path} {out_dir}/{stem}.wav --show-progress trim 0 8 : newfile : restart")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = 'splits_silence',
		description = 'Splits wav files into chunks on silence.'
		)
	parser.add_argument('-t', '--thresholds', action='store', dest='silence_threshs', nargs="*", type=int,
		default=[-45], help='Thresholds below which audio is considered silent. Default: [-45].')
	parser.add_argument('-l', '--lengths-silence', action='store', dest='min_silence_lens', nargs="*", type=int,
		default=[300], help='Lengths of silence in miliseconds on which splitting happens. Default: [300].')
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

