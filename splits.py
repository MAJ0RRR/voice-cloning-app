import os
import glob

def split_file(file_path, out_dir):
	os.system(f"sox {file_path} \"{out_dir}/$(basename -s .wav {file_path})\".wav --show-progress trim 0 8 : newfile : restart")

if __name__ == "__main__":
	# clear temp directory
	os.system("rm audiofiles/temp/*")
	
	# clear splits directory
	os.system("rm audiofiles/splits/*")
	
	# convert mp3 to proper wav
	os.system("find audiofiles/raw -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"audiofiles/temp/$(basename -s .mp3 $f)\".wav; done' _ {} +")

	# convert wav to proper wav
	os.system("find audiofiles/raw -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i \"$f\" -acodec pcm_s16le -ar 22050 -ac 1 \"audiofiles/temp/$(basename -s .wav $f)\".wav; done' _ {} +")

	# do split files
	audiofiles = glob.glob("audiofiles/temp/*.wav")
	for audiofile in audiofiles:
		split_file(audiofile, "audiofiles/splits")
	
	# remove files that are to small
	os.system("find audiofiles/splits -name \"*.wav\" -type f -size -30k -delete")
