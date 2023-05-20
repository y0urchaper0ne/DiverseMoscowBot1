import time
import sqlite3
import warnings

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters
from quizz import bolshoi_history_question, bolshoi_building_question
from location import check_location_mxat, location
from text import bolshoi_history_text, bolshoi_building_text, bolshoi_history2_text, rules

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

# Подключение к базе данных SQLite
conn = sqlite3.connect('scores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
             (user_id INTEGER PRIMARY KEY, history_score FLOAT, building_score FLOAT)''')

# Функция для получения значения history_score по user_id
def get_history_score(user_id):
    c.execute("SELECT history_score FROM scores WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]  # Возвращаем значение history_score
    else:
        return None  # Если нет записи с таким user_id, возвращаем None


def get_building_score(user_id):
    c.execute("SELECT building_score FROM scores WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None  


main_menu_closed = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Перейти дальше 🔒']], resize_keyboard=True)
main_menu_open = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Перейти дальше 🔑']], resize_keyboard=True)


def wake_up(update, context):
    """Функция, запускающая бота"""
    user_id = update.effective_chat.id

    # Проверяем, есть ли у пользователя запись в базе данных, если нет, то создаем ее со значением 0
    c.execute("INSERT OR IGNORE INTO scores (user_id, history_score, building_score) VALUES (?, 0, 0)", (user_id,))
    conn.commit()   

    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Правила 📚'], ['Начать путешествие 🎭']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Давай начнем путешествие по театрам! \nВыбери, про что хочешь узнать сначала 👇'.format(name),
        reply_markup=button
    )
    return 'INTRO'

def intro(update, context):
    if str(update.message.text) == 'Начать путешествие 🎭':
        update.message.reply_text(text='Вперед!', reply_markup=main_menu_closed)
        return 'MAIN_MENU'
    elif str(update.message.text) == 'Правила 📚':
        update.message.reply_text(text=rules)

unit_menu_quizz = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
unit_menu_wo_quizz = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)

def score(user_id):
    if get_building_score(user_id) == 1.0:
        building_score='Загадка на местности: ✅'
    else: building_score='Загадка на местности: ❌'
    if get_history_score(user_id) == 1.0:
        history_score='Загадка на историю: ✅'
    else: history_score='Загадка на историю: ❌' 
    return f'{history_score} \n{building_score}'  


def main_menu(update, context):
    """Главное меню уровня"""
    user_id = update.effective_chat.id

    if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
        main_menu = main_menu_open
    else: 
        main_menu = main_menu_closed

    if str(update.message.text) == 'История 📜':
        if get_history_score(user_id) < 1.0:
            history_menu = unit_menu_quizz
        else: 
            history_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        time.sleep(1)
        update.message.reply_text(text=f'{bolshoi_history_text}')
        time.sleep(3)
        update.message.reply_text(
            text=f'{bolshoi_history2_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Читать больше', url="https://bolshoi.ru/")]]),
            parse_mode='HTML')
        return 'BOLSHOI_HISTORY'

    elif str(update.message.text) == 'Здание 🏛️':
        if get_building_score(user_id) < 1.0:
            building_menu = unit_menu_quizz
        else:
            building_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{bolshoi_building_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Читать больше', url="https://bolshoi.ru/")]]),
            parse_mode='HTML')
        update.message.reply_photo(
            photo='https://oknadom.ru/wp-content/uploads/2020/12/p_1.jpg')
        return 'BOLSHOI_BUILDING'
        
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 1.0 or get_history_score(user_id) < 1.0:
            user_score = score(user_id)
            update.message.reply_text(text=f'Ты решил не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            update.message.reply_text(text='Отлично! Идем дальше', reply_markup=forward_menu)
            return 'LEVEL_END'

    # elif str(update.message.text) == 'Узнать счет':
    #     if get_building_score(user_id) == 1.0:
    #         building_score='Загадка на местности: ✅'
    #     else: building_score='Загадка на местности: ❌'
    #     if get_history_score(user_id) == 1.0:
    #         history_score='Загадка на историю: ✅'
    #     else: history_score='Загадка на историю: ❌'   
    #     update.message.reply_text(text=f'Давай посмотрим, сколько загадок ты решил! \n\n{history_score} \n{building_score}', 
    #                               reply_markup=main_menu)

    else: update.message.reply_text(text=f'Прости, я тебя не понял 🥺')


quizz_menu = [[
                  InlineKeyboardButton("Подсказка", callback_data='hint'),
                  InlineKeyboardButton("Показать ответ", callback_data='answer')]]


def bolshoi_history(update, context):
    """Блок истории Большого театра"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_history_score(user_id) < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_text(
            text=f"Это загадка на знание истории большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        return 'HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'
    else: update.message.reply_text(text=f'Прости, я тебя не понял 🥺')


def bolshoi_building(update, context):
    """Блок здания Большого театра"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_building_score(user_id) < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_text(
            text=f"Это загадка на местности большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        return 'BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'
    else: update.message.reply_text(text=f'Прости, я тебя не понял 🥺')


def bolshoi_history_quizz(update, context):
    """Вопрос по истории Большого театра"""
    user_id = update.effective_chat.id

    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'
    response = bolshoi_history_question(text)
    if response == 'Молодец! Это правильный ответ 🏅':
        c.execute("UPDATE scores SET history_score = history_score + 1.0 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.execute("SELECT history_score FROM scores WHERE user_id = ?", (user_id,))
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'BOLSHOI_HISTORY'
    update.message.reply_text(response)


def history_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f"Это загадка на знание истории большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Подсказка по истории Большого театра', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f"Это загадка на знание истории большого театра? \nПиши ответ внизу 👇")
        query.message.reply_text(
            text=f'<tg-spoiler>Ответ на загадку по истории Большого театрау</tg-spoiler>', parse_mode='HTML')


def bolshoi_building_quizz(update, context):
    """Вопрос про здание Большого театра"""
    user_id = update.effective_chat.id
    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'
    response = bolshoi_building_question(text)
    if response == 'Молодец! Это правильный ответ 🏅':
        c.execute("UPDATE scores SET building_score = building_score + 1.0 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.execute("SELECT building_score FROM scores WHERE user_id = ?", (user_id,))
        update.message.reply_text(response, reply_markup=unit_menu_wo_quizz)
        return 'BOLSHOI_BUILDING'
    update.message.reply_text(response)


def building_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f"Это загадка на местности большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Подсказка по зданию Большого театра', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f"Это загадка на местности большого театра? \nПиши ответ внизу 👇")
        query.message.reply_text(
            text=f'<tg-spoiler>Ответ на загадку на местности Большого театрау</tg-spoiler>', parse_mode='HTML')


# Функция для обработки геолокации
def location_callback(update: Update, context: CallbackContext) -> None:
    # Вызываем функцию проверки местоположения пользователя
    check_location_mxat(update, context)
    # Снимаем регистрацию обработчика геолокации
    return ConversationHandler.END


def level_end(update, context):
    """Обработчик меню с подсказкой"""
    reply_markup = InlineKeyboardMarkup(quizz_menu)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_text(
            text=f'Молодец, ты перешел на второй уровень! \n\nСледующая остановка в нашем '
                f'маршруте – театр, неподалеку отсюда. Вот, кстати, его символ 👇')
        update.message.reply_photo(
            photo='https://www.culture.ru/s/vopros/chayka-mhat/images/tild3462-6532-4261-a536-616335303237__2.png')
        time.sleep(3)
        update.message.reply_text(
            text=f'Догадался, о каком театре идет речь? 🤔 \nОтправь его геопозицию сообщением!',
            reply_markup=reply_markup)
        location_callback(Update, CallbackContext)
        check_location_mxat(Update, CallbackContext)
        return "LOCATION"
    else: update.message.reply_text(text=f'Прости, я тебя не понял 🥺')

def location_quizz_menu_callback(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f'Догадался, о каком театре идет речь? 🤔 \nОтправь его геопозицию сообщением!',
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Подсказка по локации МХТ', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f'Догадался, о каком театре идет речь? 🤔 \nОтправь его геопозицию сообщением!')
        query.message.reply_text(
            text=f'<tg-spoiler>Ответ: МХТ им. Чехова</tg-spoiler>', parse_mode='HTML')

def cancel(update, context):
    user_id = update.effective_chat.id
    c.execute('''DELETE FROM scores
                 WHERE user_id = ?''', (user_id,))
    update.message.reply_text(text='До встречи!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    """Создаем и запускаем бота"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', wake_up)],
        states={
            'INTRO': [MessageHandler(Filters.regex('^(Правила 📚|Начать путешествие 🎭)$'), intro)],
            'MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, main_menu)],
            'BOLSHOI_HISTORY': [MessageHandler(Filters.text & ~Filters.command, bolshoi_history)],
            'BOLSHOI_BUILDING': [MessageHandler(Filters.text & ~Filters.command, bolshoi_building)],
            'HISTORY_QUIZZ': [
                        CallbackQueryHandler(history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, bolshoi_history_quizz)],
            'BUILDING_QUIZZ': [
                        CallbackQueryHandler(building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, bolshoi_building_quizz)],
            'LEVEL_END': [
                        CallbackQueryHandler(location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, level_end),]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_chat=True,
        # per_message=True,
    )

    location_handler = MessageHandler(Filters.location, location)
    dispatcher.add_handler(ConversationHandler(
        entry_points=[location_handler],
        states={"LOCATION": [location_handler]},
        fallbacks=[]
    ))

    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    main()

if __name__ == '__main__':
    main()
