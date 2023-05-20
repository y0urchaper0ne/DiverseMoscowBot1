def bolshoi_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['большой петровский театр', 'большой петровский']:
        return 'Merci! Все так 🥳'
    else: 
        return 'Oh-la-la! Не совсем 😕'

def bolshoi_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['22']:
        return 'Bravo! Из вас хороший математик 🥳'
    else: 
        return 'Oh-la-la! Не совсем😕'