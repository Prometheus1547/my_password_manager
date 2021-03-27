from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

from statements import DELETE, SHOW_ALL
from conversations.basic_conver import markup, get_value
import passwords_handlers as ph

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
        update.message.reply_text(f'Deleted password "{answer}" with success', reply_markup=markup)
        name_of_service = ''
        return ConversationHandler.END
    else:
        update.message.reply_text('Got it.', reply_markup=markup)
        name_of_service = ''
        return ConversationHandler.END

def stop_deleting(update, context):
    return ConversationHandler.END

delete_pass_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(delete_password_from_inline_button, pattern='^' + SHOW_ALL.DELETE.value)],
    states={
        DELETE.DELETE: [
            MessageHandler(Filters.text, delete_password_answer)
        ]
    },
    fallbacks=[CommandHandler('stop_delete', stop_deleting)]
)
