from TTS.api import TTS

import argparse
import os
import shutil


def gen_audio_from_model(model_path: str, config_path: str, out_path: str, sentences: list[str]) -> None:
    # load model with config
    tts = TTS(model_path=model_path, config_path=config_path)
    
    # iterate over sentences
    for i, sentence in enumerate(sentences):
        # do tts
        tts.tts_to_file(text=sentence, file_path=os.path.join(out_path ,f'{i}.wav'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'get_audio',
        description = 'Generates audio from given sentences and models.'
    )
    parser.add_argument('-m', '--models-path', action='store', dest='models_path', type=str,
        default='audio_generation/models', help='Path to models from which audio will be generated. Default: audio_generation/models.')
    parser.add_argument('-o', '--out-path', action='store', dest='out_path', type=str,
		default='audio_generation/out', help='Path to where audio will be generated. For each directory in --models-path new direcory will be created. Default: audio_generation/out')
    parser.add_argument('-s', '--sentences-path', action='store', dest='sentences_path', type=str,
		default='audio_generation/sentences.txt', help='Path to txt file with sentences. Default: audio_generation/sentences.txt')
	
    parsed = parser.parse_args()

    # read sentences from file
    with open(parsed.sentences_path, encoding='UTF-8') as f:
        sentences = f.read().splitlines()

    # get all subfolders in direcotry with models
    subfolders = [ {'name': f.name, 'path': f.path} for f in os.scandir(parsed.models_path) if f.is_dir() ]

    # iterate over all folders with models
    for subfolder in subfolders:
        # out path for specific model
        out_path_per_model = os.path.join(parsed.out_path, subfolder['name'])

        # delete out path if it exists
        if os.path.exists(out_path_per_model):
            shutil.rmtree(out_path_per_model)
        
        # make directory for output
        os.makedirs(out_path_per_model)
        
        
        model_path = [f.path for f in os.scandir(subfolder['path']) if f.name.endswith('.pth')][0]
        config_path = [f.path for f in os.scandir(subfolder['path']) if f.name.endswith('.json')][0]

        gen_audio_from_model(model_path=model_path, config_path=config_path, out_path=out_path_per_model, sentences=sentences)
