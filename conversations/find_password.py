from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import passwords_handlers as ph
from conversations.basic_conver import basic_markup, get_value
from statements import FIND


def find_password_question1(update: Update, context):
    update.message.reply_text('Please enter the name of service:', reply_markup=ReplyKeyboardRemove())
    return FIND.FIND


def find_password_answer(update: Update, context):
    answer = update.message.text
    records = ph.find_password_by_service_name(answer, id_user=update.message.from_user.id)

    if len(records) == 1:
        password = records[0][2]
        button = [
            [
                InlineKeyboardButton("Update🔄", callback_data=FIND.UPDATE.value + records[0][1]),
                InlineKeyboardButton("Delete❌", callback_data=FIND.DELETE.value + records[0][1])
            ]
        ]
        reply_markup = InlineKeyboardMarkup(button)
        update.message.reply_text('Here is your password:')
        update.message.reply_text(password, reply_markup=reply_markup)

        return FIND.FIND
    elif len(records) > 1:
        update.message.reply_text('There are several same service:')
        for password in records:
            button = [
                [
                    InlineKeyboardButton("Get pass🔐", callback_data=FIND.GET.value + password[2])
                ],
                [
                    InlineKeyboardButton("Update🔄", callback_data=FIND.UPDATE.value + password[1]),
                    InlineKeyboardButton("Delete❌", callback_data=FIND.DELETE.value + password[1])
                ]
            ]
            reply_markup = InlineKeyboardMarkup(button)
            update.message.reply_text(password[1], reply_markup=reply_markup)
        return FIND.FIND
    elif len(records) == 0:
        update.message.reply_text('No passwords for this service found!', reply_markup=basic_markup)
    return ConversationHandler.END


def update_password(update: Update, context):
    return update.callback_query.data


def delete_password(update: Update, context):
    return update.callback_query.data


def get_password(update: Update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text(get_value(query.data))

    return FIND.FIND

find_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('find', find_password_question1)],
    states={
        FIND.FIND: [
            MessageHandler(Filters.text, find_password_answer),
            CallbackQueryHandler(update_password, pattern='^' + FIND.UPDATE.value),
            CallbackQueryHandler(delete_password, pattern='^' + FIND.DELETE.value),
            CallbackQueryHandler(get_password, pattern='^' + FIND.GET.value),
        ]
    },
    fallbacks=[CommandHandler('find', find_password_question1)]
)
