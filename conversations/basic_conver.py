from telegram import ReplyKeyboardMarkup
from statements import DELIMITER
replay_keyboard = [
    ['/generate', '/save'],
    ['/find', '/show_list']
]

basic_markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=False)

def get_value(callback_data: str):
    vals = callback_data.split(DELIMITER)
    return vals[1]


