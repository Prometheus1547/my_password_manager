from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext

import passwords_handlers as ph
from conversations.basic_conver import basic_markup, get_value, get_values
from statements import DELETE, SHOW_ALL, FIND

name_of_service = ''
pass_id = ''


def delete_password_from_inline_button(delete: Update, context: CallbackContext):
    query = delete.callback_query
    query.answer()
    global name_of_service, pass_id
    name_of_service = get_values(query.data)[0]
    pass_id = get_values(query.data)[1]

    replay_keyboard = [
        ['YES✅', 'NO❌']
    ]
    markup_delete = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    query.message.reply_text('Are you sure?', reply_markup=markup_delete)

    return DELETE.DELETE


def delete_password_answer(update: Update, context):
    global name_of_service, pass_id
    answer = update.message.text
    if answer.lower() == 'yes' or answer == 'YES✅':
        ph.delete_password_by_id(pass_id, id_user=update.message.from_user.id)
        update.message.reply_text(f'Deleted password for "{name_of_service}" with success', reply_markup=basic_markup)
        name_of_service = ''
        pass_id = ''
        return ConversationHandler.END
    else:
        update.message.reply_text('Got it.', reply_markup=basic_markup)
        name_of_service = ''
        pass_id = ''
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
