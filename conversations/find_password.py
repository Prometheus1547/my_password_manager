from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from statements import FIND
from conversations.basic_conver import markup
import passwords_handlers as ph

def find_password_question1(update: Update, context):

    update.message.reply_text('Please enter the name of service:', reply_markup=ReplyKeyboardRemove())
    return FIND.FIND


def find_password_answer(update: Update, context):
    answer = update.message.text
    password = ph.find_password_by_service_name(answer)[2]
    if len(password) > 0:
        update.message.reply_text('Here is your password:', reply_markup=markup)
        update.message.reply_text(password)
    else:
        update.message.reply_text('No passwords for this service found!', reply_markup=markup)
    return ConversationHandler.END



find_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('find', find_password_question1)],
    states={
        FIND.FIND: [
            MessageHandler(Filters.text, find_password_answer)
        ]
    },
    fallbacks=[CommandHandler('find', find_password_question1)]
)
