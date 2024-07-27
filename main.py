import telebot
from telebot import types
from config import *
from tables import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {user_name}! Я твой помощник по выбору работы. Чем могу помочь?")
    show_categories(message.chat.id)

def show_categories(chat_id):
    categories = db_manager.get_all_categories()
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(category, callback_data=f'category_{category}') for category in categories]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите интересующую вас тему:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def callback_inline(call):
    category = call.data.split('_', 1)[1]
    recommendation = db_manager.get_recommendation(category)
    if recommendation:
        bot.answer_callback_query(call.id, "Вот ваша рекомендация:")
        bot.send_message(call.message.chat.id, recommendation)
    else:
        bot.answer_callback_query(call.id, "Извините, рекомендация не найдена.")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes_button = types.InlineKeyboardButton("Да", callback_data=f'more_{category}')
    no_button = types.InlineKeyboardButton("Нет", callback_data='no_more')
    markup.add(yes_button, no_button)
    bot.send_message(call.message.chat.id, "Хотите получить более подробную информацию?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('more_'))
def provide_more_info(call):
    category = call.data.split('_', 1)[1]
    more_info = {
"Программирование": "🐍 Python - ваш верный друг в мире кода:\n1. Codecademy - интерактивные уроки, как игра\n2. freeCodeCamp - бесплатные проекты, как конструктор\n3. Coursera - онлайн-университет в вашем компьютере\n4. LeetCode - тренажерный зал для мозга программиста\n5. GitHub - библиотека кода всего мира",
"Маркетинг": "🎯 Станьте гуру маркетинга:\n1. Google Digital Garage - бесплатная школа цифрового маркетинга\n2. HubSpot Academy - учебка по входящему маркетингу\n3. Coursera Marketing - университет маркетинга онлайн\n4. Neil Patel's blog - свежие идеи каждый день\n5. 'This Old Marketing' podcast - радио для маркетологов",
"B2B продажи": "💼 Прокачайте навыки B2B продаж:\n1. Sales Hacker - энциклопедия B2B продаж\n2. LinkedIn Sales Solutions blog - советы от профи\n3. HubSpot Sales blog - блог о продажах и работе с клиентами\n4. 'The Advanced Selling Podcast' - подкаст-тренер по продажам\n5. SPIN Selling (книга) - библия B2B продаж",
"Дизайн": "🎨 Раскрасьте свой путь в дизайне:\n1. Behance - музей современного дизайна\n2. Dribbble - Instagram для дизайнеров\n3. DesignCourse на YouTube - бесплатная школа дизайна\n4. Adobe Creative Cloud - швейцарский нож дизайнера\n5. 'Don't Make Me Think' by Steve Krug - книга о том, как делать вещи понятными",
"Финансы": "💰 Станьте финансовым волшебником:\n1. Investopedia - словарь финансового языка\n2. 'The Intelligent Investor' - книга от дедушки инвестиций\n3. Wall Street Journal - газета из мира денег\n4. edX Financial Analysis - университет финансов онлайн\n5. 'Rich Dad Poor Dad' - книга о том, как думать о деньгах",
"Управление проектами": "📊 Дирижируйте проектами как про:\n1. PMI - клуб супер-менеджеров\n2. Trello - доска для управления всем\n3. PMBOK Guide - библия управления проектами\n4. Scrum.org - учебник по Scrum\n5. 'The Phoenix Project' - приключения в мире IT-проектов",
"Data Science": "📊 Погрузитесь в океан данных:\n1. Kaggle - спортзал для data scientists\n2. DataCamp - интерактивные уроки по Data Science\n3. Towards Data Science на Medium - блог умных людей\n4. 'Python for Data Analysis' - книга о том, как приручить данные\n5. Fast.ai - бесплатный университет машинного обучения",
"Кибербезопасность": "🔐 Станьте цифровым защитником:\n1. Cybrary - бесплатные курсы по кибербезопасности\n2. HackTheBox - тренировочная площадка для хакеров\n3. OWASP - библиотека знаний о веб-безопасности\n4. 'The Web Application Hacker's Handbook' - настольная книга хакера\n5. DEF CON - крупнейшая конференция по безопасности",
"Искусственный интеллект": "🧠 Создайте свой ИИ:\n1. Coursera Machine Learning - курс от гуру ИИ\n2. TensorFlow - инструмент для создания ИИ от Google\n3. 'Artificial Intelligence: A Modern Approach' - библия ИИ\n4. OpenAI Gym - спортзал для ИИ\n5. AI Weekly - новостная рассылка о мире ИИ",
"Веб-разработка": "🌐 Постройте свой уголок интернета:\n1. MDN Web Docs - энциклопедия веб-разработки\n2. freeCodeCamp - бесплатный буткемп по веб-разработке\n3. CSS-Tricks - трюки и советы по CSS\n4. 'You Don't Know JS' - серия книг о JavaScript\n5. Can I use - проверка поддержки веб-технологий",
"Мобильная разработка": "📱 Создайте приложение мечты:\n1. Android Developers - официальный гид по Android\n2. iOS Dev Center - центр разработки для iOS\n3. Flutter - фреймворк для кросс-платформенной разработки\n4. Udacity Nanodegree - онлайн-курсы по мобильной разработке\n5. 'iOS Programming: The Big Nerd Ranch Guide' - книга для iOS разработчиков",
"Предпринимательство": "💡 Запустите свой бизнес:\n1. Y Combinator Startup School - бесплатная школа стартапов\n2. Lean Startup - методология запуска стартапов\n3. Indie Hackers - сообщество индивидуальных предпринимателей\n4. 'Zero to One' by Peter Thiel - книга о создании будущего\n5. Startup Podcast - истории успеха и неудач стартапов",
"Блокчейн": "🔗 Станьте мастером блокчейна:\n1. Coursera Blockchain Specialization - курс от экспертов\n2. Ethereum.org - официальный ресурс Ethereum\n3. 'Mastering Bitcoin' - книга о технологии биткойна\n4. CryptoZombies - интерактивная школа Solidity\n5. Blockchain at Berkeley - ресурсы от ведущего университета",
"UX/UI дизайн": "🖌️ Создавайте потрясающий пользовательский опыт:\n1. Interaction Design Foundation - онлайн-курсы по UX/UI\n2. Figma - популярный инструмент для дизайна\n3. 'The Design of Everyday Things' - классическая книга о дизайне\n4. UX Booth - блог о UX дизайне\n5. Dribbble - вдохновение и сообщество дизайнеров"
}
    bot.send_message(call.message.chat.id, more_info.get(category, "Извините, дополнительная информация не найдена."))
    show_categories(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'no_more')
def no_more_info(call):
    bot.answer_callback_query(call.id, "Хорошо, давайте вернемся к выбору категорий.")
    show_categories(call.message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_message = message.text.lower()
    categories = db_manager.get_all_categories()
    
    for category in categories:
        if category.lower() in user_message:
            recommendation = db_manager.get_recommendation(category)
            if recommendation:
                bot.send_message(message.chat.id, recommendation)
                return

    bot.send_message(message.chat.id, "Извините, я не понял ваш запрос. Попробуйте выбрать категорию из списка:")
    show_categories(message.chat.id)

if __name__ == '__main__':
    bot.infinity_polling()
