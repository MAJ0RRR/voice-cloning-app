#!/bin/bash

# clear temp direcotry
rm -r audiofiles/temp/*

# clear splits directory
rm -r audiofiles/splits/*

# convert mp3 to proper wav
find audiofiles/raw -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "audiofiles/temp/$(basename -s .mp3 $f)".wav; done' _ {} +

# convert wav to proper wav
find audiofiles/raw -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "audiofiles/temp/$(basename -s .wav $f)".wav; done' _ {} +

# do split files
find audiofiles/temp -name '*.wav' -exec bash -c 'for f; do sox "$f" "audiofiles/splits/$(basename -s .wav $f)".wav --show-progress trim 0 8 : newfile : restart ; done' _ {} +

# remove files that are to small
find audiofiles/splits -name "*.wav" -type f -size -30k -delete


