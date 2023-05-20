import time
import sqlite3
import warnings

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters
from quizz import bolshoi_history_question, bolshoi_building_question
from location import check_location_mxat, location
from text import (bolshoi_history_text, bolshoi_building_text, 
                  bolshoi_history_url, bolshoi_building_url,
                  rules, rules_url, louis_1,
                  louis_2, louis_3, louis_4, louis_5, louis_6)

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

# Подключение к базе данных SQLite
conn = sqlite3.connect('scores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
             (user_id INTEGER PRIMARY KEY, history_score FLOAT, building_score FLOAT)''')

def get_history_score(user_id):
    c.execute("SELECT history_score FROM scores WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None


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
    button = ReplyKeyboardMarkup([['Прочитать правила 📝'], ['Начать путешествие 🎭']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}! Давайте начнем наше театральное приключение, стартовая точка которого — Большой театр. Вы можете сначала прочитать правила или же сразу приступить к квесту. Выберите, что хочешь 👇'.format(name),
        reply_markup=button
    )
    return 'INTRO'

def intro(update, context):
    if str(update.message.text) == 'Начать путешествие 🎭':
        button = ReplyKeyboardMarkup([['Да, интересуюсь']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text='Bonjour!')
        time.sleep(2)
        update.message.reply_text(text=louis_1, reply_markup=button)
        return 'INTRO_2'
    elif str(update.message.text) == 'Прочитать правила 📝':
        update.message.reply_text(
            text=rules,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Инструкция по прохождению', url=rules_url)]]))

def intro_two(update, context):
    if str(update.message.text) == 'Да, интересуюсь':
        button = ReplyKeyboardMarkup([['Эээ… Oui?']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=louis_2)
        time.sleep(3)
        update.message.reply_text(text=louis_3)
        time.sleep(3)
        update.message.reply_text(text='Не могли бы вы мне помочь?', reply_markup=button)
        return 'INTRO_3'

def intro_three(update, context):
    if str(update.message.text) == 'Эээ… Oui?':
        button = ReplyKeyboardMarkup([['По рукам!']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=louis_4)
        time.sleep(3)
        update.message.reply_text(text=louis_5, reply_markup=button)
        return 'INTRO_4'

def intro_four(update, context):
    if str(update.message.text) == 'По рукам!':
        update.message.reply_text(text=louis_6)
        time.sleep(3)
        update.message.reply_text(text='Про что хотите узнать: историю театра или здание?', reply_markup=main_menu_closed)
        return 'MAIN_MENU'

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

    if str(update.message.text) == 'История 📜':
        if get_history_score(user_id) < 1.0:
            history_menu = unit_menu_quizz
        else: 
            history_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        time.sleep(1)
        update.message.reply_text(
            text=f'{bolshoi_history_text}', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='История Большого театра', url=bolshoi_history_url)]]),
            )
        return 'BOLSHOI_HISTORY'

    elif str(update.message.text) == 'Здание 🏛️':
        if get_building_score(user_id) < 1.0:
            building_menu = unit_menu_quizz
        else:
            building_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{bolshoi_building_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Здание Большого театра', url=bolshoi_building_url)]]),
            )
        return 'BOLSHOI_BUILDING'
        
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 1.0 or get_history_score(user_id) < 1.0:
            user_score = score(user_id)
            update.message.reply_text(text=f'Ты решил не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            update.message.reply_text(
                text='Большому театру — большая история. Поздравляю, вы перешли на второй уровень! И нам нужно двигаться дальше.', 
                reply_markup=forward_menu)
            return 'LEVEL_END'

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
            text=f"Не подскажете, под каким названием театр прослужил меньше всего? \n\nПиши ответ внизу 👇",
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
            text=f"Интересно, какое максимальное число можно увидеть на табличке с номером подъезда театра? Пишите ответ внизу 👇",
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
    if response == 'Merci! Все так 🥳':
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
            text=f"Не подскажете, под каким названием театр прослужил меньше всего? \n\nПишите ответ внизу 👇",
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Это название дали после первого пожара в 1805 году', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f"Не подскажете, под каким названием театр прослужил меньше всего? \n\nПишите ответ внизу 👇")
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Большой Петровский театр</tg-spoiler>', parse_mode='HTML')


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
    if response == 'Bravo! Из вас хороший математик 🥳':
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
            text=f"Интересно, какое максимальное число можно увидеть на табличке с номером подъезда театра? Пишите ответ внизу 👇",
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Обойдите театр по периметру и обратите внимание на западную сторону здания', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f"Интересно, какое максимальное число можно увидеть на табличке с номером подъезда театра? Пишите ответ внизу 👇")
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>22</tg-spoiler>', parse_mode='HTML')


def location_callback(update: Update, context: CallbackContext) -> None:
    """Обработчик геолокации"""
    check_location_mxat(update, context)


def level_end(update, context):
    """Обработчик перехода на новый уровень"""
    reply_markup = InlineKeyboardMarkup(quizz_menu)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_text(
            text=f'Следующая остановка в нашем маршруте – театр, неподалеку отсюда. Вот, кстати, его символ 👇')
        update.message.reply_photo(
            photo='https://www.culture.ru/s/vopros/chayka-mhat/images/tild3462-6532-4261-a536-616335303237__2.png')
        time.sleep(3)
        update.message.reply_text(
            text=f'Догадался, о каком театре идет речь? 🤔 \nОтправь его геопозицию сообщением!',
            reply_markup=reply_markup)
        return "LOCATION"
    else: update.message.reply_text(text=f'Прости, я тебя не понял 🥺')

def location_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой локации"""
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
    """Завершение бота"""
    user_id = update.effective_chat.id
    c.execute('''DELETE FROM scores
                 WHERE user_id = ?''', (user_id,))
    update.message.reply_text(text='До встречи!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    """Создаем и запускаем бот"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', wake_up)],
        states={
            'INTRO': [MessageHandler(Filters.regex('^(Прочитать правила 📝|Начать путешествие 🎭)$'), intro)],
            'INTRO_2': [MessageHandler(Filters.text & ~Filters.command, intro_two)],
            'INTRO_3': [MessageHandler(Filters.text & ~Filters.command, intro_three)],
            'INTRO_4': [MessageHandler(Filters.text & ~Filters.command, intro_four)],
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
                        MessageHandler(Filters.text & ~Filters.command, level_end)],
            'LOCATION': [MessageHandler(Filters.location & ~Filters.command, location_callback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_chat=True,
        # per_message=True,
    )

    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    main()

if __name__ == '__main__':
    main()