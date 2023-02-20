import sqlite3

class DbService:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, table_name, values):
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def select(self, table_name, columns, where=None):
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, set_columns, where=None):
        set_parts = [f"{column} = ?" for column in set_columns]
        query = f"UPDATE {table_name} SET {', '.join(set_parts)}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query, [value for value in set_columns.values()])
        self.conn.commit()

    def delete(self, table_name, where=None):
        query = f"DELETE FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()