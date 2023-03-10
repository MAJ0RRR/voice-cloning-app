import threading

from app.views.finish_generating_samples_view import FinishGeneratingSamples
from app.views.basic.generate_samples_basic_view import GenerateSamplesBasicView


class GenerateSamplesView(GenerateSamplesBasicView):

    def __init__(self, root, voice_model_service, voice_records_service, version_service):
        super(GenerateSamplesView, self).__init__(root, voice_model_service, voice_records_service, version_service)

    def switch_to_next_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        FinishGeneratingSamples(self.root, self.voice_model_service, self.voice_recordings_service,
                                self.version_service)

    def switch_to_previous_view(self):
        self.switch_to_generate_samples()

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
