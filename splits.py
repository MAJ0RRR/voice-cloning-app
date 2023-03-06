import os
import glob
import pydub
import pathlib

def split_file(file_path, out_dir):
	signal = pydub.AudioSegment.from_file(file_path, format='wav')
	chunks = pydub.silence.split_on_silence(signal, min_silence_len=400, silence_thresh=-50, keep_silence=20)
	
	stem = pathlib.Path(file_path).stem
	
	# check if there are any chunks
	#if not chunks:
	#	file_name = f'CHUNK-0-{stem}.wav'
	#	signal.export(os.path.join(out_dir, file_name), 'wav')
	#	return
	for i, chunk in enumerate(chunks):
		print(len(chunk))
		file_name = f'CHUNK-{i}-{stem}.wav'
		chunk.export(os.path.join(out_dir, file_name), format='wav')
	
	#os.system(f"sox {file_path} {out_dir}/{stem}.wav --show-progress trim 0 8 : newfile : restart")
	

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
