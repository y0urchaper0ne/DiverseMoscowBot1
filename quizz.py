import random

negative_answers = ['Oh-la-la! Не совсем 😕', 'Non! Есть еще варианты? 🧐',
                    'Mais non! Не совсем правильно 😓', 'Hm… Сомневаюсь 🙁',
                    'Oh mon dieu! Не соглашусь 😥']


def bolshoi_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['большой петровский театр', 'большой петровский']:
        return 'Merci! Все так 🥳'
    else: 
        return random.choice(negative_answers)


def bolshoi_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['22']:
        return 'Bravo! Из вас хороший математик 🥳'
    else: 
        return random.choice(negative_answers)

def bolshoi_to_mxat_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['мхт', 'мхт чехова', 'мхт имени чехова', 'мхт им.чехова',
                        'московский художественный театр имени чехова', 
                        'московский художественный театр', 'мхт им. чехова']:
        return 'Génial! Следующая остановка нашего маршрута — МХТ им. Чехова!'
    else: 
        return random.choice(negative_answers)


def mxat_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['дядя ваня']:
        return 'Parfait! Вы абсолютно правы'
    else: 
        return random.choice(negative_answers)


def mxat_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['малая сцена']:
        return 'Chic! И правда'
    else: 
        return random.choice(negative_answers)
    

def mxat_to_nations_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['театр наций', 'наций']:
        return 'Génial! Следующая точка — Театр Наций!'
    else: 
        return random.choice(negative_answers)


def nations_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['утренники']:
        return 'Bravo! Все верно 🥳'
    else: 
        return random.choice(negative_answers)


def nations_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['флюгер']:
        return 'Bien! Вы очень внимательны'
    else: 
        return random.choice(negative_answers)


def nations_to_lenkom_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['ленком', 'ленком марка захарова',
                        'ленком им. марка захарова',
                        'ленком имени марка захарова']:
        return 'Génial! Мы направляемся к Ленкому Марка Захарова!'
    else: 
        return random.choice(negative_answers)


def lenkom_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['в день свадьбы']:
        return 'Parfait! Все так 🥳'
    else: 
        return random.choice(negative_answers)


def lenkom_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['марк захаров',
                        'марка захарова',
                        'захаров', 'захарова']:
        return 'Magnifique! Вы очень наблюдательны'
    else: 
        return random.choice(negative_answers)


def lenkom_to_electro_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['электротеатр', 
                        'электротеатр станиславский',
                        'электротеатр станиславского']:
        return 'Génial! Наша финальная точка — Электротеатр Станиславский!'
    else: 
        return random.choice(negative_answers)


def electro_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['50']:
        return 'Parfait! Вы абсолютно правы 👏'
    else: 
        return random.choice(negative_answers)


def electro_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['1918']:
        return 'Chic! И правда 🤗'
    else: 
        return random.choice(negative_answers)
