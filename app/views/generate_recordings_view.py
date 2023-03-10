import tkinter as tk

from app.views.basic.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT


class GenerateRecordingsView(BasicView):

    def __init__(self, root, gender, language, voice_model_service, voice_records_service, version_service, model_id,
                 option):
        super(GenerateRecordingsView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.option = option
        self.gender = gender
        self.language = language
        self.model_id = model_id
        # label over input
        # input
        # button to generate
        # label for created
        # button to play
        # button to delete
        # button to come back to main menu
        # button to come back to list with models
        # button to come back to all generated recordings
