from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

from statements import UPDATE, SHOW_ALL
from conversations.basic_conver import markup, get_value
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

    return UPDATE.SERVICE


def update_password_question_3(update: Update, context):
    global name_of_service
    name_of_service = update.message.text
    update.message.reply_text('Please insert new password:')

    return UPDATE.UPDATE


def update_password_answer(update: Update, context):
    global name_of_service
    password = update.message.text
    ph.update_password_by_service(name_of_service, password)
    update.message.reply_text(f'Updated password "{password}" with success', reply_markup=markup)
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

