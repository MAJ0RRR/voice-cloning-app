"""
This script discards transcriptions that contain illegal symbols or doesn't meet criterias
from `metadata.csv` file and deltes according `*.wav` file.

Usage: # Order of arguments matter!
------
1) Default language and default location
`python3 ./discard.transcriptions.py` 
------
2) Custom language and default location
`python3 ./discard.transcriptions.py pl`
`python3 ./discard.transcriptions.py en`
------
3) Custom language and custom location
`python3 ./discard.transcriptions.py pl /PATH/TO/DATASET`
`python3 ./discard.transcriptions.py en /PATH/TO/DATASET`
------
4) Custom language and custom location with custom min_words limit for ex. 5
`python3 ./discard.transcriptions.py pl /PATH/TO/DATASET 5`
`python3 ./discard.transcriptions.py en /PATH/TO/DATASET 5`
------
"""

import csv
import os
import sys

def is_valid_string(string,alphabet,symbols):
    for char in string.upper():
        if char not in alphabet:
            if char not in symbols:
                return False
    return True

def discard_transciprions(alph="pl",path="audiofiles/datasets/dataset",word_count=3):
    polish_alphabet = list("AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ")
    english_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    symbols = list(" ,.?!")
    min_words = 3

    alphabets = {
        "pl" : polish_alphabet,
        "en" : english_alphabet
    }

    alphabet = []
    root = 'audiofiles/datasets/dataset'

    if __name__ != "__main__": # Invoked through function
        alphabet = alph
        root = path
        min_words = word_count
    else:
        if len(sys.argv) == 1: # Default language in default location
            alphabet = polish_alphabet
        elif len(sys.argv) == 2: # Custom language in default location
            alphabet = alphabets[str(sys.argv[1])]
        elif len(sys.argv) == 3:  # Custom language in custom location
            alphabet = alphabets[str(sys.argv[1])]
            root = str(sys.argv[2])
        else: # Custom language in custom location with custom min_words limit
            alphabet = alphabets[str(sys.argv[1])]
            root = str(sys.argv[2])
            min_words = int(sys.argv[3])
    
    with open(os.path.join(root,'metadata.csv')) as orginal, \
        open(os.path.join(root,'filtered.csv'), 'w') as filtered:
        transcript = csv.reader(orginal, delimiter='|')

        for row in transcript:
            words = len(row[1].split(" "))
            if words <= min_words:
                valid = False
            else:
                valid = True

            if valid:
                for substring in str.split(row[1]," "):
                    if not is_valid_string(substring,alphabet,symbols):
                        valid = False
                        break

            if valid:
                for element in row[:-1]:
                    filtered.write(element)
                    filtered.write('|')
                filtered.write(row[-1])
                filtered.write("\n")
            else:
                if os.path.exists(os.path.join(root,f"wavs/{row[0]}.wav")):
                    print(f"Removing: {row[0]}.wav\n")
                    os.remove(os.path.join(root,f"wavs/{row[0]}.wav"))
                else:
                    print(f"Tried to remove {row[0]}.wav, but it does not exist.")

    os.remove(os.path.join(root,'metadata.csv'))
    os.rename(os.path.join(root,'filtered.csv'),os.path.join(root,'metadata.csv'))


if __name__ == "__main__":
    discard_transciprions()
