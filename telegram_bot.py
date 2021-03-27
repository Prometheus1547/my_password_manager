import logging

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import Updater, Filters, CallbackContext

from conversations.basic_conver import markup
from conversations.delete_password import delete_pass_conv
from conversations.generate_password import generate_pass_conv
from conversations.save_password import save_pass_conv
from conversations.find_password import find_pass_conv
from conversations.list_passwords import list_passwords_conv
from conversations.update_password import update_pass_conv, update_password_from_inline_button

import passwords_handlers as ph
from statements import GENERATE, SAVING, SHOW_ALL

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = '1656054388:AAEfmVAqRehKc4-7hvU2yDb6w54ChS0aVEE'


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome!', reply_markup=markup)




def main():
    updater = Updater(token=TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

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
