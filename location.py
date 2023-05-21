from geopy import distance
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

def check_location_mxat(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.760236
    target_longitude = 37.612991
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 300:
        message = "Génial! Следующая остановка нашего маршрута — МХТ им. Чехова!"
    else:
        message = "Oh-la-la! Не совсем 😕"
    
    update.message.reply_text(message)


def check_location_nations(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.765944
    target_longitude = 37.612748
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    update.message.reply_text(message)


def check_location_lenkom(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.767762
    target_longitude = 37.606909
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    update.message.reply_text(message)


def check_location_electro(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.766825
    target_longitude = 37.600945
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 300:
        message = "Вы на месте!"
    else:
        message = "Вы не на месте :("
    
    update.message.reply_text(message)
