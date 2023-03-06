import sqlite3


class VersionService:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS versions (id INTEGER PRIMARY KEY, version INTEGER)''')
        self.cursor.execute('''SELECT COUNT(*) FROM versions''')
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.insert_version(0)
        self.conn.commit()

    def insert_version(self, version):
        self.cursor.execute('''INSERT INTO versions (version) VALUES (?)''', (version,))
        self.conn.commit()
        return True

    def get_version(self):
        self.cursor.execute('''SELECT version FROM versions''')
        rows = self.cursor.fetchall()
        return rows[0]

    def update_version(self, old_version, new_version):
        self.cursor.execute('''UPDATE versions SET version = ? WHERE vesion = ?''', (new_version, old_version))
        self.conn.commit()
        return True

    def __del__(self):
        self.conn.close()