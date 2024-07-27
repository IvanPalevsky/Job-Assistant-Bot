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

#Введите новые рекомендации и запустите этот файл, чтобы добавить их в бд.
initial_recommendations = {
"Программирование": "💻 Начните с Python! Это как конструктор LEGO для кода - простой, но мощный. Идеально для новичков!",
"Маркетинг": "📣 Маркетинг - это как готовить вкусный суп. Нужны правильные ингредиенты (4P: Product, Price, Place, Promotion) и щепотка креативности!",
"B2B продажи": "🤝 B2B продажи - это как быть детективом в мире бизнеса. Ищите проблемы компаний и предлагайте решения!",
"Дизайн": "🎨 Дизайн - это как раскрашивать мир. Начните с основ графического дизайна, UX/UI или промышленного дизайна.",
"Финансы": "💰 Финансы - это как игра в шахматы с деньгами. Изучите правила игры: бухучет, анализ и инвестиции.",
"Управление проектами": "🚀 Управление проектами - это как дирижировать оркестром. Познакомьтесь с Agile и Scrum - это ваши дирижерские палочки!",
"Data Science": "🔬 Data Science - это как быть детективом в мире чисел. Начните с Python или R, добавьте статистику и щепотку машинного обучения.",
"Кибербезопасность": "🛡️ Кибербезопасность - это как быть супергероем в цифровом мире. Защищайте данные от злодеев!",
"Искусственный интеллект": "🤖 ИИ - это как учить компьютер думать. Начните с машинного обучения и нейронных сетей.",
"Веб-разработка": "🌐 Веб-разработка - это как строить digital-дома. HTML - фундамент, CSS - дизайн, JavaScript - все крутые фишки!",
"Мобильная разработка": "📱 Мобильная разработка - это как создавать волшебные палочки для смартфонов. Выберите iOS или Android и творите чудеса!",
"Предпринимательство": "🚀 Предпринимательство - это как выращивать деревья. Посадите идею, поливайте упорством, и однажды она принесет плоды!",
"Блокчейн": "⛓️ Блокчейн - это как цифровой сейф с множеством ключей. Изучите криптографию и распределенные системы.",
"UX/UI дизайн": "🖼️ UX/UI дизайн - это как быть архитектором цифровых пространств. Создавайте красивые и удобные интерфейсы!"
}

db_manager = DBManager(DATABASE)

#for category, content in initial_recommendations.items():
#    db_manager.add_recommendation(category, content)