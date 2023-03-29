from whole_pipeline import run_pipeline
import json


DEFINITIONS_FILE_NAME = "definitions.json"
def generate_definitions(name_idx_start=0, raw_sources=None, trim_source_lengths_mins=None, silence_split_types=None, split_lengths=None,
                 split_min_silence_lens=None, split_silence_threshs=None, remove_noises=None, discard_transcripts=None, discard_word_counts=None, languages_and_models=None,):
    defs = []
