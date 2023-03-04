from app.views.generate_samples_basic_view import GenerateSamplesBasicView


class GenerateSamplesView(GenerateSamplesBasicView):

    def __init__(self, root, voice_model_service, voice_records_service):
        super(GenerateSamplesBasicView, self).__init__(root, voice_model_service, voice_records_service)
                