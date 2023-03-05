import tkinter as tk

from app.views.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT, MAX_FONT, HEIGHT


class FinishGeneratingSamples(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service):
        super(FinishGeneratingSamples, self).__init__(root, voice_model_service, voice_records_service)
        label1 = tk.Label(self.root, text="Generowanie próbek zakończone.", font=MAX_FONT, bg='green')
        label1.pack(pady=PAD_Y)
        label2 = tk.Label(self.root, text="Próbki znajdują się w folderze...", font=MAX_FONT, bg='green')
        label2.pack()
        b1 = tk.Button(self.root, text="Stwórz kolejne próbki", command=self.switch_to_generate_samples,
                       width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        b2 = tk.Button(self.root, text="Wróc do menu głównego", width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1,
                       command=self.switch_to_main_view,
                       font=BUTTON_FONT)

        b1.place(x=500, y=HEIGHT / 2 - 20)
        b2.place(x=1000, y=HEIGHT / 2 - 20)
