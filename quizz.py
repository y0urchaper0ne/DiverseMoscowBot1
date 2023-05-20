def bolshoi_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['история']:
        return 'Молодец! Это правильный ответ 🏅'
    else: 
        return 'К сожалению, это неверный ответ 🙁 Подумай еще!'

def bolshoi_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['22']:
        return 'Молодец! Это правильный ответ 🏅'
    else: 
        return 'К сожалению, это неверный ответ 🙁 Подумай еще!'