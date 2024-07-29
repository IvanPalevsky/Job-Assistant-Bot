import telebot
from telebot import types
from config import *
from tables import DBManager
import requests

bot = telebot.TeleBot(TOKEN)
db_manager = DBManager(DATABASE)

@bot.message_handler(commands=["start"])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {user_name}! Я твой помощник по выбору работы. Чем могу помочь?")
    bot.send_message(message.chat.id, "Вы можете использовать команду /feedback, чтобы оставить отзыв или предложение.")
    bot.send_message(message.chat.id, "Чтобы пройти квиз и узнать, какая профессия вам подходит, используйте команду /quiz.")
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
    jobs_button = types.InlineKeyboardButton("Найти вакансии", callback_data=f'jobs_{category}')
    markup.add(yes_button, no_button, jobs_button)
    bot.send_message(call.message.chat.id, "Хотите получить более подробную информацию или найти вакансии?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('more_'))
def provide_more_info(call):
    category = call.data.split('_', 1)[1]
    more_info = db_manager.get_more_info(category)
    bot.send_message(call.message.chat.id, more_info if more_info else "Извините, дополнительная информация не найдена.")
    show_categories(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'no_more')
def no_more_info(call):
    bot.answer_callback_query(call.id, "Хорошо, давайте вернемся к выбору категорий.")
    show_categories(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('jobs_'))
def search_jobs(call):
    category = call.data.split('_', 1)[1]
    bot.answer_callback_query(call.id, "Ищем вакансии...")
    jobs = get_jobs(category)
    if jobs:
        for job in jobs:
            bot.send_message(call.message.chat.id, f"{job['name']}\n{job['alternate_url']}")
    else:
        bot.send_message(call.message.chat.id, "Извините, не удалось найти вакансии.")
    show_categories(call.message.chat.id)

def get_jobs(category):
    url = f"https://api.hh.ru/vacancies?text={category}&per_page=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    return None

@bot.message_handler(commands=["feedback"])
def feedback(message):
    bot.reply_to(message, "Пожалуйста, напишите ваш отзыв или предложение в следующем сообщении.")
    bot.register_next_step_handler(message, process_feedback)

def process_feedback(message):
    user_id = message.from_user.id
    feedback_content = message.text
    db_manager.add_feedback(user_id, feedback_content)
    bot.reply_to(message, "Спасибо за ваш отзыв! Мы ценим ваше мнение.")

@bot.message_handler(commands=["quiz"])
def start_quiz(message):
    questions = db_manager.get_all_quiz_questions()
    bot.send_message(message.chat.id, "Давайте определим, какая профессия вам подходит! Ответьте на несколько вопросов.")
    ask_question(message, questions, 0, {})

def ask_question(message, questions, current_question, answers):
    if current_question < len(questions):
        question, option_a, option_b = questions[current_question]
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add(option_a, option_b)
        bot.send_message(message.chat.id, question, reply_markup=markup)
        bot.register_next_step_handler(message, process_answer, questions, current_question, answers)
    else:
        show_quiz_result(message, answers)

def process_answer(message, questions, current_question, answers):
    answers[current_question] = message.text
    ask_question(message, questions, current_question + 1, answers)

def show_quiz_result(message, answers):
    profession = determine_profession(answers)
    result = f"На основе ваших ответов, вам может подойти профессия в сфере {profession}."
    bot.send_message(message.chat.id, result, reply_markup=types.ReplyKeyboardRemove())
    show_categories(message.chat.id)

def determine_profession(answers):
    tech_score = 0
    creative_score = 0
    business_score = 0

    for answer in answers.values():
        if answer in ["С компьютерами", "Аналитическая", "Удаленно", "Оптимизировать существующее", "Индивидуально"]:
            tech_score += 1
        elif answer in ["С людьми", "Творческая", "В офисе", "Создавать новое", "В команде"]:
            creative_score += 1
        else:
            business_score += 1

    if tech_score >= creative_score and tech_score >= business_score:
        return "IT и программирования"
    elif creative_score >= tech_score and creative_score >= business_score:
        return "дизайна и креатива"
    else:
        return "бизнеса и менеджмента"

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

    bot.send_message(message.chat.id, "Извините, я не понял ваш запрос. Попробуйте выбрать категорию из списка или используйте команду /quiz для прохождения теста.")
    show_categories(message.chat.id)

if __name__ == '__main__':
    bot.infinity_polling()
