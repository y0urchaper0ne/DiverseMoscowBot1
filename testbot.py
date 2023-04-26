import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from quizz import first_question

from text import bolshoi_history, bolshoi_building, bolshoi_history2, rules

import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

LEVEL_COUNTER = 0.0

menu3_buttons = [[
                  InlineKeyboardButton("Подсказка", callback_data='hint'),
                  InlineKeyboardButton("Показать ответ", callback_data='answer')]]

# Создаем функции для обработки команд
# def start(update, context):
#     """Отправляем главное меню"""
#     reply_markup = InlineKeyboardMarkup(menu1_buttons)
#     button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
#     update.message.reply_text('Выберите раздел:', reply_markup=reply_markup)


def wake_up(update, context):
    """Функция, запускающая бота"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Правила 📚'], ['Начать путешествие 🎭']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Давай начнем путешествие по театрам! \nВыбери, про что хочешь узнать сначала 👇'.format(name),
        reply_markup=button
    )


def message_handler_lvl_one(update, context):
    """Обработчик сообщений"""
    global LEVEL_COUNTER

    if LEVEL_COUNTER < 1.0:
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
    else: 
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔑']], resize_keyboard=True)

    if str(update.message.text) == 'Правила 📚':
        update.message.reply_text(text=rules)

    elif str(update.message.text) == 'Начать путешествие 🎭':
        update.message.reply_text(text='Вперед!', reply_markup=main_menu)

    elif str(update.message.text) == 'История 📜':
        history_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        # update.message.reply_chat_action(action='typing', write_timeout=3.0)
        update.message.reply_text(text=f'{bolshoi_history}')
        time.sleep(3)
        update.message.reply_text(
            text=f'{bolshoi_history2}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Читать больше', url="https://bolshoi.ru/")]]),
            parse_mode='HTML')

    elif str(update.message.text) == 'Здание 🏛️':
        building_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{bolshoi_building}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Читать больше', url="https://bolshoi.ru/")]]),
            parse_mode='HTML')
        update.message.reply_photo(
            photo='https://oknadom.ru/wp-content/uploads/2020/12/p_1.jpg')
    
    elif str(update.message.text) == 'Доп. Инфа 🤫':
        extra_menu = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
        update.message.reply_text(
            text=f'Здесь будут ну <b>ОЧЕНЬ</b> интересные факты, о которых мало кто знает',
            parse_mode='HTML',
            reply_markup=extra_menu)
            
    elif str(update.message.text) == 'Назад':
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)

    elif str(update.message.text) == 'Загадка':
        reply_markup = InlineKeyboardMarkup(menu3_buttons)
        update.message.reply_text(
            text=f"Историю какого театра ты только что прочитал? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
    
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True)
        if LEVEL_COUNTER < 1.0:
            update.message.reply_text(text='Ты решил не все загадки!')
        elif LEVEL_COUNTER == 1.0:
            update.message.reply_text(text='Отлично! Идем дальше', reply_markup=forward_menu)
            return LEVEL_COUNTER

    elif str(update.message.text) == 'Вперед!':
        update.message.reply_text(text=f'Молодец, ты перешел на второй уровень! \n\nОтправляйся сюда 👇')
        update.message.reply_location(latitude=55.760073, longitude=37.613144)

    elif str(update.message.text) == 'LEVEL_COUNTER': 
        update.message.reply_text(text=LEVEL_COUNTER, reply_markup=main_menu)  


    else: 
        text = str(update.message.text).lower()
        response = first_question(text)
        if response == 'Молодец! Это правильный ответ 🏅':
            LEVEL_COUNTER += 0.5
            # print(LEVEL_COUNTER)
        update.message.reply_text(response)


def message_handler_lvl_two(update, context):
    """Обработчик сообщений"""
    main_menu = ReplyKeyboardMarkup([['📜 История'], ['🏛️ Здание'], ['🤫 Доп. Инфа']], resize_keyboard=True)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_text(text='Молодец, ты перешел на второй уровень!', reply_markup=main_menu)

    elif str(update.message.text) == 'LEVEL_COUNTER': 
        update.message.reply_text(text=LEVEL_COUNTER)  

    elif str(update.message.text) == '📜 История':
        history_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        # menu2_markup = InlineKeyboardMarkup(menu2_buttons)
        update.message.reply_text(text='Узнаем немного про историю!')
        update.message.reply_text(text=f'{bolshoi_history}')
        time.sleep(3)
        update.message.reply_text(
            text=f'{bolshoi_history2} \n<a href="https://bolshoi.ru/">Читать больше</a>', 
            reply_markup=history_menu, parse_mode='HTML')

    elif str(update.message.text) == '🏛️ Здание':
        # menu2_markup = InlineKeyboardMarkup(menu2_buttons)
        building_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        update.message.reply_text(text='Узнаем немного про здание!')
        update.message.reply_text(
            text=f'{bolshoi_building}', parse_mode='HTML')
        update.message.reply_photo(
            photo='https://oknadom.ru/wp-content/uploads/2020/12/p_1.jpg',
            reply_markup=building_menu)
    
    elif str(update.message.text) == '🤫 Доп. Инфа':
        extra_menu = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
        update.message.reply_text(
            text=f'Здесь будут ну <b>ОЧЕНЬ</b> интересные факты, о которых мало кто знает',
            parse_mode='HTML',
            reply_markup=extra_menu)
            
        update.message.reply_video_note(video_note="DQACAgIAAxkBAAEeoVpkGbZVCjkSphnyyGHM9Jy4oWggXgAC4SkAArTu0EhSPBhw-4Wxgi8E")

    elif str(update.message.text) == 'Назад':
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)

    elif str(update.message.text) == 'Загадка':
        reply_markup = InlineKeyboardMarkup(menu3_buttons)
        update.message.reply_text(
            text=f"Историю какого театра ты только что прочитал? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)

    else: 
        text = str(update.message.text).lower()
        response = first_question(text)
        update.message.reply_text(response)


def menu3_callback(update, context):
    """Обработчик выбора меню для загадки"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f"Историю какого театра ты только что прочитал? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        query.message.reply_text(
            text='Подсказка', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f"Историю какого театра ты только что прочитал? \nПиши ответ внизу 👇")
        query.message.reply_text(
            text=f'<tg-spoiler>ответ на загадку</tg-spoiler>', parse_mode='HTML')      


def main():
    """Создаем и запускаем бота"""
    global LEVEL_COUNTER
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CallbackQueryHandler(menu3_callback, pattern='^(hint|answer)$'))

    # if LEVEL_COUNTER < 1.0:
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler_lvl_one))
    if (LEVEL_COUNTER >= 1.0) and (LEVEL_COUNTER < 2.0):
        updater.dispatcher.remove_handler(message_handler_lvl_one)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler_lvl_two))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
