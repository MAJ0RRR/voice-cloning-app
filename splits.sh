#!/bin/bash

# clear temp direcotry

rm -r $1/audiofiles/temp/*

# clear splits directory
rm -r $1/audiofiles/splits/*
# convert mp3 to proper wav
find "$1/audiofiles/raw" -name '*.mp3' -exec bash -c 'for f; do ffmpeg -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "$1/audiofiles/temp/$(basename "$f" .mp3)".wav; done' _ "$1" {} +

# convert wav to proper wav
find "$1/audiofiles/raw" -name '*.wav' -exec bash -c 'for f; do ffmpeg -y -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "$1/audiofiles/temp/$(basename -s .wav $f)".wav; done' _ "$1" {} +

# do split files
find "$1/audiofiles/temp" -name '*.wav' -exec bash -c 'for f; do sox "$f" "$1/audiofiles/splits/$(basename -s .wav $f)".wav --show-progress trim 0 8 : newfile : restart ; done' _ "$1" {} +

# remove files that are to small
find $1/audiofiles/splits -name "*.wav" -type f -size -30k -delete


