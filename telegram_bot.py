import logging

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import Updater, Filters, CallbackContext

from conversations.basic_conver import markup
from conversations.generate_password import generate_pass_conv
from conversations.save_password import save_pass_conv
from conversations.find_password import find_pass_conv

import passwords_handlers as ph
from statements import GENERATE, SAVING

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = '1656054388:AAEfmVAqRehKc4-7hvU2yDb6w54ChS0aVEE'


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome!', reply_markup=markup)


def show_all_passwords(update: Update, context):
    passwords = ph.read_all_passwords()
    if len(passwords) > 0:
        update.message.reply_text('List of passwords:')
        for password in passwords:
            button = [[InlineKeyboardButton("Get pass", callback_data=password[2])]]
            reply_markup = InlineKeyboardMarkup(button)
            update.message.reply_text(password[1], reply_markup=reply_markup)
    else:
        update.message.reply_text('There is no any passwords!')


def get_password_from_button(update: Update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text(query.data)


def main():
    updater = Updater(token=TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('show_list', show_all_passwords))

    updater.dispatcher.add_handler(generate_pass_conv)
    updater.dispatcher.add_handler(save_pass_conv)
    updater.dispatcher.add_handler(find_pass_conv)

    updater.dispatcher.add_handler(CallbackQueryHandler(get_password_from_button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
