from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, \
    Filters

from conversations.update_password import update_pass_conv
from statements import SHOW_ALL, UPDATE

import passwords_handlers as ph
from conversations.basic_conver import get_value


def show_all_passwords(update: Update, context):
    passwords = ph.read_all_passwords()
    if len(passwords) > 0:
        update.message.reply_text('List of passwords:')
        for password in passwords:
            button = [
                [
                    InlineKeyboardButton("Get pass", callback_data=SHOW_ALL.GET.value + password[2])
                ],
                [
                    InlineKeyboardButton("Update", callback_data=SHOW_ALL.UPDATE.value + password[1]),
                    InlineKeyboardButton("Delete", callback_data=password[1])
                ]
            ]
            reply_markup = InlineKeyboardMarkup(button)
            update.message.reply_text(password[1], reply_markup=reply_markup)
    else:
        update.message.reply_text('There is no any passwords!')

    return SHOW_ALL.INIT


def get_password_from_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.reply_text(get_value(query.data))

    return SHOW_ALL.INIT


def update_password_from_button(update: Update, context):

    return update.callback_query.data


list_passwords_conv = ConversationHandler(
    entry_points=[CommandHandler('show_list', show_all_passwords)],
    states={
        SHOW_ALL.INIT: [
            CallbackQueryHandler(get_password_from_button, pattern='^' + SHOW_ALL.GET.value),
            CallbackQueryHandler(update_password_from_button, pattern='^' + SHOW_ALL.UPDATE.value)
        ]
    },
    fallbacks=[CommandHandler('show_list', show_all_passwords)]
)
