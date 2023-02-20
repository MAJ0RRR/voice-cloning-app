import sqlite3


class VoiceRecordingDbService:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS voice_recordings (id INTEGER PRIMARY KEY," \
                f"name TEXT NOT NULL UNIQUE," \
                f"path TEXT NOT NULL UNIQUE," \
                "model_id INTEGER NOT NULL," \
                "FOREIGN KEY(user_id)  REFERENCES voice_models(id));"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, voice_recording):
        query = """
                   INSERT INTO voice_recorings (id, name, path, model_id) 
                   VALUES (?, ?, ?, ?)
               """
        values = (voice_recording.id, voice_recording.name, voice_recording.path, voice_recording.model_id)
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.lastrowid

    def select_user_id(self, user_id):
        query = "SELECT v.id, v.name, v.path, v.gender, v.language" \
                "FROM voice_recordings AS v" \
                "WHERE v.user_id = ?"
        self.cursor.execute(query, (user_id))
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.conn.close()