import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from quizz import nations_building_question, nations_history_question, nations_to_lenkom_question
from location import check_location_nations
from texts.text_three import *
from levels.lvl_one import (main_menu_closed, main_menu_open, 
                            unit_menu_quizz, unit_menu_wo_quizz,
                            quizz_menu,)
from files_manager import (get_building_score, get_history_score,
                           increment_level_count, increment_building_score,
                           increment_history_score)


def nations_score(user_id):
    if get_building_score(user_id) == 3.0:
        building_score='Загадка на местности: ✅'
    else: building_score='Загадка на местности: ❌'
    if get_history_score(user_id) == 3.0:
        history_score='Загадка на историю: ✅'
    else: history_score='Загадка на историю: ❌' 
    return f'{history_score} \n{building_score}' 


def nations_transition(update, context):
    """Обработчик геолокации"""
    user_id = update.effective_chat.id
    response = check_location_nations(update, context)
    if response:
        increment_level_count(user_id)
        update.message.reply_text(
            text='C чего начнем в этот раз?', 
            reply_markup=main_menu_closed)
        return 'NATIONS_MAIN_MENU'
    update.message.reply_text(text='Похоже, вы еще не дошли до театра')


def nations_main_menu(update, context):
    """Главное меню уровня"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'История 📜':
        if get_history_score(user_id) < 3.0:
            history_menu = unit_menu_quizz
        else: 
            history_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        time.sleep(1)
        update.message.reply_text(
            text=f'{nations_history_text}', 
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='История Театра Наций', url=nations_history_url)]]),
            )
        return 'NATIONS_HISTORY'

    elif str(update.message.text) == 'Здание 🏛️':
        if get_building_score(user_id) < 3.0:
            building_menu = unit_menu_quizz
        else:
            building_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{nations_building_text}', 
            reply_markup= InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Здание Театра Наций', url=nations_building_url)]]),
            )
        return 'NATIONS_BUILDING'
      
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 3.0 or get_history_score(user_id) < 3.0:
            user_score = nations_score(user_id)
            update.message.reply_text(text=f'Вы решили не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) >= 3.0 and get_history_score(user_id) >= 3.0:
            update.message.reply_text(
                text=f'Больше половины нашего promenade уже позади! Вы уже на четвертом уровне, bravo 🥳 \n\n' \
                     f'Давайте же скорее пойдем к следующей точке.', 
                reply_markup=forward_menu)
            return 'LEVEL_THREE_END'

    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def nations_history(update, context):
    """Блок истории Театра Наций"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_history_score(user_id) < 3.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://ic.wampi.ru/2023/06/08/nations_history.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'NATIONS_HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 3.0 and get_history_score(user_id) == 3.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'NATIONS_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def nations_building(update, context):
    """Блок здания Театра Наций"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_building_score(user_id) < 3.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://im.wampi.ru/2023/06/08/nations_building.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'NATIONS_BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 3.0 and get_history_score(user_id) == 3.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'NATIONS_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def nations_history_quizz(update, context):
    """Вопрос по истории Театра Наций"""
    user_id = update.effective_chat.id

    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 3.0 and get_history_score(user_id) == 3.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'NATIONS_MAIN_MENU'
    response = nations_history_question(text)
    if response == 'Bravo! Все верно 🥳':
        increment_history_score(user_id)
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'NATIONS_HISTORY'
    update.message.reply_text(response)


def nations_history_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Их название отсылает ко времени суток', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Утренники</tg-spoiler>', parse_mode='HTML')


def nations_building_quizz(update, context):
    """Вопрос про здание Театра Наций"""
    user_id = update.effective_chat.id
    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 3.0 and get_history_score(user_id) == 3.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'NATIONS_MAIN_MENU'
    response = nations_building_question(text)
    if response == 'Bien! Вы очень внимательны':
        increment_building_score(user_id)
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'NATIONS_BUILDING'
    update.message.reply_text(response)


def nations_building_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Оно показывает направление ветра', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Флюгер</tg-spoiler>', parse_mode='HTML')


def level_three_end(update, context):
    """Обработчик перехода на новый уровень"""
    reply_markup = InlineKeyboardMarkup(quizz_menu)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_photo(
            photo="https://ie.wampi.ru/2023/06/08/lenkom_transition.png")
        time.sleep(2)
        update.message.reply_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!',
            reply_markup=reply_markup)
        return "NATIONS_TO_LENKOM_TRANSITION"
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def nations_to_lenkom(update, context):
    """Обработчик загадки с Ленкомом"""
    button = ReplyKeyboardMarkup(
        [[KeyboardButton(text='На месте!', request_location=True)]], resize_keyboard=True, one_time_keyboard=True)    
    text = str(update.message.text).lower()
    response = nations_to_lenkom_question(text)
    if response == 'Génial! Мы направляемся к Ленкому Марка Захарова!':
        update.message.reply_text(response)
        time.sleep(2)
        update.message.reply_text(
            text=lenkom_transition_text,
            reply_markup=button)
        return 'NATIONS_LOCATION'
    update.message.reply_text(response)


def nations_location_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой локации"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!',
            reply_markup=reply_markup)
        query.message.reply_text(
            text=f'💡 Загаданный фильм — «12 стульев»', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nОтправьте его название в сообщении!')
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>Ленком Марка Захарова</tg-spoiler>', parse_mode='HTML')
