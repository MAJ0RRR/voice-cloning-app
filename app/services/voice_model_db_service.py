import sqlite3
import os

from app.entities.voice_model import VoiceModel
from app.settings import VOICE_DIR, MODEL_DIR


class VoiceModelDbService:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        if self.select_all_voice_models() == []:
            self.initialize()

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS voice_models (id INTEGER PRIMARY KEY," \
                f"name TEXT NOT NULL UNIQUE," \
                f"path_model TEXT NOT NULL UNIQUE," \
                f"gender TEXT NOT NULL, " \
                f"language TEXT NOT NULL," \
                f"path_config TEXT NOT NULL)"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, voice_model):
        query = """
                   INSERT INTO voice_models (id, name, path_model, path_config, gender, language) 
                   VALUES (?, ?, ?,?, ?, ?)
               """
        values = (voice_model.id, voice_model.name, voice_model.path_model, voice_model.path_config, voice_model.gender, voice_model.language)
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.lastrowid

    def select_gender_language(self, gender, language):
        query = "SELECT v.id, v.name, v.path_model, v.path_config, v.gender, v.language " \
                "FROM voice_models AS v " \
                "WHERE v.gender = ? and v.language = ?"
        self.cursor.execute(query, (gender, language))
        rows = self.cursor.fetchall()
        voice_models = []
        for row in rows:
            voice_model = {"id": row[0], "name": row[1], "path_model": row[2],'path_config':row[3], "gender": row[4], "language": row[5]}
            voice_models.append(voice_model)
        return voice_models

    def select_all_voice_models(self):
        query = "SELECT v.id, v.name, v.path_model, v.path_config, v.gender, v.language " \
                "FROM voice_models AS v"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def initialize(self):
        path_model1 = os.path.join(MODEL_DIR, 'woman_1/checkpoint_672000.pth')
        path_config1 = os.path.join(MODEL_DIR, 'woman_1/config.json')
        path_model2 = os.path.join(MODEL_DIR, 'woman_2/checkpoint_50000.pth')
        path_config2 = os.path.join(MODEL_DIR, 'woman_2/config.json')
        self.insert(VoiceModel('test1', path_model1, path_config1, 'woman', 'english'))
        self.insert(VoiceModel('test2', path_model2, path_config2,'woman', 'polish'))

    def close(self):
        self.conn.close()
