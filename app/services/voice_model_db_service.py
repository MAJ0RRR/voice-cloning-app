import sqlite3
import os

from app.entities.voice_model import VoiceModel
from app.settings import AUDIO_DIR, MODEL_DIR


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
                f"path TEXT NOT NULL UNIQUE," \
                f"gender TEXT NOT NULL, " \
                f"language TEXT NOT NULL)"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, voice_model):
        query = """
                   INSERT INTO voice_models (id, name, path, gender, language) 
                   VALUES (?, ?, ?, ?, ?)
               """
        values = (voice_model.id, voice_model.name, voice_model.path, voice_model.gender, voice_model.language)
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.lastrowid

    def select_gender_language(self, gender, language):
        query = "SELECT v.id, v.name, v.path, v.gender, v.language " \
                "FROM voice_models AS v " \
                "WHERE v.gender = ? and v.language = ?"
        self.cursor.execute(query, (gender, language))
        rows = self.cursor.fetchall()
        voice_models = []
        for row in rows:
            voice_model = {"id": row[0], "name": row[1], "path": row[2], "gender": row[3], "language": row[4]}
            voice_models.append(voice_model)
        return voice_models

    def select_all_voice_models(self):
        query = "SELECT v.id, v.name, v.path, v.gender, v.language " \
                "FROM voice_models AS v"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def initialize(self):
        path1 = os.path.join(MODEL_DIR, 'test1.txt')
        path2 = os.path.join(MODEL_DIR, 'test2.txt')
        path3 = os.path.join(MODEL_DIR, 'test3.txt')
        path4 = os.path.join(MODEL_DIR, 'test4.txt')
        path5 = os.path.join(MODEL_DIR, 'test5.txt')
        path6 = os.path.join(MODEL_DIR, 'test6.txt')
        path7 = os.path.join(MODEL_DIR, 'test7.txt')
        path8 = os.path.join(MODEL_DIR, 'test8.txt')
        path9 = os.path.join(MODEL_DIR, 'test9.txt')
        path10 = os.path.join(MODEL_DIR, 'test10.txt')
        path11 = os.path.join(MODEL_DIR, 'test11.txt')
        path12 = os.path.join(MODEL_DIR, 'test12.txt')
        self.insert(VoiceModel('test1', path1, 'man', 'polish'))
        self.insert(VoiceModel('test2', path2, 'man', 'polish'))
        self.insert(VoiceModel('test3', path3, 'man', 'polish'))
        self.insert(VoiceModel('test4', path4, 'man', 'polish'))
        self.insert(VoiceModel('test5', path5, 'man', 'polish'))
        self.insert(VoiceModel('test6', path6, 'man', 'polish'))
        self.insert(VoiceModel('test7', path7, 'man', 'polish'))
        self.insert(VoiceModel('test8', path8, 'man', 'polish'))
        self.insert(VoiceModel('test9', path9, 'man', 'polish'))
        self.insert(VoiceModel('test10', path10, 'man', 'polish'))
        self.insert(VoiceModel('test11', path11, 'man', 'polish'))
        self.insert(VoiceModel('test12', path12, 'man', 'polish'))

    def close(self):
        self.conn.close()
