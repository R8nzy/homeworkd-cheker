import sqlite3

class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.create()

    def create(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('CREATE TABLE IF NOT EXISTS homework ('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                         'subject TEXT, task TEXT)')
        conn.close()

    def add_homework(self, subject, task):
        conn = sqlite3.connect(self.database)
        with conn:
            # Если по этому предмету уже есть ДЗ, заменяем его.
            conn.execute('DELETE FROM homework WHERE subject = ?', (subject,))
            conn.execute(
                'INSERT INTO homework (subject, task) VALUES (?, ?)',
                (subject, task)
            )
        conn.close()

    def get_homework(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT subject, task FROM homework ORDER BY id')
            homework = cursor.fetchall()
        conn.close()
        return homework

    def clear_homework(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('DELETE FROM homework')
        conn.close()
