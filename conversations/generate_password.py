from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext

import passwords_handlers as ph
from conversations.basic_conver import basic_markup
from statements import GENERATE


def generate_password_question(update: Update, context: CallbackContext):
    replay_keyboard = [
        ['All Symbols', 'Only digits']
    ]
    markup = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    update.message.reply_text('What symbols use in password?', reply_markup=markup)
    return GENERATE.ASK_HOW


symbols = ''
length = 12


def generate_password_question2(update: Update, context):
    answer = update.message.text
    global symbols
    if answer.lower() == 'all symbols':
        symbols = ph.chars
        update.message.reply_text('Please give me name of service:')
        return GENERATE.SERVICE
    else:
        symbols = ph.digits
        update.message.reply_text('Please insert length of password:')
        return GENERATE.ASK_HOW_LONG


def generate_password_question_2_1(update: Update, context):
    answer = int(update.message.text)
    global length
    length = answer
    update.message.reply_text('Please give me name of service:')
    return GENERATE.SERVICE


def generate_password_answer1(update: Update, context):
    name_of_service = update.message.text
    global length
    if ph.check_password(name_of_service, id_user=update.message.from_user.id):
        password = ph.generate_password(service_name=name_of_service, id_user=update.message.from_user.id, symbols=symbols, length=length)
        update.message.reply_text('Your generated password for service ' + name_of_service + ' is:')
        update.message.reply_text(password, reply_markup=basic_markup)
    else:
        update.message.reply_text('Looks like something get wrong! Maybe password for this service already exists',
                                  reply_markup=basic_markup)
    length = 12
    return ConversationHandler.END


generate_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('generate', generate_password_question)],
    states={
        GENERATE.ASK_HOW: [
            MessageHandler(Filters.regex('^(All Symbols|Only digits)$'), generate_password_question2)
        ],
        GENERATE.ASK_HOW_LONG: [
            MessageHandler(Filters.regex('^\d+$'), generate_password_question_2_1)
        ],
        GENERATE.SERVICE: [
            MessageHandler(Filters.text, generate_password_answer1)
        ]
    },
    fallbacks=[CommandHandler('generate', generate_password_question)]
)
