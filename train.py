from trainer import Trainer, TrainerArgs
from TTS.config import load_config
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
import os
import argparse
import json

OUTPUT_PATH = "output/"
CONFIG_FILE_NAME = "config.json"
DEFAULT_RUN_NAME = "new_model"
DATASETS_DIR = "audiofiles/datasets"
TEST_SENTENCES_FILE = "test_sentences.json"
ROOT_DIR = ""


def validate_input(root_dir, args):
    assert int(args.gpu_num) >= 0, f'gpu_num is smaller than 0, gpu_num={args.gpu_num}'

    assert args.language in ('en', 'pl'), f'incorrect language ID, language={args.language}'

    assert args.run_name, f'run_name cannot be empty'

    assert args.dataset_name, f'dataset_name cannot be empty'
    assert os.path.exists(os.path.join(root_dir, DATASETS_DIR, args.dataset_name)), \
        f'directory dataset_name does not exist, dataset_name={os.path.join(root_dir, DATASETS_DIR, args.dataset_name)}'

    if args.model_path:
        assert args.model_path.endswith('.pth'), f'model_path file type incorrect, model_path={args.model_path}'

        assert os.path.exists(os.path.join(root_dir, OUTPUT_PATH, args.model_path)),\
            f'model_path file type incorrect, model_path={args.model_path}'

        model_dir_path = os.path.join(root_dir,OUTPUT_PATH,*args.model_path.split('/')[0:-1])
        assert CONFIG_FILE_NAME in os.listdir(os.path.join(model_dir_path)),\
            f'model_path directory does not contain {os.path.join(model_dir_path)} file file'


def train(root_dir, model_path, dataset_name, language, run_name, datasets_dir=DATASETS_DIR):
    mode = 'continue' if model_path else 'new'

    dataset_config = BaseDatasetConfig(
        formatter="ljspeech", meta_file_train="metadata.csv", path=os.path.join(root_dir, datasets_dir, dataset_name))

    audio_config = VitsAudioConfig(
        sample_rate=22050, win_length=1024, hop_length=256, num_mels=80, mel_fmin=0, mel_fmax=None
    )

    print(f"Mode=={mode}\n")

    if mode == 'new':
        config = VitsConfig(
            audio=audio_config,
            run_name=run_name,
            batch_size=20,
            eval_batch_size=20,
            batch_group_size=4,
            # num_loader_workers=8,
            num_loader_workers=4,
            num_eval_loader_workers=4,
            run_eval=True,
            test_delay_epochs=-1,
            epochs=100000,
            save_step=10000,
            save_checkpoints=True,
            save_n_checkpoints=10,
            save_best_after=1000,
            # text_cleaner="english_cleaners",
            text_cleaner="multilingual_cleaners",
            eval_split_size=0.1,
            use_phonemes=True,
            phoneme_language=language,
            phoneme_cache_path=os.path.join(root_dir, OUTPUT_PATH, "phoneme_cache"),
            compute_input_seq_cache=True,
            print_step=10,
            print_eval=True,
            mixed_precision=True,
            output_path=os.path.join(root_dir, OUTPUT_PATH),
            datasets=[dataset_config],
            cudnn_benchmark=False,
        )
    else:
        model_dir = model_path[:model_path.rfind("/")]
        config = load_config(os.path.join(root_dir, OUTPUT_PATH, model_dir, CONFIG_FILE_NAME))
        config.run_name = run_name
        old_root_dir = root_dir
        if root_dir == "":
            root_dir = os.getcwd()
        config.output_path = os.path.join(root_dir , OUTPUT_PATH)
        config.phoneme_cache_path = os.path.join(root_dir , OUTPUT_PATH, 'phoneme_cache')
        config.datasets[0]["path"] = os.path.join(root_dir , DATASETS_DIR, dataset_name)
        config.restore_path = os.path.join(root_dir, model_path)
        root_dir = old_root_dir

    try:
     with open(os.path.join(root_dir,TEST_SENTENCES_FILE), "r", encoding="utf-8") as json_file:
        test_sentences = json.load(json_file)
        config.test_sentences = test_sentences[language]
    except FileNotFoundError:
        print(f"Error: JSON file {TEST_SENTENCES_FILE} not found.")   
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {TEST_SENTENCES_FILE}.")    
    except Exception as e:
        print(f"Error: {e}")


    #print(config)
    # INITIALIZE THE AUDIO PROCESSOR
    # Audio processor is used for feature extraction and audio I/O.
    # It mainly serves to the dataloader and the training loggers.
    ap = AudioProcessor.init_from_config(config)

    # INITIALIZE THE TOKENIZER
    # Tokenizer is used to convert text to sequences of token IDs.
    # config is updated with the default characters if not defined in the config.
    tokenizer, config = TTSTokenizer.init_from_config(config)

    # LOAD DATA SAMPLES
    # Each sample is a list of [text, audio_file_path, speaker_name]
    # You can define your custom sample loader returning the list of samples.
    # Or define your custom formatter and pass it to the load_tts_samples.
    # Check TTS.tts.datasets.load_tts_samples for more details.
    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )

    model = Vits(config, ap, tokenizer, speaker_manager=None)
    if mode == 'continue':
        model.load_checkpoint(config, os.path.join(root_dir, OUTPUT_PATH, model_path))

    # init the trainer and begin
    trainer = Trainer(
        TrainerArgs(),
        config,
        os.path.join(root_dir, OUTPUT_PATH),
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )
    trainer.fit()


if __name__=='__main__':

    parser = argparse.ArgumentParser(prog='Train',
                                     description='Trains model from scratch or continues training of given model')
    parser.add_argument('-m', '--model_path', action='store', dest='model_path', default=None,
                        help='Model path (from output/), starts from scratch if not given.'
                             ' There must be config.json next to model!')
    parser.add_argument('-n', '--run_name', action='store', dest='run_name', default=DEFAULT_RUN_NAME,
                        help=f'Run name. Default {DEFAULT_RUN_NAME}')
    parser.add_argument('-l', '--language', action='store', dest='language', default='en',
                        help='Language of model (en/pl). Default: en.')
    parser.add_argument('-d', '--dataset', action='store', dest='dataset_name', default='dataset',
                        help=f'Dataset name (from {DATASETS_DIR}). Default: dataset.')
    parser.add_argument('-g', '--gpu', action='store', dest='gpu_num', required=True, help='GPU number.')

    args = parser.parse_args()
    validate_input(ROOT_DIR, args)

    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_num

    train(ROOT_DIR, args.model_path, args.dataset_name, args.language, args.run_name)
