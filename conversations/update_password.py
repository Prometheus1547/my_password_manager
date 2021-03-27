from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

import passwords_handlers as ph
from conversations.basic_conver import basic_markup, get_values
from statements import UPDATE, SHOW_ALL, FIND

name_of_service = ''
pass_id = ''


def update_password_question_1(update: Update, context):
    update.message.reply_text('Please enter the name of service:', reply_markup=ReplyKeyboardRemove())
    return UPDATE.SERVICE


def update_password_from_inline_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    global name_of_service, pass_id
    name_of_service = get_values(query.data)[0]
    pass_id = get_values(query.data)[1]
    query.message.reply_text(f'Please insert new password for "{name_of_service}":', reply_markup=ReplyKeyboardRemove())

    return UPDATE.UPDATE


def update_password_question_3(update: Update, context):
    global name_of_service
    name_of_service = update.message.text
    update.message.reply_text(f'Please insert new password for "{name_of_service}":',
                              reply_markup=ReplyKeyboardRemove())

    return UPDATE.UPDATE


def update_password_answer(update: Update, context):
    global name_of_service, pass_id
    password = update.message.text
    ph.update_password_by_id(pass_id, password, id_user=update.message.from_user.id)
    update.message.reply_text(f'Updated password "{password}" for service "{name_of_service} "with success',
                              reply_markup=basic_markup)
    name_of_service = ''
    pass_id = ''
    return ConversationHandler.END


update_pass_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(update_password_from_inline_button,
                                       pattern=f"^({SHOW_ALL.UPDATE.value}.*|{FIND.UPDATE.value}.*)"),
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
