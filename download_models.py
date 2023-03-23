import json
import gdown
import os

def _create_subdir(directory, subdir):
	path = os.path.join(directory, subdir)
	if not os.path.exists(path):
		os.mkdir(path)
	return path


def download_models(project_root):
	import gdown

	models_dir = "models"
	deafult_dir = "default"
	default_models_file = "default_models.json"
	models_dir_path = _create_subdir(project_root, models_dir)
	default_models_dir_path = _create_subdir(models_dir_path, deafult_dir)

	with open(default_models_file, 'r') as file:
		config = json.load(file)

	for language in config.keys():
		language_path = _create_subdir(default_models_dir_path, language)

		for speaker, model_url in config[language].items():
			speaker_path = _create_subdir(language_path, speaker)
			gdown.download_folder(model_url, output=speaker_path)


if __name__ == '__main__':
	download_models(os.getcwd())