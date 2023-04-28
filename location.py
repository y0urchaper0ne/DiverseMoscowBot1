from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from geopy import distance

# Функция для проверки местоположения пользователя
def check_location_mxat(update: Update, context: CallbackContext) -> None:
    # Получаем объект геолокации из сообщения пользователя
    location = update.message.location
    
    # Координаты места, которое нужно проверить
    target_latitude = 55.760236
    target_longitude = 37.612991
    
    # Вычисляем расстояние между двумя точками
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    # Проверяем, находится ли пользователь в радиусе 100 метров от места
    if distance_in_meters <= 300:
        message = "Все верно! 👏 Следующая остановка нашего маршрута – МХТ им. Чехова!"
    else:
        message = "К сожалению, ты не угадал 🙁 \nПодумай еще!"
    
    # Отправляем сообщение пользователю
    update.message.reply_text(message)


def check_location_nations(update: Update, context: CallbackContext) -> None:
    # Получаем объект геолокации из сообщения пользователя
    location = update.message.location
    
    # Координаты места, которое нужно проверить
    target_latitude = 55.765944
    target_longitude = 37.612748
    
    # Вычисляем расстояние между двумя точками
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    # Проверяем, находится ли пользователь в радиусе 100 метров от места
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    # Отправляем сообщение пользователю
    update.message.reply_text(message)


def check_location_lenkom(update: Update, context: CallbackContext) -> None:
    # Получаем объект геолокации из сообщения пользователя
    location = update.message.location
    
    # Координаты места, которое нужно проверить
    target_latitude = 55.767762
    target_longitude = 37.606909
    
    # Вычисляем расстояние между двумя точками
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    # Проверяем, находится ли пользователь в радиусе 100 метров от места
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    # Отправляем сообщение пользователю
    update.message.reply_text(message)


def check_location_electro(update: Update, context: CallbackContext) -> None:
    # Получаем объект геолокации из сообщения пользователя
    location = update.message.location
    
    # Координаты места, которое нужно проверить
    target_latitude = 55.766825
    target_longitude = 37.600945
    
    # Вычисляем расстояние между двумя точками
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    # Проверяем, находится ли пользователь в радиусе 100 метров от места
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    # Отправляем сообщение пользователю
    update.message.reply_text(message)

# Функция для обработки команды /check
def start(update: Update, context: CallbackContext) -> None:
    # Отправляем запрос на геолокацию
    update.message.reply_text("Отправьте мне свою геолокацию, чтобы я проверил ваше местоположение")
    
    # Регистрируем обработчик геолокации
    return "LOCATION"

# Функция для обработки геолокации
def location(update: Update, context: CallbackContext) -> None:
    # Вызываем функцию проверки местоположения пользователя
    check_location_mxat(update, context)
    
    # Снимаем регистрацию обработчика геолокации
    return ConversationHandler.END

# # Создаем объект updater и регистрируем обработчики команд и сообщений
# updater = Updater("5431544410:AAE8CXiXkE3ZZcB1TxvMXTZhJwxMcGwtnMU")
# dispatcher = updater.dispatcher

# # Создаем обработчик команды /check
# start_handler = CommandHandler("check", start)

# # Создаем обработчик геолокации
# location_handler = MessageHandler(Filters.location, location)

# # Регистрируем обработчики команды /check и геолокации
# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(ConversationHandler(
#     entry_points=[location_handler],
#     states={"LOCATION": [location_handler]},
#     fallbacks=[]
# ))

# # Запускаем бота
# updater.start_polling()
# updater.idle()
