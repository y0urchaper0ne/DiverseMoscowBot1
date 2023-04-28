def first_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ('большой', 'большой театр', 'большого', 'большого театра'):
        # LEVEL_COUNTER += 0.5
        return 'Молодец! Это правильный ответ 🏅'
    else: 
        return 'Прости, я тебя не понял 🙁 Попробуй ввести ответ еще раз'
    

def bolshoi_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ('история'):
        return 'Молодец! Это правильный ответ 🏅'
    else: 
        return 'К сожалению, это неверный ответ 🙁 Подумай еще!'

def bolshoi_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ('здание'):
        return 'Молодец! Это правильный ответ 🏅'
    else: 
        return 'К сожалению, это неверный ответ 🙁 Подумай еще!'