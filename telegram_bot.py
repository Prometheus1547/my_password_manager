import logging

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import Updater, Filters, CallbackContext

import passwords_handlers as ph
from statements import GENERATE, SAVING

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = '1656054388:AAEfmVAqRehKc4-7hvU2yDb6w54ChS0aVEE'

replay_keyboard = [
    ['/generate', '/save'],
    ['/find', '/show_list']
]
markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=False)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome!', reply_markup=markup)


def generate_password_question(update: Update, context: CallbackContext):
    replay_keyboard = [
        ['YES', 'NO']
    ]
    markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    update.message.reply_text('You want your password for some service or no?', reply_markup=markup)
    return GENERATE.ASK_HOW


def generate_password_question2(update: Update, context):
    answer = update.message.text
    if answer.lower() == 'yes':
        update.message.reply_text('Please give me name of service:')
        return GENERATE.SERVICE
    else:
        password = ph.generate_password()
        update.message.reply_text('Your generated password is:')
        update.message.reply_text(password, reply_markup=markup)

        return ConversationHandler.END


def generate_password_answer1(update: Update, context):
    name_of_service = update.message.text
    password = ph.generate_password(name=name_of_service)
    update.message.reply_text('Your generated password for service ' + name_of_service + ' is:')
    update.message.reply_text(password, reply_markup=markup)

    return ConversationHandler.END


def show_all_passwords(update: Update, context):
    passwords = ph.read_all_passwords()
    if len(passwords) > 0:
        update.message.reply_text('List of passwords:')
        for password in passwords:
            button = [[InlineKeyboardButton("Get pass", callback_data=password[1])]]
            reply_markup = InlineKeyboardMarkup(button)
            update.message.reply_text(password, reply_markup=reply_markup)
    else:
        update.message.reply_text('There is no any passwords!')


def get_password_from_button(update: Update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text(query.data)

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


def main():
    updater = Updater(token=TOKEN, use_context=True)

    generate_pass_conv = ConversationHandler(
        entry_points=[CommandHandler('generate', generate_password_question)],
        states={
            GENERATE.ASK_HOW: [
                MessageHandler(Filters.regex('^(YES|NO)$'), generate_password_question2)
            ],
            GENERATE.SERVICE: [
                MessageHandler(Filters.text, generate_password_answer1)
            ]
        },
        fallbacks=[CommandHandler('generate', generate_password_question)]
    )

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

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('show_list', show_all_passwords))
    updater.dispatcher.add_handler(generate_pass_conv)
    updater.dispatcher.add_handler(save_pass_conv)
    updater.dispatcher.add_handler(CallbackQueryHandler(get_password_from_button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
