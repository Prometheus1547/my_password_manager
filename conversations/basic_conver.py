from telegram import ReplyKeyboardMarkup

replay_keyboard = [
    ['/generate', '/save'],
    ['/find', '/show_list']
]

markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=False)

