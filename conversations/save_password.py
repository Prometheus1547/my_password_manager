from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

import passwords_handlers as ph
from statements import SAVING
from conversations.basic_conver import markup

def save_password_question_1(update: Update, context):
    replay_keyboard = [
        ['YES', 'NO']
    ]
    markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    update.message.reply_text('You want your password for some service or no?', reply_markup=markup)
    return SAVING.ASK_HOW


def save_password_question_2(update: Update, context):
    answer = update.message.text
    if answer.lower() == 'yes':
        update.message.reply_text('Please give me name of service:')
        return SAVING.SERVICE
    else:
        update.message.reply_text('Please insert password:')
        return SAVING.PASSWORD


name_of_service = ''


def save_password_question_3(update: Update, context):
    global name_of_service
    name_of_service = update.message.text
    update.message.reply_text('Please insert password:')

    return SAVING.PASSWORD


def save_password_answer(update: Update, context):
    global name_of_service
    password = update.message.text
    ph.save_pass_to_csv(name_of_service, password)
    update.message.reply_text(f'Added password "{password}" with success', reply_markup=markup)
    name_of_service = ''
    return ConversationHandler.END


save_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('save', save_password_question_1)],
    states={
        SAVING.ASK_HOW: [
            MessageHandler(Filters.regex('^(YES|NO)$'), save_password_question_2)
        ],
        SAVING.SERVICE: [
            MessageHandler(Filters.text, save_password_question_3)
        ],
        SAVING.PASSWORD: [
            MessageHandler(Filters.text, save_password_answer)
        ]
    },
    fallbacks=[CommandHandler('save', save_password_question_1)]
)
