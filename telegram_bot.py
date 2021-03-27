import logging
import os
from pathlib import Path

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import Updater, Filters, CallbackContext
from telegram.utils.types import FileInput

from configs import API_TOKEN
from conversations.basic_conver import basic_markup
from conversations.delete_password import delete_pass_conv
from conversations.generate_password import generate_pass_conv
from conversations.save_password import save_pass_conv
from conversations.find_password import find_pass_conv
from conversations.list_passwords import list_passwords_conv
from conversations.update_password import update_pass_conv, update_password_from_inline_button

from passwords_handlers import get_file_name


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome!', reply_markup=basic_markup)


def backup_passwords(update: Update, context):
    path = get_file_name(update.message.from_user.id)
    if os.path.exists(path):
        with open(path, 'rb') as file:
            update.message.reply_text('Here are your passwords:')
            update.message.reply_document(document=file, filename='passwords.csv')
    else:
        update.message.reply_text('We do not have any passwords for you.')


def main():
    updater = Updater(token=API_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('backup', backup_passwords))

    updater.dispatcher.add_handler(generate_pass_conv)
    updater.dispatcher.add_handler(save_pass_conv)
    updater.dispatcher.add_handler(find_pass_conv)
    updater.dispatcher.add_handler(list_passwords_conv)
    updater.dispatcher.add_handler(update_pass_conv)
    updater.dispatcher.add_handler(delete_pass_conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
