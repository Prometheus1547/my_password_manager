from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext

from conversations.basic_conver import markup
import passwords_handlers as ph
from statements import GENERATE


def generate_password_question(update: Update, context: CallbackContext):
    replay_keyboard = [
        ['YES', 'NO']
    ]
    markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    update.message.reply_text('You want your password for some service or no?', reply_markup=markup)
    return GENERATE.ASK_HOW


def generate_password_question2(update: Update, context):
    answer = update.message.text
    if answer.lower() == 'yes':
        update.message.reply_text('Please give me name of service:')
        return GENERATE.SERVICE
    else:
        password = ph.generate_password()
        update.message.reply_text('Your generated password is:')
        update.message.reply_text(password, reply_markup=markup)

        return ConversationHandler.END


def generate_password_answer1(update: Update, context):
    name_of_service = update.message.text
    if ph.check_password(name_of_service):
        password = ph.generate_password(service_name=name_of_service)
        update.message.reply_text('Your generated password for service ' + name_of_service + ' is:')
        update.message.reply_text(password, reply_markup=markup)
    else:
        update.message.reply_text('Looks like something get wrong! Maybe password for this service already exists',
                                  reply_markup=markup)

    return ConversationHandler.END


generate_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('generate', generate_password_question)],
    states={
        GENERATE.ASK_HOW: [
            MessageHandler(Filters.regex('^(YES|NO)$'), generate_password_question2)
        ],
        GENERATE.SERVICE: [
            MessageHandler(Filters.text, generate_password_answer1)
        ]
    },
    fallbacks=[CommandHandler('generate', generate_password_question)]
)
