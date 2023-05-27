import itertools
from typing import List
from typing import Optional

import json

DEFINITIONS_FILE_NAME = "experiments/definitions.json"
DESCRIPTION_FILE_NAME = "experiments/experiments_description.json"


class ParametersSet:
    def __init__(self, name: str, source: dict, trim_len: int, split_type: str, remove_noise: bool,
                 discard: int, split_length: Optional[int] = None, split_min_silence_len: Optional[List[int]] = None,
                 split_silence_thresh: Optional[List[int]] = None):
        self.name = name
        self.source = source
        self.trim_len = trim_len
        self.split_type = split_type
        self.remove_noise = remove_noise
        self.discard = discard
        self.split_length = split_length
        self.split_min_silence_len = split_min_silence_len
        self.split_silence_thresh = split_silence_thresh


def _set_definition_values(params: ParametersSet):
    definition = {}
    definition["Name"] = params.name
    definition["RawSource"] = params.source["RawSource"]
    definition["TrimSourceLengthMs"] = params.trim_len * 60 * 1000
    definition["ModelPath"] = params.source["ModelPath"]
    definition["Language"] = params.source["Language"]
    definition["SilenceSplitType"] = params.split_type
    definition["RemoveNoise"] = params.remove_noise
    definition["DiscardTranscripts"] = True
    definition["DiscardWordCount"] = params.discard
    definition["SplitSilenceLength"] = params.split_length
    definition["SplitSilenceMinLength"] = params.split_min_silence_len
    definition["SplitSilenceThresh"] = params.split_silence_thresh

    return definition


def generate_definitions_product(name_idx_start: int = 0, sources: List[dict] = None,
                                 trim_source_lengths_mins: List[int] = None,
                                 silence_split_types: List[str] = None, split_lengths: List[int] = None,
                                 split_min_silence_lens: List[List[int]] = None, split_silence_threshs: List[List[int]] = None,
                                 remove_noises: List[bool] = None, discard_word_counts: List[int] = None,
                                 whisper_vram: int = 8, gpu: int = 0):
    """
    :param gpu: int - GPU number
    :param whisper_vram: int - RAM memory available for whisper in GB
    :param name_idx_start: Start index for experiment names
    :param sources: List of dicts - elements should be given in format
        {"RawSource": str, "ModelPath": str, "Language": str}
    :param trim_source_lengths_mins: List of lengths to which input audios will be trimmed
    :param silence_split_types: List of silence split types - elements can be either 'equal' or 'silence'
    :param split_lengths: List of split lengths for split_equal
    :param split_min_silence_lens: List of min silence lengths for split_silence
    :param split_silence_threshs: List of silence threshs for split_silence
    :param remove_noises: List - elements can be either true or false
    :param discard_word_counts: List of ints - 0 means no transcripts are discarded
    :return: None
    """

    defs = []
    args = itertools.product(sources, trim_source_lengths_mins, silence_split_types, remove_noises, discard_word_counts)

    name_idx_count = name_idx_start
    name_base = "experiment_"
    for source, trim_len, split_type, remove_noise, discard in args:

        if split_type == 'equal':
            for length in split_lengths:
                params = ParametersSet(name=f'{name_base}{name_idx_count}', source=source, trim_len=trim_len,
                                       split_type=split_type, remove_noise=remove_noise,
                                       discard=discard, split_length=length)
                defs.append(_set_definition_values(params))
                name_idx_count += 1

        elif split_type == 'silence':
            for silence_len, thresh in zip(split_min_silence_lens, split_silence_threshs):
                params = ParametersSet(name=f'{name_base}{name_idx_count}', source=source, trim_len=trim_len,
                                       split_type=split_type, remove_noise=remove_noise, discard=discard,
                                       split_min_silence_len=silence_len, split_silence_thresh=thresh)
                defs.append(_set_definition_values(params))
                name_idx_count += 1

    output = {
        "Definitions": defs,
        "Gpu": gpu,
        "WhisperVram": whisper_vram
    }

    with open(DEFINITIONS_FILE_NAME, 'w') as file:
        file.write(json.dumps(output))


