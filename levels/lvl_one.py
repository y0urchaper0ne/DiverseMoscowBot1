import time

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, 
                      ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from quizz import (bolshoi_history_question, bolshoi_building_question, 
                   bolshoi_to_mxat_question)
from files_manager import (get_building_score, get_history_score,
                           get_user_level, increment_level_count,
                           increment_building_score, increment_history_score)
from texts.text_one import *

main_menu_closed = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Перейти дальше 🔒']], 
                                       resize_keyboard=True)
main_menu_open = ReplyKeyboardMarkup([['История 📜'], ['Здание 🏛️'], ['Перейти дальше 🔑']], 
                                     resize_keyboard=True)


def level_choice_menu(update, context):
    user_id = update.effective_chat.id
    lvl_one_button = 'Уровень 1 ✅'
    if get_user_level(user_id) >= 2:
        lvl_two_button = 'Уровень 2 ✅'
    else: lvl_two_button = 'Уровень 2 ⛔️'
    if get_user_level(user_id) >= 3:
        lvl_three_button = 'Уровень 3 ✅'
    else: lvl_three_button = 'Уровень 3 ⛔️'
    if get_user_level(user_id) >= 4:
        lvl_four_button = 'Уровень 4 ✅'
    else: lvl_four_button = 'Уровень 4 ⛔️'
    if get_user_level(user_id) >= 5:
        lvl_five_button = 'Уровень 5 ✅'
    else: lvl_five_button = 'Уровень 5 ⛔️'
    levels_menu = ReplyKeyboardMarkup([
        [f'{lvl_one_button}'], [f'{lvl_two_button}'], [f'{lvl_three_button}'],
        [f'{lvl_four_button}'], [f'{lvl_five_button}']], resize_keyboard=True)
    update.message.reply_text(text='Выберите, на какой уровень вы хотите перейти!', 
                              reply_markup=levels_menu)
    return 'LEVEL_CHOICE'


