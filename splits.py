import os
import glob
import pydub
import pathlib
import argparse
import tempfile

class FileSpliter:
	def __init__(self, source, destination, silence_thresh, min_silence_len):
		self.source = source
		self.destination = destination
		self.silence_thresh = silence_thresh
		self.min_silence_len = min_silence_len
		
	def split(self):
		audiofiles = glob.glob(self.source)
		for audiofile in audiofiles:
			self.__split_file(audiofile, self.destination)
			
	def __split_file(self, file_path, out_dir):
		signal = pydub.AudioSegment.from_file(file_path, format='wav')
		chunks = pydub.silence.split_on_silence(signal, min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh, keep_silence=50)
		
		stem = pathlib.Path(file_path).stem
		
		for i, chunk in enumerate(chunks):
			file_name = f'CHUNK-{i}-{stem}.wav'
			chunk.export(os.path.join(out_dir, file_name), format='wav')
			
		#os.system(f"sox {file_path} {out_dir}/{stem}.wav --show-progress trim 0 8 : newfile : restart")
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = 'Splits',
		description = 'Splits wav files into chunks on silence.'
		)
	parser.add_argument('-t', '--threshold', action='store', dest='silence_thresh', type=int,
		default=-45, help='Threshold below which audio is considered silent. Default: -45.')
	parser.add_argument('-l', '--length-silence', action='store', dest='min_silence_len', type=int,
		default=300, help='Length of silence in miliseconds on which splitting happens. Default: 300.')
	parser.add_argument('-s', '--source', action='store', dest='source', type=str,
		default='audiofiles/raw', help='Path to raw audio. Default: audiofiles/raw')
	parser.add_argument('-d', '--destiantion', action='store', dest='destination', type=str,
		default='audiofiles/splits', help='Path to director to store audio chunks. Default: audiofiles/splits')
	
	parsed = parser.parse_args()
	
	# get tempdir
	tempdir = tempfile.TemporaryDirectory()
	
	# clear splits directory
	os.system(f"rm {parsed.destination}/*")
	
	# convert mp3 to proper wav
	os.system(f"find {parsed.source} -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .mp3 $f)\".wav -loglevel error; done' _ {{}} +")

	# convert wav to proper wav
	os.system(f"find {parsed.source} -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .wav $f)\".wav -loglevel error; done' _ {{}} +")
	
	# do split files
	fileSpliter = FileSpliter(source=f"{tempdir.name}/*.wav", destination=f"{parsed.destination}", silence_thresh=parsed.silence_thresh, min_silence_len=parsed.min_silence_len)
	fileSpliter.split()
	
	# close tempdir
	tempdir.cleanup()

