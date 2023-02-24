import tkinter as tk

from lazy_import import lazy_module
from app.components.listbox_with_button import ListBoxWithButton


choose_gender_language_module = lazy_module("app.views.choose_gender_language_view")
main_menu_module = lazy_module("app.views.main_view")
WIDTH = 1920
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
PAD_Y = 80


class ChooseVoiceModelView:

    def __init__(self, root, gender, language, voice_model_service, voice_records_service):
        self.root = root
        self.voice_model_service = voice_model_service
        self.voice_records_service = voice_records_service
        models = self.voice_model_service.select_gender_language(gender, language)

        self.listbox = ListBoxWithButton(self.root)
        for model in models:
            audio_records = voice_records_service.select_model_id(model['id'])
            for audio_record in audio_records:
                if audio_record['name'] == 'basic':
                    self.listbox.insert(tk.END, model['name'], audio_record['path'])
                    break

        b1 = tk.Button(self.root, text="Menu główne", command=self.switch_to_main_menu, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        b2 = tk.Button(self.root, text="Cofnij",width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.switch_to_choose_gender_language_view)
        b3 = tk.Button(self.root, text="Dalej",width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.switch_to_choose_audio_view)

        b1.pack(pady=PAD_Y)
        b2.pack(pady=PAD_Y)
        b3.pack(pady=PAD_Y)

    def switch_to_choose_gender_language_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        choose_gender_language_module.ChooseGenderLanguageView(self.root)

    def switch_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_menu_module.MainView(self.root, self.voice_model_service, self.voice_records_service)

    def switch_to_choose_audio_view(self):
        pass


