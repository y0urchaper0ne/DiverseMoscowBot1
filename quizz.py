# from testbot import LEVEL_COUNTER

# LEVEL_COUNTER = 0.0

def first_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ('большой', 'большой театр', 'большого', 'большого театра'):
        # LEVEL_COUNTER += 0.5
        return 'Молодец! Это правильный ответ 🏅'
    else: return 'Прости, я тебя не понял 🙁 Попробуй ввести ответ еще раз'