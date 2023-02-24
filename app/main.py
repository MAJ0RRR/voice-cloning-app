import tkinter as tk

from app.views.main_view import MainView
from services.voice_model_db_service import VoiceModelDbService
from services.voice_recording_db_service import VoiceRecordingDbService
from settings import db_file

voice_model_db_service = VoiceModelDbService(db_file)
voice_records_db_service = VoiceRecordingDbService(db_file)
root = tk.Tk()
root.configure(bg='green')
root.geometry("1920x1080")
MainView(root, voice_model_db_service, voice_records_db_service)
root.mainloop()


