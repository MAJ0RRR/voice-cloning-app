import os
import glob
import argparse
import tempfile
from file_splitter import FileSpliter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
		prog = 'splits_silence',
		description = 'Splits wav files into chunks on silence.'
		)
    parser.add_argument('-l', '--length', action='store', dest='length', type=int,
		default=8, help='Length of chunk. Default: 8.')
    parser.add_argument('-s', '--source', action='store', dest='source', type=str,
        default='audiofiles/raw', help='Path to raw audio. Default: audiofiles/raw')
    parser.add_argument('-d', '--destiantion', action='store', dest='destination', type=str,
        default='audiofiles/splits', help='Path to director to store audio chunks. Default: audiofiles/splits')

    parsed = parser.parse_args()

    # get tempdir
    tempdir = tempfile.TemporaryDirectory()
	
	# clear splits directory
    if os.path.exists(f"{parsed.destination}/*"):
        os.system(f"rm {parsed.destination}/*")
	
	# convert mp3 to proper wav
    os.system(f"find {parsed.source} -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .mp3 $f)\".wav -loglevel error; done' _ {{}} +")

	# convert wav to proper wav
    os.system(f"find {parsed.source} -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"{tempdir.name}/$(basename -s .wav $f)\".wav -loglevel error; done' _ {{}} +")

	# do split files
    fs = FileSpliter(f"{tempdir.name}/*.wav", 'audiofiles/splits')
    fs.split_length(parsed.length)
	
	# close tempdir
    tempdir.cleanup()

	# remove files that are to small
    os.system(f"find {parsed.destination} -name \"*.wav\" -type f -size -30k -delete")
