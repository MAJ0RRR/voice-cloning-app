import sqlite3
import os

from app.settings import GENERATED_DIR
from app.entities.voice_recording import VoiceRecording


class VoiceRecordingDbService:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        if self.select_voice_recordings() == []:
            self.initialize()

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS voice_recordings (id INTEGER PRIMARY KEY," \
                f"name TEXT NOT NULL," \
                f"path TEXT NOT NULL UNIQUE," \
                "model_id INTEGER NOT NULL," \
                "FOREIGN KEY(model_id)  REFERENCES voice_models(id));"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, voice_recording):
        query = """
                   INSERT INTO voice_recordings (name, path, model_id) 
                   VALUES (?, ?, ?)
               """
        self.cursor.execute(query, (voice_recording.name, voice_recording.path, voice_recording.model_id))
        self.conn.commit()

        return self.cursor.lastrowid

    def select_voice_recordings(self, model_id=None, name=None):
        if model_id:
            if name:
                query = "SELECT v.id, v.name, v.path, v.model_id " \
                        "FROM voice_recordings AS v " \
                        "WHERE v.model_id = ? and v.name = ?"
                self.cursor.execute(query, (model_id, name))
            else:
                query = "SELECT v.id, v.name, v.path, v.model_id " \
                        "FROM voice_recordings AS v " \
                        "WHERE v.model_id = ?"
                self.cursor.execute(query, (model_id,))
        elif name:
            query = "SELECT v.id, v.name, v.path, v.model_id " \
                    "FROM voice_recordings AS v " \
                    "WHERE v.name = ?"
            self.cursor.execute(query, (name,))
        else:
            query = "SELECT v.id, v.name, v.path, v.model_id " \
                    "FROM voice_recordings AS v "
            self.cursor.execute(query)
        rows = self.cursor.fetchall()
        voice_records = []
        for row in rows:
            voice_record = {"id": row[0], "name": row[1], "path": row[2], "model_id": row[3]}
            voice_records.append(voice_record)
        return voice_records

    def initialize(self):
        path1 = os.path.join(GENERATED_DIR, 'test1.mp3')
        self.insert(VoiceRecording('basic', path1, 1))

    def close(self):
        self.conn.close()
