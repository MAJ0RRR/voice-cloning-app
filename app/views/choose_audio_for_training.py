from lazy_import import lazy_module
import tkinter as tk

from app.views.basic.basic_choose_audio_file import BasicChooseAudioFile
from app.views.basic.basic_view import BUTTON_WIDTH_1, BUTTON_HEIGHT_1, BUTTON_FONT, Y_MENU
from app.views.train_view import TrainView

choose_voice_model_view = lazy_module("app.views.choose_voice_model_view")


class ChooseAudioForTrainingView(BasicChooseAudioFile):

    def __init__(self, root, voice_model_service, voice_records_service, version_service, gender, language, model_id):
        super(ChooseAudioForTrainingView, self).__init__(root, voice_model_service, voice_records_service,
                                                         version_service)
        self.gender = gender
        self.language = language
        self.model_id = model_id
        self.generate_samples = tk.BooleanVar()

    def display_widgets(self):
        main_menu_button = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        back_button = tk.Button(self.root, text="Wybierz ponownie model głosu", width=BUTTON_WIDTH_1,
                                height=BUTTON_HEIGHT_1,
                                command=self.switch_to_choose_gender_language_train, font=BUTTON_FONT)
        continue_button = tk.Button(self.root, text="Trenuj model", width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        main_menu_button.place(x=250, y=Y_MENU)
        back_button.place(x=750, y=Y_MENU)
        continue_button.place(x=1250, y=Y_MENU)
        checkbox = tk.Checkbutton(self.root, text="Wygeneruj próbki", activebackground='green', highlightthickness=0,
                                  highlightcolor='green',
                                  bg='green', font=BUTTON_FONT, variable=self.generate_samples, width=BUTTON_WIDTH_1,
                                  height=BUTTON_HEIGHT_1)
        checkbox.place(x=1250, y=Y_MENU + 100)

    def switch_to_choose_model(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_voice_model_view.ChooseVoiceModelView(self.root, self.gender, self.language, self.voice_model_service,
                                                     self.voice_recordings_service, self.version_service)

    def switch_to_training_view(self):
        generate_samples = self.generate_samples.get()
        for widget in self.root.winfo_children():
            widget.destroy()
        if generate_samples:
            pass
        TrainView(self.root, self.voice_model_service, self.voice_recordings_service, self.version_service, self.gender,
                  self.language,
                  self.model_id)
