import time
import sqlite3

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from quizz import mxat_history_question, mxat_building_question, mxat_to_nations_question
from location import check_location_mxat
from texts.text_two import *
from levels.lvl_one import (main_menu_closed, main_menu_open, 
                            unit_menu_quizz, unit_menu_wo_quizz,
                            quizz_menu,)
from files_manager import (get_building_score, get_history_score,
                           increment_level_count, increment_building_score,
                           increment_history_score)


def mxat_score(user_id):
    if get_building_score(user_id) == 2.0:
        building_score='Загадка на местности: ✅'
    else: building_score='Загадка на местности: ❌'
    if get_history_score(user_id) == 2.0:
        history_score='Загадка на историю: ✅'
    else: history_score='Загадка на историю: ❌' 
    return f'{history_score} \n{building_score}' 


def mxat_transition(update, context):
    """Обработчик геолокации"""
    user_id = update.effective_chat.id
    response = check_location_mxat(update, context)
    if response:
        increment_level_count(user_id)
        update.message.reply_text(
            text='Предлагаю начать знакомство с театром — выбирайте, история или здание?', 
            reply_markup=main_menu_closed)
        return 'MXAT_MAIN_MENU'
    update.message.reply_text(text='Похоже, вы еще не дошли до театра')


def mxat_main_menu(update, context):
    """Главное меню уровня"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'История 📜':
        if get_history_score(user_id) < 2.0:
            history_menu = unit_menu_quizz
        else: 
            history_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        time.sleep(1)
        update.message.reply_text(
            text=f'{mxat_history_text}', 
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='История МХТ им. Чехова', url=mxat_history_url)]]),
            )
        return 'MXAT_HISTORY'

    elif str(update.message.text) == 'Здание 🏛️':
        if get_building_score(user_id) < 2.0:
            building_menu = unit_menu_quizz
        else:
            building_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{mxat_building_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Здание МХТ им. Чехова', url=mxat_building_url)]]),
            )
        return 'MXAT_BUILDING'
      
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 2.0 or get_history_score(user_id) < 2.0:
            user_score = mxat_score(user_id)
            update.message.reply_text(text=f'Вы решили не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) >= 2.0 and get_history_score(user_id) >= 2.0:
            update.message.reply_text(
                text=f'МХТ и правда впечатляет своей историей. Bravo, вы теперь на третьем уровне!' \
                     f' Однако нужно скорее двигаться к следующей точке.', 
                reply_markup=forward_menu)
            return 'LEVEL_TWO_END'

    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def mxat_history(update, context):
    """Блок истории МХТ"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_history_score(user_id) < 2.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://ic.wampi.ru/2023/06/08/mxat_history.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'MXAT_HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 2.0 and get_history_score(user_id) == 2.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'MXAT_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def mxat_building(update, context):
    """Блок здания МХТ"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_building_score(user_id) < 2.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://im.wampi.ru/2023/06/08/mxat_building.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'MXAT_BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 2.0 and get_history_score(user_id) == 2.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'MXAT_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def mxat_history_quizz(update, context):
    """Вопрос по истории МХТ"""
    user_id = update.effective_chat.id

    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 2.0 and get_history_score(user_id) == 2.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'MXAT_MAIN_MENU'
    response = mxat_history_question(text)
    if response == 'Parfait! Вы абсолютно правы':
        increment_history_score(user_id)
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'MXAT_HISTORY'
    update.message.reply_text(response)


def mxat_history_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Это одна из известных пьес А.П. Чехова', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Дядя Ваня</tg-spoiler>', parse_mode='HTML')


def mxat_building_quizz(update, context):
    """Вопрос про здание МХТ"""
    user_id = update.effective_chat.id
    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 2.0 and get_history_score(user_id) == 2.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'MXAT_MAIN_MENU'
    response = mxat_building_question(text)
    if response == 'Chic! И правда':
        increment_building_score(user_id)
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'MXAT_BUILDING'
    update.message.reply_text(response)


def mxat_building_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Посмотрите на надпись на двери под горельефом', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Малая сцена</tg-spoiler>', parse_mode='HTML')


def level_two_end(update, context):
    """Обработчик перехода на новый уровень"""
    reply_markup = InlineKeyboardMarkup(quizz_menu)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_photo(
            photo="https://ie.wampi.ru/2023/06/08/nations_transition.png")
        time.sleep(2)
        update.message.reply_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!',
            reply_markup=reply_markup)
        return "MXAT_TO_NATIONS_TRANSITION"
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def mxat_to_nations(update, context):
    """Обработчик загадки с Театром Наций"""
    button = ReplyKeyboardMarkup(
        [[KeyboardButton(text='На месте!', request_location=True)]], resize_keyboard=True, one_time_keyboard=True)    
    text = str(update.message.text).lower()
    response = mxat_to_nations_question(text)
    if response == 'Génial! Следующая точка — Театр Наций!':
        update.message.reply_text(response)
        time.sleep(2)
        update.message.reply_text(text=f"{nations_transition_text}")
        time.sleep(3)
        update.message.reply_text(
            text=nations_transition_text_2,
            reply_markup=button)
        return 'MXAT_LOCATION'
    update.message.reply_text(response)


def mxat_location_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой локации"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!',
            reply_markup=reply_markup)
        query.message.reply_text(
            text=f'💡 Его действующий худрук — Евгений Миронов', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!')
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Театр Наций</tg-spoiler>', parse_mode='HTML')
