import os
import glob
import pydub
import pathlib
from typing import List

class FileSpliter:
	def __init__(self, source: str, destination: str):
		self.source = source
		self.destination = destination
		
	def split_silence(self, silence_threshs: List[int], min_silence_lens: List[int], min_audio_len: int = 2500, max_audio_len: int = 15000):
		# iterate over all files
		audiofiles_src = glob.glob(self.source)
		for audiofile in audiofiles_src:
			stem = pathlib.Path(audiofile).stem
			len_saved = 0
			print(f'Spliting: {stem}')
			chunk_num_out = 0
			signal = pydub.AudioSegment.from_file(audiofile, format='wav')
			chunks = [signal]
			for silence_thresh, min_silence_len in zip(silence_threshs, min_silence_lens):
				chunks_new_iter = []
				for chunk in chunks:
					new_chunks = pydub.silence.split_on_silence(chunk, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=50)
					for new_chunk in new_chunks:
						if len(new_chunk) < min_audio_len:
							pass
						elif len(new_chunk) > max_audio_len:
							chunks_new_iter.append(new_chunk)
						else:
							len_saved += len(new_chunk)
							new_chunk.export(os.path.join(self.destination, f'{stem}-CHUNK-{chunk_num_out}.wav'), format='wav')
							chunk_num_out = chunk_num_out + 1
				chunks = chunks_new_iter
			print(f'{(len_saved/len(signal) * 100):.2f}% is used')

	def split_length(self, length: int):
		audiofiles_src = glob.glob(self.source)
		for audiofile in audiofiles_src:
			os.system(f"sox {audiofile} \"{self.destination}/$(basename -s .wav {audiofile})\".wav --show-progress trim 0 {length} : newfile : restart")
