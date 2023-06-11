from geopy import distance
from telegram import Update
from telegram.ext import CallbackContext

def check_location_mxat(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.760236
    target_longitude = 37.612991
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 100:
        return True
    else:
        return False


def check_location_nations(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.765944
    target_longitude = 37.612748
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 100:
        return True
    else:
        return False


def check_location_lenkom(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.767762
    target_longitude = 37.606909
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 100:
        return True
    else:
        return False


def check_location_electro(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    
    target_latitude = 55.766825
    target_longitude = 37.600945
    
    user_location = (location.latitude, location.longitude)
    target_location = (target_latitude, target_longitude)
    distance_in_meters = distance.distance(user_location, target_location).m
    
    if distance_in_meters <= 100:
        return True
    else:
        return False
