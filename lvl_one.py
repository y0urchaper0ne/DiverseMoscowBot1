import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters
from quizz import bolshoi_history_question, bolshoi_building_question
from location import check_location_mxat, location
from text import bolshoi_history_text, bolshoi_building_text, bolshoi_history2_text, rules

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

HISTORY_SCORE = 0.0
BUILDING_SCORE = 0.0

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
    return 'INTRO'

def intro(update, context):
    main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
    if str(update.message.text) == 'Начать путешествие 🎭':
        update.message.reply_text(text='Вперед!', reply_markup=main_menu)
        return 'MAIN_MENU'
    elif str(update.message.text) == 'Правила 📚':
        update.message.reply_text(text=rules)


def main_menu(update, context):
    """Главное меню уровня"""
    global HISTORY_SCORE, BUILDING_SCORE

    if HISTORY_SCORE == 1.0 and BUILDING_SCORE == 1.0:
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔑']], resize_keyboard=True)
    else: 
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)

    if str(update.message.text) == 'История 📜':
        if HISTORY_SCORE < 1.0:
            history_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        else: 
            history_menu = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
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
        if BUILDING_SCORE < 1.0:
            building_menu = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
        else:
            building_menu = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{bolshoi_building_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Читать больше', url="https://bolshoi.ru/")]]),
            parse_mode='HTML')
        update.message.reply_photo(
            photo='https://oknadom.ru/wp-content/uploads/2020/12/p_1.jpg')
        return 'BOLSHOI_BUILDING'
    
    elif str(update.message.text) == 'Доп. Инфа 🤫':
        return 'BOLSHOI_EXTRA'
        
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if (HISTORY_SCORE < 1.0) or (BUILDING_SCORE < 1.0):
            update.message.reply_text(text='Ты решил не все загадки!')
        elif HISTORY_SCORE == 1.0 and BUILDING_SCORE == 1.0:
            update.message.reply_text(text='Отлично! Идем дальше', reply_markup=forward_menu)
            return 'LEVEL_END'

    elif str(update.message.text) == 'SCORE': 
        update.message.reply_text(text=f'HISTORY_SCORE: {HISTORY_SCORE} \nBUILDING_SCORE: {BUILDING_SCORE}', 
                                  reply_markup=main_menu)
    # else: update.message.reply_text(text=f'Прости, я тебя не понял')


quizz_menu = [[
                  InlineKeyboardButton("Подсказка", callback_data='hint'),
                  InlineKeyboardButton("Показать ответ", callback_data='answer')]]


def bolshoi_history(update, context):
    """Блок истории Большого театра"""
    global HISTORY_SCORE

    if str(update.message.text) == 'Загадка' and HISTORY_SCORE < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_text(
            text=f"Это загадка на знание истории большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        return 'HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'


def bolshoi_building(update, context):
    """Блок здания Большого театра"""
    global BUILDING_SCORE

    if str(update.message.text) == 'Загадка' and BUILDING_SCORE < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_text(
            text=f"Это загадка на местности большого театра? \nПиши ответ внизу 👇",
            reply_markup=reply_markup)
        return 'BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'


def bolshoi_extra(update, context):
    """Блок дополнительной информации о Большом театре"""
    extra_menu = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
    update.message.reply_text(
        text=f'Здесь будут ну <b>ОЧЕНЬ</b> интересные факты, о которых мало кто знает',
        parse_mode='HTML',
        reply_markup=extra_menu)
    if str(update.message.text) == 'Назад':
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'

def bolshoi_history_quizz(update, context):
    """Вопрос по истории Большого театра"""
    global HISTORY_SCORE

    text = str(update.message.text).lower()
    if text == 'назад':
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
        return 'MAIN_MENU'
    response = bolshoi_history_question(text)
    if response == 'Молодец! Это правильный ответ 🏅':
        HISTORY_SCORE += 1.0
        update.message.reply_text(response)
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
    """Вопрос по истории Большого театра"""
    global BUILDING_SCORE

    text = str(update.message.text).lower()
    if text == 'назад':
        main_menu = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Доп. Инфа 🤫'], ['Перейти дальше 🔒']], resize_keyboard=True)
        update.message.reply_text(text='Выбери, про что хочешь узнать!', reply_markup=main_menu)
    response = bolshoi_building_question(text)
    if response == 'Молодец! Это правильный ответ 🏅':
        BUILDING_SCORE += 1.0
        update.message.reply_text(response)
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
    update.message.reply_text(text='До встречи!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
 

def main():
    """Создаем и запускаем бота"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # dispatcher.add_handler(MessageHandler(Filters.text, wake_up))

    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', wake_up)],
        states={
            'INTRO': [MessageHandler(Filters.regex('^(Правила 📚|Начать путешествие 🎭)$'), intro)],
            # 'MAIN_MENU': [MessageHandler(Filters.regex('^(История 📜|Здание 🏛️|Доп. Инфа 🤫|Перейти дальше 🔒)$'), main_menu)],
            'MAIN_MENU': [MessageHandler(Filters.text, main_menu)],
            'BOLSHOI_HISTORY': [MessageHandler(Filters.text, bolshoi_history)],
            'BOLSHOI_BUILDING': [MessageHandler(Filters.text, bolshoi_building)],
            'BOLSHOI_EXTRA': [MessageHandler(Filters.text, bolshoi_extra)],
            'HISTORY_QUIZZ': [
                        MessageHandler(Filters.regex('^(hint|answer)$'), history_quizz_menu_callback), 
                        MessageHandler(Filters.text, bolshoi_history_quizz)],
            'BUILDING_QUIZZ': [
                        MessageHandler(Filters.regex('^(hint|answer)$'), building_quizz_menu_callback), 
                        MessageHandler(Filters.text, bolshoi_building_quizz)],
            'LEVEL_END': [
                        MessageHandler(Filters.regex('^(hint|answer)$'), location_quizz_menu_callback), 
            ]
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

if __name__ == '__main__':
    main()
