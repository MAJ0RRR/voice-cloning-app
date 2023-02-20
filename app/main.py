import tkinter as tk

from app.views.main_view import MainView
from services.voice_model_db_service import VoiceModelDbService
from services.voice_recording_db_service import VoiceRecordingDbService
from settings import db_file

VoiceModelDbService(db_file)
VoiceRecordingDbService(db_file)
root = tk.Tk()
root.configure(bg='green')
root.geometry("1920x1080")
MainView(root, db_file)
root.mainloop()


