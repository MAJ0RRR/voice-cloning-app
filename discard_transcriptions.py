"""
This script discards transcriptions that contain illegal symbols or doesn't meet criterias
from `metadata.csv` file and deltes according `*.wav` file.
"""

import argparse
import csv
import os


def is_valid_string(string,alphabet,symbols):
    for char in string.upper():
        if char not in alphabet:
            if char not in symbols:
                return False
    return True

def discard_transcriptions(alph: str = 'en', path: str = 'audiofiles/datasets/dataset', word_count: int = 3):
    polish_alphabet = list("AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ")
    english_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    symbols = list(" ,.?!-0123456789")
    min_words = 3

    alphabets = {
        "pl" : polish_alphabet,
        "en" : english_alphabet
    }
 
    alphabet = alphabets[alph]
    root = path
    min_words = word_count
    
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
    parser = argparse.ArgumentParser(
        prog = 'discard_transcriptions',
        description = 'Deletes files and entries in csv with wrong transcription.'
        )
    parser.add_argument('-l', '--language', action='store', dest='language', 
        default='en', help='Language of speech in your data (en/pl). Default: en.')
    parser.add_argument('-s', '--source-directory', action='store', dest='source_dir', 
        default='audiofiles/datasets/dataset', help='Directory with dataset. Default: audiofiles/datasets/dataset.')
    parser.add_argument('-m', '--min-words', action='store', dest='min_words', 
        default=3, type=int, help='Minimal number of words in transriptions. Default: 3')

    parsed = parser.parse_args()

    assert parsed.language in ('en', 'pl'), f'incorrect language ID, language={parsed.language}'

    discard_transcriptions(alph=parsed.language, path=parsed.source_dir, word_count=parsed.min_words)
