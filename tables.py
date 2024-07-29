import sqlite3
from config import *

class DBManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY,
                category TEXT,
                content TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS more_info (
                id INTEGER PRIMARY KEY,
                category TEXT,
                content TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                option_a TEXT,
                option_b TEXT
            )
        ''')
        self.conn.commit()

    def add_recommendation(self, category, content):
        self.cursor.execute('INSERT INTO recommendations (category, content) VALUES (?, ?)', (category, content))
        self.conn.commit()

    def get_recommendation(self, category):
        self.cursor.execute('SELECT content FROM recommendations WHERE category = ? ORDER BY RANDOM() LIMIT 1', (category,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_categories(self):
        self.cursor.execute('SELECT DISTINCT category FROM recommendations')
        return [row[0] for row in self.cursor.fetchall()]

    def add_feedback(self, user_id, content):
        self.cursor.execute('INSERT INTO feedback (user_id, content) VALUES (?, ?)', (user_id, content))
        self.conn.commit()

    def get_all_feedback(self):
        self.cursor.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
        return self.cursor.fetchall()

    def add_more_info(self, category, content):
        self.cursor.execute('INSERT INTO more_info (category, content) VALUES (?, ?)', (category, content))
        self.conn.commit()

    def get_more_info(self, category):
        self.cursor.execute('SELECT content FROM more_info WHERE category = ?', (category,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_quiz_question(self, question, option_a, option_b):
        self.cursor.execute('INSERT INTO quiz_questions (question, option_a, option_b) VALUES (?, ?, ?)', (question, option_a, option_b))
        self.conn.commit()

    def get_all_quiz_questions(self):
        self.cursor.execute('SELECT question, option_a, option_b FROM quiz_questions')
        return self.cursor.fetchall()

db_manager = DBManager(DATABASE)

quiz_questions = [
   # Здесь можно добавить код для заполнения таблицы quiz_questions 
]
for question, option_a, option_b in quiz_questions:
    db_manager.add_quiz_question(question, option_a, option_b)

initial_recommendations = {
    # Здесь можно добавить начальные рекомендации
}

more_info = {
    # Здесь можно добавить дополнительную информацию
}

for category, content in initial_recommendations.items():
    db_manager.add_recommendation(category, content)

for category, content in more_info.items():
    db_manager.add_more_info(category, content)