def generate_definitions_diff(default_params: ParametersSet, name_idx_start: int = 0, sources: List[dict] = None,
                              trim_source_lengths_mins: List[int] = None,
                              silence_split_types: List[str] = None, split_lengths: List[int] = None,
                              split_min_silence_lens: List[List[int]] = None, split_silence_threshs: List[List[int]] = None,
                              remove_noises: List[bool] = None, discard_word_counts: List[int] = None,
                              whisper_vram: int = 8, gpu: int = 0):
    """
    :param default_params: default parameters
    :param gpu: int - GPU number
    :param whisper_vram: int - RAM memory available for whisper in GB
    :param name_idx_start: Start index for experiment names
    :param sources: List of dicts - elements should be given in format
        {"RawSource": str, "ModelPath": str, "Language": str}
    :param trim_source_lengths_mins: List of lengths to which input audios will be trimmed
    :param silence_split_types: List of silence split types - elements can be either 'equal' or 'silence'
    :param split_lengths: List of split lengths for split_equal
    :param split_min_silence_lens: List of min silence lengths for split_silence
    :param split_silence_threshs: List of silence threshs for split_silence
    :param remove_noises: List - elements can be either true or false
    :param discard_word_counts: List of ints - 0 means no transcripts are discarded
    :return: None
    """
    params = []
    name_idx_count = name_idx_start
    name_base = "experiment_"

    for source in sources:
        param_set = default_params
        param_set.source = source
        name_idx_count += 1
        param_set.name = f'{name_base}{name_idx_count}'
        params.append(param_set)

    for trim_len in trim_source_lengths_mins:
        param_set = default_params
        param_set.trim_len = trim_len
        name_idx_count += 1
        param_set.name = f'{name_base}{name_idx_count}'
        params.append(param_set)

    for noise in remove_noises:
        param_set = default_params
        param_set.remove_noise = noise
        name_idx_count += 1
        param_set.name = f'{name_base}{name_idx_count}'
        params.append(param_set)

    for source in sources:
        param_set = default_params
        param_set.source = source
        name_idx_count += 1
        param_set.name = f'{name_base}{name_idx_count}'
        params.append(param_set)

    for count in discard_word_counts:
        param_set = default_params
        param_set.discard = count
        name_idx_count += 1
        param_set.name = f'{name_base}{name_idx_count}'
        params.append(param_set)

    for type in silence_split_types:
        if type == 'equal':
            for length in split_lengths:
                param_set = default_params
                param_set.split_type = type
                param_set.split_length = length
                name_idx_count += 1
                param_set.name = f'{name_base}{name_idx_count}'
                params.append(param_set)
        elif type == 'silence':
            for length in split_min_silence_lens:
                param_set = default_params
                param_set.split_type = type
                param_set.split_min_silence_len = length
                name_idx_count += 1
                param_set.name = f'{name_base}{name_idx_count}'
                params.append(param_set)
            for thresh in split_silence_threshs:
                param_set = default_params
                param_set.split_type = type
                param_set.split_silence_thresh = thresh
                name_idx_count += 1
                param_set.name = f'{name_base}{name_idx_count}'
                params.append(param_set)

    defs = [_set_definition_values(p) for p in params]

    output = {
        "Definitions": defs,
        "Gpu": gpu,
        "WhisperVram": whisper_vram
    }

    with open(DEFINITIONS_FILE_NAME, 'w') as file:
        file.write(json.dumps(output))


if __name__ == '__main__':
    with open(DESCRIPTION_FILE_NAME, "r") as file:
        description = json.load(file)

    sources = description["Source"]
    trim_source_lengths_mins = description["TrimSourceLengthMins"]
    silence_split_types = description["SilenceSplitType"]
    split_lengths = description["SplitSilenceLength"]
    split_min_silence_lens = description["SplitSilenceMinLength"]
    split_silence_threshs = description["SplitSilenceThresh"]
    remove_noises = description["RemoveNoise"]
    discard_word_counts = description["DiscardWordCount"]
    gpu = description["Gpu"]
    vram = description["WhisperVram"]

    if description["Mode"] == "diff":
        default_config_json = description["Mode"]["DefaultConfig"]
        default_config = ParametersSet(name="", source=default_config_json["Source"],
                                       trim_len=default_config_json["TrimSourceLengthMs"],
                                       split_type=default_config_json["SilenceSplitType"],
                                       remove_noise=default_config_json["RemoveNoise"],
                                       discard=default_config_json["DiscardWordCount"],
                                       split_length=default_config_json["SplitSilenceLength"],
                                       split_min_silence_len=default_config_json["SplitSilenceMinLength"],
                                       split_silence_thresh=default_config_json["SplitSilenceThresh"])
        generate_definitions_diff(default_config, sources=sources, trim_source_lengths_mins=trim_source_lengths_mins,
                                     silence_split_types=silence_split_types, split_lengths=split_lengths,
                                     split_min_silence_lens=split_min_silence_lens,
                                     split_silence_threshs=split_silence_threshs,
                                     remove_noises=remove_noises, discard_word_counts=discard_word_counts,
                                     whisper_vram=vram, gpu=gpu)
    else:
        generate_definitions_product(sources=sources, trim_source_lengths_mins=trim_source_lengths_mins,
                                     silence_split_types=silence_split_types, split_lengths=split_lengths,
                                     split_min_silence_lens=split_min_silence_lens,
                                     split_silence_threshs=split_silence_threshs,
                                     remove_noises=remove_noises, discard_word_counts=discard_word_counts,
                                     whisper_vram=vram, gpu=gpu)
