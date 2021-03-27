from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

import passwords_handlers as ph
from conversations.basic_conver import basic_markup, get_value
from statements import DELETE, SHOW_ALL, FIND

name_of_service = ''


def delete_password_from_inline_button(delete: Update, context: CallbackContext):
    query = delete.callback_query
    query.answer()
    global name_of_service
    name_of_service = get_value(query.data)

    replay_keyboard = [
        ['YES', 'NO']
    ]
    markup_delete = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    query.message.reply_text('Are you sure?', reply_markup=markup_delete)

    return DELETE.DELETE


def delete_password_answer(update: Update, context):
    global name_of_service
    answer = update.message.text
    if answer.lower() == 'yes':
        ph.delete_password_by_service(name_of_service)
        update.message.reply_text(f'Deleted password for "{name_of_service}" with success', reply_markup=basic_markup)
        name_of_service = ''
        return ConversationHandler.END
    else:
        update.message.reply_text('Got it.', reply_markup=basic_markup)
        name_of_service = ''
        return ConversationHandler.END


def stop_deleting(update, context):
    return ConversationHandler.END


delete_pass_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(delete_password_from_inline_button,
                                       pattern=f"^({SHOW_ALL.DELETE.value}.*|{FIND.DELETE.value}.*)")],
    states={
        DELETE.DELETE: [
            MessageHandler(Filters.text, delete_password_answer)
        ]
    },
    fallbacks=[CommandHandler('stop_delete', stop_deleting)]
)
