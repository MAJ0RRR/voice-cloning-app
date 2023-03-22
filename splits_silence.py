import os
import argparse
import tempfile
from FileSpliter import FileSpliter

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
	fileSpliter = FileSpliter(f"{tempdir.name}/*.wav", f"{parsed.destination}")
	fileSpliter.split_silence(parsed.silence_threshs, parsed.min_silence_lens)
	
	# close tempdir
	tempdir.cleanup()

