import csv
import os

def is_valid_string(string,alphabet,symbols):
    for char in string.upper():
        if char not in alphabet:
            return char in symbols
    return True

if __name__ == "__main__":
    polish_alphabet = ['A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'Ń', 'O', 'Ó', 'P', 'Q', 'R', 'S', 'Ś', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ź', 'Ż']
    symbols = [' ',',','.','?','!']
    
    with open('audiofiles/datasets/dataset/metadata.csv') as orginal, \
        open('audiofiles/datasets/dataset/filtered.csv', 'w') as filtered:
        transcript = csv.reader(orginal, delimiter='|')

        for row in transcript:
            valid = True
            for substring in str.split(row[1]," "):
                if not is_valid_string(substring,polish_alphabet,symbols):
                    valid = False

            if valid:
                for element in row[:-1]:
                    filtered.write(element)
                    filtered.write('|')
                filtered.write(row[-1])
                filtered.write("\n")

            else:
                os.remove(f"audiofiles/wavs/{row[0]}.wav")

    os.remove('audiofiles/datasets/dataset/metadata.csv')
    os.rename('audiofiles/datasets/dataset/filtered.csv','audiofiles/datasets/dataset/metadata.csv')




