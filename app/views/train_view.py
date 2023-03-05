from app.views.basic_view import BasicView


class TrainView(BasicView):

    def __init__(self, root, voice_model_service, voice_recordings_service, gender, language, model_id,
                 generate_samples):
        super(TrainView, self).__init__(root, voice_model_service, voice_recordings_service)
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.generate_samples = generate_samples
