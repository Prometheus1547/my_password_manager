from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

from statements import UPDATE, SHOW_ALL
from conversations.basic_conver import basic_markup, get_value
import passwords_handlers as ph

name_of_service = ''


def update_password_question_1(update: Update, context):
    update.message.reply_text('Please enter the name of service:', reply_markup=ReplyKeyboardRemove())
    return UPDATE.SERVICE


def update_password_from_inline_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    global name_of_service
    name_of_service = get_value(query.data)
    query.message.reply_text(f'Please insert new password for "{name_of_service}":', reply_markup=ReplyKeyboardRemove())

    return UPDATE.UPDATE


def update_password_question_3(update: Update, context):
    global name_of_service
    name_of_service = update.message.text
    update.message.reply_text(f'Please insert new password for "{name_of_service}":', reply_markup=ReplyKeyboardRemove())

    return UPDATE.UPDATE


def update_password_answer(update: Update, context):
    global name_of_service
    password = update.message.text
    ph.update_password_by_service(name_of_service, password)
    update.message.reply_text(f'Updated password "{password}" for service "{name_of_service} "with success', reply_markup=basic_markup)
    name_of_service = ''
    return ConversationHandler.END


update_pass_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(update_password_from_inline_button, pattern='^' + SHOW_ALL.UPDATE.value),
                  CommandHandler('update', update_password_question_1)],
    states={
        UPDATE.SERVICE: [
            MessageHandler(Filters.text, update_password_question_3)
        ],
        UPDATE.UPDATE: [
            MessageHandler(Filters.text, update_password_answer)
        ]
    },
    fallbacks=[CommandHandler('update', update_password_question_1)]
)

