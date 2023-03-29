import json
from ..whole_pipeline import run_pipeline

DEFINITIONS_FILE_NAME = "definitions.json"

def run_experiments():
    with open(DEFINITIONS_FILE_NAME, 'r') as file:
        definitions = json.load(file.read())
    
    whisper_vram = definitions["WhisperVram"]
    gpu = definitions["Gpu"]
    experiments = definitions["Definitions"]

    for experiment in experiments:
        name = experiment["Name"]
        raw_source = experiment["RawSource"]
        trim_source = experiment["TrimSourceLengthMs"]
        split_type = experiment["SilenceSplitType"]
        split_len = None
        thresh = None
        silence_len = None
        remove_noise = experiment["RemoveNoise"]
        language = experiment["Language"]
        discard_transcripts = experiment["DiscardTranscripts"]
        discard_words_len = experiment["DiscardWordCount"]
        model_path = experiment["ModelPath"]
        
        if split_type == 'equal':
            split_len = experiment["SplitSilenceLength"]
        elif split_type == 'silence':
            thresh = experiment["SplitSilenceThresh"]   
            silence_len = experiment["SplitSilenceMinLength"]

        run_pipeline(gpu_num=gpu, experiment_dir=name, raw_source=raw_source, trim_source_length=trim_source, silence_split_type=split_type, split_len=split_len, split_min_silence_lens=silence_len, split_silence_threshs=thresh, remove_noises=remove_noise, discard_transcripts=discard_transcripts, discard_word_count=discard_words_len, language=language, model_path=model_path)