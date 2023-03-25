import os

from splits_equal import split_equal
from splits_silence import split_silence
from noise import remove_noise
from whispertrans import create_transcription
from discard_transcriptions import discard_transcriptions
from distutils.dir_util import copy_tree

if __name__ == "__main__":
    gpu_num = "2"

    silence_split_type = "equal"
    remove_noises = True
    discard = True

    raw_audio = "audiofiles/raw"
    split_audio = "audiofiles/splits"
    split_len = 8

    split_min_silence_lens = [300]
    split_silence_threshs = [-45]

    dataset_name = "dataset"
    dataset_dir = "audiofiles/datasets"
    dataset_path = os.path.join(dataset_dir, dataset_name)

    language = "en"
    whisper_vram = 10
    discard_word_count = 3

    model_path = None
    run_name = "experimental"

    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_num   

    if silence_split_type == "equal":
        split_equal(split_audio, raw_audio,length=split_len)
    else:
        split_silence(split_audio, raw_audio, split_silence_threshs, split_min_silence_lens)

    if remove_noises:
        remove_noise(split_audio, dataset_name)
    else:
        copy_tree(split_audio, dataset_path)

    create_transcription(os.getcwd(), dataset_name, language, whisper_vram)

    if discard:
        discard_transcriptions(language, dataset_path, discard_word_count)

    train(model_path, dataset_name, language, run_name)

