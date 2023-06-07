import sqlite3
# import mysql.connector
# import pymysql
import psycopg2

import warnings

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.ext import (CallbackQueryHandler,
                          CommandHandler, ConversationHandler,
                          Filters, Updater, MessageHandler)

from levels.lvl_one import (intro, intro_two, intro_three, intro_four,
                     bolshoi_building, bolshoi_building_quizz, 
                     bolshoi_history, bolshoi_history_quizz,
                     bolshoi_main_menu, history_quizz_menu_callback,
                     building_quizz_menu_callback, level_one_end,
                     bolshoi_location_quizz_menu_callback,
                     level_choice, level_choice_menu, bolshoi_to_mxat,
                    )
from levels.lvl_two import (mxat_transition, mxat_main_menu, mxat_history,
                            mxat_building, mxat_location_quizz_menu_callback,
                            mxat_history_quizz, mxat_history_quizz_menu_callback,
                            mxat_building_quizz_menu_callback, level_two_end,
                            mxat_building_quizz,mxat_to_nations,
                            )
from levels.lvl_three import (nations_transition, nations_building,
                              nations_building_quizz, nations_history,
                              nations_building_quizz_menu_callback, 
                              nations_history_quizz_menu_callback,
                              nations_location_quizz_menu_callback,
                              nations_history_quizz, nations_main_menu,
                              level_three_end, nations_to_lenkom,
                              )
from levels.lvl_four import (lenkom_transition, lenkom_building,
                              lenkom_building_quizz, lenkom_history,
                              lenkom_building_quizz_menu_callback, 
                              lenkom_history_quizz_menu_callback,
                              lenkom_location_quizz_menu_callback,
                              lenkom_history_quizz, lenkom_main_menu,
                              level_four_end, lenkom_to_electro,
                              )
from levels.lvl_five import (electro_transition, electro_building,
                              electro_building_quizz, electro_history,
                              electro_building_quizz_menu_callback, 
                              electro_history_quizz_menu_callback,
                              electro_history_quizz, electro_main_menu,
                              level_five_end,
                              )

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

conn = psycopg2.connect(
    host="188.120.245.105",
    port="1500",
    user="root",
    password="96348916318uuf",
    database="scores"
)

