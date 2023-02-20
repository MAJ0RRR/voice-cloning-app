import sqlite3


class VoiceModelDbService:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS voice_models (id INTEGER PRIMARY KEY," \
                f"name TEXT NOT NULL UNIQUE," \
                f"path TEXT NOT NULL UNIQUE," \
                f"gender TEXT NOT NULL," \
                f"langeauge TEXT NOT NULL)"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, voice_model):
        query = """
                   INSERT INTO voice_models (id, name, path, gender, language) 
                   VALUES (?, ?, ?, ?, ?)
               """
        values = (voice_model.voice_id, voice_model.name, voice_model.path, voice_model.gender, voice_model.language)
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.lastrowid

    def select_gender_language(self, gender, language):
        query = "SELECT v.id, v.name, v.path, v.gender, v.language" \
                "FROM voice_models AS v" \
                "WHERE v.gender = ? and v.language = ?"
        self.cursor.execute(query, (gender, language))
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.conn.close()