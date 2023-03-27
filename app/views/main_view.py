import tkinter as tk

from app.views.basic.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT


class MainView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service):
        super(MainView, self).__init__(root, voice_model_service, voice_records_service, version_service)
        self.display_widgets()

    def display_widgets(self):
        b1 = tk.Button(self.root, text="Stwórz nowy model głosu",
                       command=self.switch_to_choose_gender_language_train_old,
                       width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        b2 = tk.Button(self.root, text="Dotrenuj model głosu", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                       command=self.switch_to_choose_gender_language_train_new,
                       font=BUTTON_FONT)
        b3 = tk.Button(self.root, text="Syntezuj mowę na podstawie modelu", width=BUTTON_WIDTH_1,
                       height=BUTTON_HEIGHT_1, font=BUTTON_FONT,
                       command=self.switch_to_choose_gender_language_synthesize)
        b4 = tk.Button(self.root, text="Wygeneruj próbki do uczenia", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                       command=self.switch_to_choose_language, font=BUTTON_FONT)

        b1.pack(pady=PAD_Y)
        b2.pack(pady=PAD_Y)
        b3.pack(pady=PAD_Y)
        b4.pack(pady=PAD_Y)