# conn = sqlite3.connect('scores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
            (user_id INTEGER PRIMARY KEY, history_score FLOAT,
            building_score FLOAT, level FLOAT)''')


def start(update, context):
    """Функция, запускающая бота"""
    user_id = update.effective_chat.id

    c.execute(
        """INSERT OR IGNORE INTO scores
        (user_id, history_score, building_score, level) VALUES (%s, 0, 0, 0)""",
        (user_id,))
    conn.commit()

    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Прочитать правила 📝'], ['Начать путешествие 🎭']],
        resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}! Давайте начнем наше театральное приключение, ' \
            f'стартовая точка которого — Большой театр. Вы можете сначала ' \
            f'прочитать правила или же сразу приступить к квесту. Выберите, что хотите 👇',
        reply_markup=button
    )
    return 'INTRO'


def feedback(update, context):
    """Отправка фидбэка"""
    text = str(update.message.text).lower()
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=380077303,
        text=f'Фидбэк от пользователя {name}: \n\n{text}',
    )
    update.message.reply_text(
        text='Спасибо!',)


def feedback_receiver(update, context):
    """Получение фидбэка"""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Здесь вы можете отправить любой фидбэк по квесту 👇',
    )
    return 'FEEDBACK'


def cancel(update, context):
    """Завершение бота"""
    user_id = update.effective_chat.id
    c.execute('''DELETE FROM scores
                 WHERE user_id = %s''', (user_id,))
    conn.commit()
    update.message.reply_text(
        text='До встречи!', reply_markup=ReplyKeyboardRemove())
    # c.close()
    # conn.close()
    return ConversationHandler.END


def restart(update, context):
    """Перезапускаем бот"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Прочитать правила 📝'], ['Начать путешествие 🎭']],
        resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}! Давайте начнем наше театральное приключение, ' \
            f'стартовая точка которого — Большой театр. Вы можете сначала ' \
            f'прочитать правила или же сразу приступить к квесту. Выберите, что хотите 👇',
        reply_markup=button
    )
    return 'INTRO'


def main():
    """Создание и запуск бота"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'FEEDBACK': [MessageHandler(Filters.text & ~Filters.command, feedback)],
            #ВСТУПЛЕНИЕ
            'INTRO': [MessageHandler(Filters.regex('^(Прочитать правила 📝|Начать путешествие 🎭)$'), intro)],
            'LEVEL_CHOICE': [MessageHandler(Filters.text & ~Filters.command, level_choice)],
            'INTRO_2': [MessageHandler(Filters.text & ~Filters.command, intro_two)],
            'INTRO_3': [MessageHandler(Filters.text & ~Filters.command, intro_three)],
            'INTRO_4': [MessageHandler(Filters.text & ~Filters.command, intro_four)],

            #БОЛЬШОЙ ТЕАТР
            'BOLSHOI_MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, bolshoi_main_menu)],
            'BOLSHOI_HISTORY': [MessageHandler(Filters.text & ~Filters.command, bolshoi_history)],
            'BOLSHOI_BUILDING': [MessageHandler(Filters.text & ~Filters.command, bolshoi_building)],
            'BOLSHOI_HISTORY_QUIZZ': [
                        CallbackQueryHandler(history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, bolshoi_history_quizz)],
            'BOLSHOI_BUILDING_QUIZZ': [
                        CallbackQueryHandler(building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, bolshoi_building_quizz)],
            'LEVEL_ONE_END': [MessageHandler(Filters.text & ~Filters.command, level_one_end)],
            'BOLSHOI_TO_MXAT_TRANSITION': [
                CallbackQueryHandler(bolshoi_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                MessageHandler(Filters.text & ~Filters.command, bolshoi_to_mxat)],
            'BOLSHOI_LOCATION': [
                        CallbackQueryHandler(bolshoi_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.location & ~Filters.command, mxat_transition)],

            #МХТ ЧЕХОВА
            'MXAT_MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, mxat_main_menu)],
            'MXAT_HISTORY': [MessageHandler(Filters.text & ~Filters.command, mxat_history)],
            'MXAT_BUILDING': [MessageHandler(Filters.text & ~Filters.command, mxat_building)],
            'MXAT_HISTORY_QUIZZ': [
                        CallbackQueryHandler(mxat_history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, mxat_history_quizz)],
            'MXAT_BUILDING_QUIZZ': [
                        CallbackQueryHandler(mxat_building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, mxat_building_quizz)],
            'LEVEL_TWO_END': [MessageHandler(Filters.text & ~Filters.command, level_two_end)],
            'MXAT_TO_NATIONS_TRANSITION': [
                CallbackQueryHandler(mxat_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                MessageHandler(Filters.text & ~Filters.command, mxat_to_nations)],
            'MXAT_LOCATION': [
                        CallbackQueryHandler(mxat_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.location & ~Filters.command, nations_transition)],

            #ТЕАТР НАЦИЙ
            'NATIONS_MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, nations_main_menu)],
            'NATIONS_HISTORY': [MessageHandler(Filters.text & ~Filters.command, nations_history)],
            'NATIONS_BUILDING': [MessageHandler(Filters.text & ~Filters.command, nations_building)],
            'NATIONS_HISTORY_QUIZZ': [
                        CallbackQueryHandler(nations_history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, nations_history_quizz)],
            'NATIONS_BUILDING_QUIZZ': [
                        CallbackQueryHandler(nations_building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, nations_building_quizz)],
            'LEVEL_THREE_END': [MessageHandler(Filters.text & ~Filters.command, level_three_end)],
            'NATIONS_TO_LENKOM_TRANSITION': [
                CallbackQueryHandler(nations_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                MessageHandler(Filters.text & ~Filters.command, nations_to_lenkom)],
            'NATIONS_LOCATION': [
                        CallbackQueryHandler(nations_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.location & ~Filters.command, lenkom_transition)],

            #ЛЕНКОМ
            'LENKOM_TRANSITION': [MessageHandler(Filters.text & ~Filters.command, lenkom_transition)],
            'LENKOM_MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, lenkom_main_menu)],
            'LENKOM_HISTORY': [MessageHandler(Filters.text & ~Filters.command, lenkom_history)],
            'LENKOM_BUILDING': [MessageHandler(Filters.text & ~Filters.command, lenkom_building)],
            'LENKOM_HISTORY_QUIZZ': [
                        CallbackQueryHandler(lenkom_history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, lenkom_history_quizz)],
            'LENKOM_BUILDING_QUIZZ': [
                        CallbackQueryHandler(lenkom_building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, lenkom_building_quizz)],
            'LEVEL_FOUR_END': [MessageHandler(Filters.text & ~Filters.command, level_four_end)],
            'LENKOM_TO_LENKOM_TRANSITION': [
                CallbackQueryHandler(lenkom_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                MessageHandler(Filters.text & ~Filters.command, lenkom_to_electro)],
            'LENKOM_LOCATION': [
                        CallbackQueryHandler(lenkom_location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.location & ~Filters.command, electro_transition)],

            #ЭЛЕКТРОТЕАТР
            'ELECTRO_TRANSITION': [MessageHandler(Filters.text & ~Filters.command, electro_transition)],
            'ELECTRO_MAIN_MENU': [MessageHandler(Filters.text & ~Filters.command, electro_main_menu)],
            'ELECTRO_HISTORY': [MessageHandler(Filters.text & ~Filters.command, electro_history)],
            'ELECTRO_BUILDING': [MessageHandler(Filters.text & ~Filters.command, electro_building)],
            'ELECTRO_HISTORY_QUIZZ': [
                        CallbackQueryHandler(electro_history_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, electro_history_quizz)],
            'ELECTRO_BUILDING_QUIZZ': [
                        CallbackQueryHandler(electro_building_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.text & ~Filters.command, electro_building_quizz)],
            'LEVEL_FIVE_END': [MessageHandler(Filters.text & ~Filters.command, level_five_end)],
        },
        fallbacks=[CommandHandler('restart', restart), 
                   CommandHandler('levels', level_choice_menu),
                   CommandHandler('cancel', cancel),
                   CommandHandler('feedback', feedback_receiver)],
        per_chat=True,
    )

    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    main()

if __name__ == '__main__':
    main()
