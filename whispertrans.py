import whisper
import sys
import os, os.path
import glob
import pandas as pd
import argparse
from pathlib import Path


def create_transcription(dataset_path, language, vram):

    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)

    wavs_path = os.path.join(dataset_path, 'wavs')
    if language == 'en':
        if vram >= 5:
            model_name = 'medium.en'
        elif vram >= 2:
            model_name = 'small.en'
        else:
            model_name = 'base.en'
    elif language == 'pl':
        if vram >= 10:
            model_name = 'large'
        elif vram >= 5:
            model_name = 'medium'
        elif vram >= 2:
            model_name = 'small'
        else:
            model_name = 'base'
    else:
        print('wrong language')
        return
    print(model_name)
    model = whisper.load_model(model_name)

    paths = glob.glob(os.path.join(wavs_path, '*.wav'))
    print(len(paths))

    all_filenames = []
    transcript_text = []
    with open(os.path.join(dataset_path, 'metadata.csv'), 'w', encoding='utf-8') as outfile:
        for filepath in paths:
            base = os.path.basename(filepath)
            all_filenames.append(base)
        for filepath in paths:
            result = model.transcribe(filepath)
            output = result["text"].lstrip()
            output = output.replace("\n", "")
            thefile = str(os.path.basename(filepath).lstrip(".")).rsplit(".")[0]
            outfile.write(thefile + '|' + output + '|' + output + '\n')
            print(thefile + '|' + output + '|' + output + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='WhisperTrans',
        description='Creates transcription for given set of audio files (in <dataset_path>) using whisper.'
    )
    parser.add_argument('-l', '--language', action='store', dest='language',
                        default='en', help='Language of speech in your data (en/pl). Default: en.')
    parser.add_argument('-p', '--path', action='store', dest='dataset_path',
                        default='audiofiles/datasets/dataset',
                        help='Dataset path. Default: audiofiles/datasets/dataset.')
    parser.add_argument('-v', '--vram', action='store', dest='vram',
                        default='10', type=int, help='Vram of your graphics card. Default: 10')
    parser.add_argument('-g', '--gpu', action='store', dest='gpu_num',
                        required=True, help='GPU number.')

    result = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = result.gpu_num

    dataset_path = os.path.join(os.getcwd(), result.dataset_path)
    create_transcription(dataset_path, result.language, result.vram)
