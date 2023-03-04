import tkinter as tk
from tkinter import messagebox as mb
import subprocess
from time import sleep
from app.views.basic_view import BasicView, BUTTON_HEIGHT_1, BUTTON_WIDTH_1, PAD_Y, BUTTON_FONT


class GenerateSamplesBasicView(BasicView):

    def __init__(self, root, voice_model_service, voice_records_service):
        super(GenerateSamplesBasicView, self).__init__(root, voice_model_service, voice_records_service)
        label = tk.Label(self.root, font=BUTTON_FONT, text='Próbki są przygotowywane')
        label.pack()
        cancel_button = tk.Button(self.root, text='Anuluj', font=BUTTON_FONT, command=self.cancel)
        cancel_button.pack()
        self.processes = []
        self.generate_samples()

    def cancel(self):
        res = mb.askquestion('Przerwanie tworzenia próbek', 'Czy na pewno chcesz zakończyć tworzenie próbek')
        if res == 'yes':
            for process in self.processes:
                process.terminate()
            self.switch_to_previous_view()

    def switch_to_previous_view(self):
        print('zadzialalo')

    def generate_samples(self):
        process = subprocess.Popen(["sh", "../splits.sh"])
        process.wait()
        #self.processes.append(subprocess.Popen(["py", "noise.py"]))





