from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

import passwords_handlers as ph
from conversations.basic_conver import basic_markup
from statements import SAVING


def save_password_question_2(update: Update, context):
    update.message.reply_text('Please give me name of service:')
    return SAVING.SERVICE


name_of_service = ''


def save_password_question_3(update: Update, context):
    global name_of_service
    name_of_service = update.message.text
    if ph.check_password(service_name=name_of_service, id_user=update.message.from_user.id):
        update.message.reply_text('Please insert password:')
        return SAVING.PASSWORD
    else:
        update.message.reply_text('Password for this service already exists!', reply_markup=basic_markup)
        return ConversationHandler.END


def save_password_answer(update: Update, context):
    global name_of_service
    password = update.message.text
    ph.save_pass_to_csv(name_of_service, password, id_user=update.message.from_user.id)
    update.message.reply_text(f'Added password "{password}" with success', reply_markup=basic_markup)
    name_of_service = ''
    return ConversationHandler.END


save_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('save', save_password_question_2)],
    states={
        SAVING.SERVICE: [
            MessageHandler(Filters.text, save_password_question_3)
        ],
        SAVING.PASSWORD: [
            MessageHandler(Filters.text, save_password_answer)
        ]
    },
    fallbacks=[CommandHandler('save', save_password_question_2)]
)
