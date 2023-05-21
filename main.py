import sqlite3

import warnings

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.ext import (CallbackQueryHandler,
                          CommandHandler, ConversationHandler,
                          Filters, Updater, MessageHandler)

from lvl_one import (intro, intro_two, intro_three, intro_four,
                     bolshoi_building, bolshoi_building_quizz, 
                     bolshoi_history, bolshoi_history_quizz,
                     bolshoi_main_menu, history_quizz_menu_callback,
                     building_quizz_menu_callback, level_one_end,
                     location_callback, location_quizz_menu_callback
                    )

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

conn = sqlite3.connect('scores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
            (user_id INTEGER PRIMARY KEY, history_score FLOAT,
            building_score FLOAT)''')


def wake_up(update, context):
    """Функция, запускающая бота"""
    user_id = update.effective_chat.id

    c.execute(
        """INSERT OR IGNORE INTO scores
        (user_id, history_score, building_score) VALUES (?, 0, 0)""",
        (user_id,))
    conn.commit()

    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Прочитать правила 📝'], ['Начать путешествие 🎭']],
        resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}! Давайте начнем наше театральное приключение, стартовая точка которого — Большой театр. Вы можете сначала прочитать правила или же сразу приступить к квесту. Выберите, что хочешь 👇'.format(name),
        reply_markup=button
    )
    return 'INTRO'


def cancel(update, context):
    """Завершение бота"""
    user_id = update.effective_chat.id
    c.execute('''DELETE FROM scores
                 WHERE user_id = ?''', (user_id,))
    update.message.reply_text(
        text='До встречи!', reply_markup=ReplyKeyboardRemove())
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
            'BOLSHOI_LOCATION': [
                        CallbackQueryHandler(location_quizz_menu_callback, pattern='^(hint|answer)$'),
                        MessageHandler(Filters.location & ~Filters.command, location_callback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
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
