import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler
from telegram.ext import Updater, Filters, CallbackContext

import passwords_handlers as ph

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = '1656054388:AAEfmVAqRehKc4-7hvU2yDb6w54ChS0aVEE'

ASK_HOW, SERVICE, BASIC = range(3)

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
    return ASK_HOW


def generate_password_question2(update: Update, context):
    answer = update.message.text
    if answer.lower() == 'yes':
        update.message.reply_text('Please give me name of service:')
        return SERVICE
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
    update.message.reply_text('List of passwords:')
    update.message.reply_text(ph.get_passwords())

def main():
    updater = Updater(token=TOKEN, use_context=True)
    generate_pass_conv = ConversationHandler(
        entry_points=[CommandHandler('generate', generate_password_question)],
        states={
            ASK_HOW: [
                MessageHandler(Filters.regex('^(YES|NO)$'), generate_password_question2)
            ],
            SERVICE: [
                MessageHandler(Filters.text, generate_password_answer1)
            ],
            BASIC: [
                CommandHandler('start', start)
            ]
        },
        fallbacks=[CommandHandler('generate', generate_password_question)]
    )

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('show_list', show_all_passwords))
    updater.dispatcher.add_handler(generate_pass_conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