def intro(update, context):
    if str(update.message.text) == 'Начать путешествие 🎭':
        button = ReplyKeyboardMarkup([['Да, интересуюсь']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_photo(
            photo="https://wampi.ru/image/RXB3FF0",
            caption = 'Bonjour!',
            reply_markup=ReplyKeyboardRemove()) 
        time.sleep(2)
        update.message.reply_text(text=louis_1, reply_markup=button)
        return 'INTRO_2'
    elif str(update.message.text) == 'Прочитать правила 📝':
        update.message.reply_text(
            text=rules,
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Инструкция по прохождению', url=rules_url)]]))
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')
    

def level_choice(update, context):
    user_id = update.effective_chat.id
    if str(update.message.text)[:-2] == 'Уровень 1':
        if get_user_level(user_id) >= 1.0:
            if get_building_score(user_id) >= 1.0 and get_history_score(user_id) >= 1.0:
                reply_markup = main_menu_open
            else: reply_markup = main_menu_closed
            update.message.reply_text(text='Про что хотите узнать: историю театра или здание?', 
                                      reply_markup=reply_markup)
            return 'BOLSHOI_MAIN_MENU'
        else:
            button = ReplyKeyboardMarkup(
                [['Да, интересуюсь']], resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_photo(
                photo="https://wampi.ru/image/RXB3FF0",
                caption = 'Bonjour!', reply_markup=ReplyKeyboardRemove()) 
            time.sleep(2)
            update.message.reply_text(text=louis_1, reply_markup=button)
            return 'INTRO_2'

    if str(update.message.text)[:-2] == 'Уровень 2' and get_user_level(user_id) >= 2.0:
        if get_building_score(user_id) >= 2.0 and get_history_score(user_id) >= 2.0:
            reply_markup = main_menu_open
        else: reply_markup = main_menu_closed
        update.message.reply_text(
            text='Предлагаю начать знакомство с театром — выбирайте, история или здание?', 
            reply_markup=reply_markup)
        return 'MXAT_MAIN_MENU'

    if str(update.message.text)[:-2] == 'Уровень 3' and get_user_level(user_id) >= 3.0:
        if get_building_score(user_id) >= 3.0 and get_history_score(user_id) >= 3.0:
            reply_markup = main_menu_open
        else: reply_markup = main_menu_closed
        update.message.reply_text(
            text='C чего начнем в этот раз?', 
            reply_markup=reply_markup)
        return 'NATIONS_MAIN_MENU'

    if str(update.message.text)[:-2] == 'Уровень 4' and get_user_level(user_id) >= 4.0:
        if get_building_score(user_id) >= 4.0 and get_history_score(user_id) >= 4.0:
            reply_markup = main_menu_open
        else: reply_markup = main_menu_closed
        update.message.reply_text(
            text='Про что узнаем сперва?', 
            reply_markup=reply_markup)
        return 'LENKOM_MAIN_MENU'

    if str(update.message.text)[:-2] == 'Уровень 5' and get_user_level(user_id) >= 5.0:
        if get_building_score(user_id) >= 5.0 and get_history_score(user_id) >= 5.0:
            reply_markup = main_menu_open
        else: reply_markup = main_menu_closed
        update.message.reply_text(
            text='Про что рассказать вам — историю или здание?', 
            reply_markup=reply_markup)
        return 'ELECTRO_MAIN_MENU'
    else: update.message.reply_text(text='Похоже, этот уровень тебе еще недоступен!')


def intro_two(update, context):
    if str(update.message.text) == 'Да, интересуюсь':
        button = ReplyKeyboardMarkup([['Эээ… Oui?']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=louis_2)
        time.sleep(3)
        update.message.reply_text(text=louis_3)
        time.sleep(3)
        update.message.reply_text(text='Не могли бы вы мне помочь?', reply_markup=button)
        return 'INTRO_3'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def intro_three(update, context):
    if str(update.message.text) == 'Эээ… Oui?':
        button = ReplyKeyboardMarkup([['По рукам!']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=louis_4)
        time.sleep(3)
        update.message.reply_text(text=louis_5, reply_markup=button)
        return 'INTRO_4'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def intro_four(update, context):
    user_id = update.effective_chat.id
    if get_history_score(user_id) < 1.0:
        history_menu = main_menu_closed
    else: 
        history_menu = main_menu_open
    if str(update.message.text) == 'По рукам!':
        increment_level_count(user_id)
        update.message.reply_text(text=louis_6)
        time.sleep(3)
        update.message.reply_text(text='Про что хотите узнать: историю театра или здание?',
                                  reply_markup=history_menu)
        return 'BOLSHOI_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


unit_menu_quizz = ReplyKeyboardMarkup([['Загадка'], ['Назад']], resize_keyboard=True)
unit_menu_wo_quizz = ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)


def bolshoi_score(user_id):
    if get_building_score(user_id) == 1.0:
        building_score='Загадка на местности: ✅'
    else: building_score='Загадка на местности: ❌'
    if get_history_score(user_id) == 1.0:
        history_score='Загадка на историю: ✅'
    else: history_score='Загадка на историю: ❌' 
    return f'{history_score} \n{building_score}'  


def bolshoi_main_menu(update, context):
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
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='История Большого театра', url=bolshoi_history_url)]]),
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
            reply_markup= InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Здание Большого театра', url=bolshoi_building_url)]]),
            )
        return 'BOLSHOI_BUILDING'
      
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Вперед!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 1.0 or get_history_score(user_id) < 1.0:
            user_score = bolshoi_score(user_id)
            update.message.reply_text(text=f'Вы решили не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) >= 1.0 and get_history_score(user_id) >= 1.0:
            update.message.reply_text(
                text=f'Большому театру — большая история. Поздравляю, вы перешли на второй уровень!' \
                     f' И нам нужно двигаться дальше.', 
                reply_markup=forward_menu)
            return 'LEVEL_ONE_END'

    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


quizz_menu = [[
                InlineKeyboardButton("Подсказка", callback_data='hint'),
                InlineKeyboardButton("Показать ответ", callback_data='answer')]]


def bolshoi_history(update, context):
    """Блок истории Большого театра"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_history_score(user_id) < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://ic.wampi.ru/2023/06/08/bolshoi_history7643e942eeab8632.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'BOLSHOI_HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'BOLSHOI_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def bolshoi_building(update, context):
    """Блок здания Большого театра"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_building_score(user_id) < 1.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo="https://im.wampi.ru/2023/06/08/bolshoi_building.png",
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'BOLSHOI_BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'BOLSHOI_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def bolshoi_history_quizz(update, context):
    """Вопрос по истории Большого театра"""
    user_id = update.effective_chat.id
    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 1.0 and get_history_score(user_id) == 1.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'BOLSHOI_MAIN_MENU'
    response = bolshoi_history_question(text)
    if response == 'Merci! Все так 🥳':
        increment_history_score(user_id)
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'BOLSHOI_HISTORY'
    update.message.reply_text(response)


def history_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Это название дали после первого пожара в 1805 году', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
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
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'BOLSHOI_MAIN_MENU'
    response = bolshoi_building_question(text)
    if response == 'Bravo! Из вас хороший математик 🥳':
        increment_building_score(user_id)
        update.message.reply_text(response, reply_markup=unit_menu_wo_quizz)
        return 'BOLSHOI_BUILDING'
    update.message.reply_text(response)


def building_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Обойдите театр по периметру и обратите внимание на западную сторону здания', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>22</tg-spoiler>', parse_mode='HTML')


def level_one_end(update, context):
    """Обработчик перехода на новый уровень"""
    reply_markup = InlineKeyboardMarkup(quizz_menu)
    if str(update.message.text) == 'Вперед!':
        update.message.reply_photo(
            photo="https://ie.wampi.ru/2023/06/08/mxat_transition.png")
        time.sleep(2)
        update.message.reply_text(
            text=f'Догадались, о каком театре речь? 🤔 \nНапишите его название сообщением!',
            reply_markup=reply_markup)
        return "BOLSHOI_TO_MXAT_TRANSITION"
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def bolshoi_to_mxat(update, context):
    """Обработчик загадки с МХТ"""
    button = ReplyKeyboardMarkup(
        [[KeyboardButton(text='На месте!', request_location=True)]], resize_keyboard=True, one_time_keyboard=True)    
    text = str(update.message.text).lower()
    response = bolshoi_to_mxat_question(text)
    if response == 'Génial! Следующая остановка нашего маршрута — МХТ им. Чехова!':
        update.message.reply_text(response)
        time.sleep(2)
        update.message.reply_text(text=f"{mxat_transition_text}")
        time.sleep(3)
        update.message.reply_text(
            text="Идти до МХТ совсем ничего: дайте знать, когда будете стоять напротив его здания!",
            reply_markup=button)
        return 'BOLSHOI_LOCATION'
    update.message.reply_text(response)


def bolshoi_location_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой локации"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nНапишите его название сообщением!',
            reply_markup=reply_markup)
        query.message.reply_text(
            text=f'💡 Следующий театр носит имя русского драматурга.' \
                 f' В одном из названий его произведений фигурирует птица,'
                 f' которая впоследствии стала символом театра.', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_text(
            text=f'Догадались, о каком театре речь? 🤔 \nНапишите его название сообщением!')
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>МХТ им. Чехова</tg-spoiler>', parse_mode='HTML')
