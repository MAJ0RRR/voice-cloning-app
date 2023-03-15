from lazy_import import lazy_module
import threading

from app.views.train_view import TrainView
from app.views.basic.generate_samples_basic_view import GenerateSamplesBasicView
choose_audio_for_training_module = lazy_module('app.views.choose_audio_for_training')


class GenerateSamplesView(GenerateSamplesBasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service, gender, language, model_id):
        super(GenerateSamplesView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.gender = gender
        self.language = language
        self.model_id = model_id

    def switch_to_next_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        TrainView(self.root, self.voice_model_service, self.voice_recordings_service, self.version_service, self.gender,
                  self.language,
                  self.model_id)

    def switch_to_previous_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_audio_for_training_module.ChooseAudioForTrainingView(self.root, self.voice_model_service,
                                                                    self.voice_recordings_service, self.version_service,
                                                                    self.gender, self.language,
                                                                    self.model_id)

    def start_generate_samples(self):
        thread = threading.Thread(target=self.generate_samples, args=(self.finished_generating, self.stop_event))
        thread.start()

    def finished_generating(self):
        self.root.after(0, self.after_generating())

    def after_generating(self):
        if self.stop:
            self.switch_to_previous_view()
        else:
            self.switch_to_next_view()
