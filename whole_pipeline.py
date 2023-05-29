import argparse
import os
import subprocess
import time
from pydub import AudioSegment
from distutils.dir_util import copy_tree
import glob

from splits_equal import split_equal
from splits_silence import split_silence
from noise import remove_noise
from whispertrans import create_transcription
from discard_transcriptions import discard_transcriptions
from train import train

DEFAULT_PROCESS_RUNTIME_SECONDS = 32400
DEFAULT_TRIM_SOURCE_LENGTH = 0
DEFAULT_SILENCE_SPLIT_TYPE = "equal"
DEFAULT_SPLIT_LEN = 8
DEFAULT_SPLIT_MIN_SILENCE_LENS = [300]
DEFAULT_SPLIT_SILENCE_THRESHS = [-45]
DEFAULT_REMOVE_NOISES = True
DEFAULT_DATASET_NAME = "dataset"
DEFAULT_WHISPER_VRAM = 10
DEFAULT_DISCARD_TRANSCRIPTS = True
DEFAULT_DISCARD_WORD_COUNT = 3
DEFAULT_LANGUAGE = "en"
DEFAULT_MODEL_PATH = None
DEFAULT_RUN_NAME = "experiment"

def run_and_kill_after(func, timeout):
    p = subprocess.Popen(["python", "-c", func], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_count = 0
    step = 10
    while time_count < timeout:
        print(f'Function is already running for {time_count} / {timeout} seconds, waiting for additional {step} seconds')
        time_count += step
        time.sleep(step)
        
        return_code = p.poll()
        if return_code is not None:
            print('Got output from function:')
            stdout, stderr = p.communicate()
            print('STDOUT:')
            print(stdout.decode())
            print('STDERR:')
            print(stderr.decode())
            print(f'Process finished with code: {return_code}')
            break

    if p.poll() is None:
        p.kill()
        raise TimeoutError("Subprocess timed out after {} seconds".format(timeout))
    
def trim_wavs(source, destinantion, desired_len_ms):
    len_sum = 0
    audiofiles_src = glob.glob(source + "/*")
    for idx, audiofile in enumerate(audiofiles_src):
        ext = os.path.splitext(audiofile)[1]
        if ext == ".wav":
            audio_segment = AudioSegment.from_wav(audiofile)
        elif ext == ".mp3":
            audio_segment = AudioSegment.from_mp3(audiofile)
        else:
            print(f'UNSUPPORTED EXTENSION:{ext}, {audiofile}')
        len_sum += len(audio_segment)
        if len_sum > desired_len_ms:
            trimmed_len = len_sum - desired_len_ms
            trimmed_audio_segment = audio_segment[:-trimmed_len]
        else:
            trimmed_audio_segment = audio_segment
        # Export the trimmed audio segment as a wav file
        dest_file = os.path.join(destinantion, str(idx) + ext)
        trimmed_audio_segment.export(dest_file, format=ext[1:])
        if len_sum >= desired_len_ms:
            break


def run_pipeline(gpu_num, experiment_dir, raw_source, trim_source_length=DEFAULT_TRIM_SOURCE_LENGTH,
                 silence_split_type=DEFAULT_SILENCE_SPLIT_TYPE, split_len=DEFAULT_SPLIT_LEN,
                 split_min_silence_lens=DEFAULT_SPLIT_MIN_SILENCE_LENS,
                 split_silence_threshs=DEFAULT_SPLIT_SILENCE_THRESHS, remove_noises=DEFAULT_REMOVE_NOISES,
                 dataset_name=DEFAULT_DATASET_NAME, whisper_vram=DEFAULT_WHISPER_VRAM,
                 discard_transcripts=DEFAULT_DISCARD_TRANSCRIPTS, discard_word_count=DEFAULT_DISCARD_WORD_COUNT,
                 language=DEFAULT_LANGUAGE, model_path=DEFAULT_MODEL_PATH, run_name=DEFAULT_RUN_NAME,
                 timeout_seconds=DEFAULT_PROCESS_RUNTIME_SECONDS):

    splits_dir = os.path.join(experiment_dir, 'splits')
    datasets_dir = os.path.join(experiment_dir, 'datasets')
    dataset_dir = os.path.join(datasets_dir, dataset_name)

    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_num)

    if not os.path.exists(splits_dir):
        os.makedirs(splits_dir)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    
    if trim_source_length == 0:
        audio_source = raw_source
    else:
        audio_source = os.path.join(experiment_dir, 'trimmed')
        os.makedirs(audio_source)
        trim_wavs(raw_source, audio_source, trim_source_length)

    if silence_split_type == "equal":
        split_equal(splits_dir, audio_source, length=split_len)
    else:
        split_silence(splits_dir, audio_source, split_silence_threshs, split_min_silence_lens)
    
    if remove_noises:
        remove_noise(splits_dir, dataset_dir)
    else:
        copy_tree(splits_dir, os.path.join(dataset_dir,"wavs"))
    
    create_transcription(dataset_dir, language, whisper_vram)

    if discard_transcripts:
        discard_transcriptions(language, dataset_dir, discard_word_count)

    train_func = """from train import train\ntrain( "", '{}', '{}', '{}', '{}', '{}')""".format(
        model_path, dataset_name,language, run_name, datasets_dir)
    print(train_func)
    try:
        run_and_kill_after(train_func, timeout_seconds)
    except TimeoutError as e:
        print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='whole_pipeline',
        description='Runs whole pipeline for automated voice cloning'
        )

    parser.add_argument('--gpu', action='store', dest='gpu', help='GPU number')
    parser.add_argument('--run_dir', action='store', dest='experiment_dir', help='Directory where processed audio will be stored')
    parser.add_argument('--raw_source', action='store', dest='raw_source', help='Directory with raw audio samples')

    parser.add_argument('--trim_source_length', action='store', dest='trim_source_length', default=DEFAULT_TRIM_SOURCE_LENGTH, type=int,
                        help=f'Length to which the input audio will be cut in minutes.  Default {DEFAULT_TRIM_SOURCE_LENGTH}')
    parser.add_argument('--silence_split_type', action='store', dest='silence_split_type', default=DEFAULT_SILENCE_SPLIT_TYPE, type=str,
                        help=f'Method using which input samples will be split into chunks, can be "equal" or "silence". Default {DEFAULT_SILENCE_SPLIT_TYPE}')
    parser.add_argument('--split_len', action='store', dest='split_len', default=DEFAULT_SPLIT_LEN, type=int,
                        help=f'Length to which the input samples will be cut. Used only if silence_split_type = "equal". Default {DEFAULT_SPLIT_LEN}')
    parser.add_argument('--split_min_silence_lens', action='store', dest='split_min_silence_lens', default=DEFAULT_SPLIT_MIN_SILENCE_LENS, nargs="*", type=int,
                        help=f'Lengths of silence in miliseconds on which splitting happens. Used only if silence_split_type = "silence". Default {DEFAULT_SPLIT_MIN_SILENCE_LENS}')
    parser.add_argument('--split_silence_threshs', action='store', dest='split_silence_threshs', default=DEFAULT_SPLIT_SILENCE_THRESHS, nargs="*", type=int,
                        help=f'Thresholds below which audio is considered silent. Used only if silence_split_type = "silence". Default {DEFAULT_SPLIT_SILENCE_THRESHS}')
    parser.add_argument('--remove_noises', action='store', dest='remove_noises', default=DEFAULT_REMOVE_NOISES, type=bool,
                        help=f'Remove noises when processing audio. Default {DEFAULT_REMOVE_NOISES}')
    parser.add_argument('--dataset_name', action='store', dest='dataset_name', default=DEFAULT_DATASET_NAME, type=str,
                        help=f'Name of dataset directory. Default {DEFAULT_DATASET_NAME}')
    parser.add_argument('--whisper_vram', action='store', dest='whisper_vram', default=DEFAULT_WHISPER_VRAM, type=int,
                        help=f'VRAM available to Whisper STT. Default {DEFAULT_WHISPER_VRAM}')
    parser.add_argument('--discard_transcripts', action='store', dest='discard_transcripts', default=DEFAULT_DISCARD_TRANSCRIPTS, type=bool,
                        help=f'Discard faulty transcripts while processing audio. Default {DEFAULT_DISCARD_TRANSCRIPTS}')
    parser.add_argument('--discard_word_count', action='store', dest='discard_word_count', default=DEFAULT_DISCARD_WORD_COUNT, type=int,
                        help=f'Minimum sentence length in words. Used only if discard_transcripts = true. Default {DEFAULT_DISCARD_WORD_COUNT}')
    parser.add_argument('--language', action='store', dest='language', default=DEFAULT_LANGUAGE, type=str,
                        help=f'Input language, either "en" or "pl. Default {DEFAULT_LANGUAGE}')
    parser.add_argument('--model_path', action='store', dest='model_path', default=DEFAULT_MODEL_PATH, type=str,
                        help=f'Path to base model. If not provided new one will be created. Default {DEFAULT_MODEL_PATH}')
    parser.add_argument('--run_name', action='store', dest='run_name', default=DEFAULT_RUN_NAME, type=str,
                        help=f'Run directory name. Default {DEFAULT_RUN_NAME}')
    parser.add_argument('--timeout_seconds', action='store', dest='timeout_seconds', default=DEFAULT_PROCESS_RUNTIME_SECONDS, type=int,
                        help=f'Time in seconds after which model training will be finished. Default {DEFAULT_PROCESS_RUNTIME_SECONDS}')

    parsed = parser.parse_args()
