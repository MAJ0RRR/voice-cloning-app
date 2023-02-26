from lazy_import import lazy_module

choose_gender_view = lazy_module("app.views.choose_gender_language_view")
choose_audio_for_samples_view = lazy_module("app.views.choose_audio_for_generating_samples_view")
main_menu_module = lazy_module("app.views.main_view")

WIDTH = 1920
HEIGHT = 1080
PAD_Y = 80
BUTTON_WIDTH_1 = 30
BUTTON_HEIGHT_1 = 3
BUTTON_WIDTH_2 = 17
BUTTON_HEIGHT_2 = 1
MODELS_ON_PAGE = 10
Y_FIRST_MODEL = 150
Y_MENU = 800
BUTTON_FONT = ("Helvetica", 14)
ENABLED_EXTENSIONS = ('.mp3', '.mp4', '.wav')


class BasicView:

    def __init__(self, root, voice_model_service, voice_recordings_service):
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_recordings_service = voice_recordings_service

    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_gender_view.ChooseGenderLanguageView(self.root, self.voice_model_service, self.voice_recordings_service)

    def switch_to_generate_samples(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_audio_for_samples_view.ChooseAudioForGeneratingSamplesView(self.root, self.voice_model_service,
                                                                          self.voice_recordings_service)

    def switch_to_main_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_recordings_service)
