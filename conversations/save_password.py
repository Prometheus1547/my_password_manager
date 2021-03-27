from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
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
        update.message.reply_text('Please insert password:', reply_markup=ReplyKeyboardRemove())
        return SAVING.PASSWORD
    else:
        replay_keyboard = [
            ['YES✅', 'NO❌']
        ]
        markup_generate = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
        update.message.reply_text('Looks like  password for this service already exists! Create it anyway?',
                                  reply_markup=markup_generate)
        return SAVING.CREATE_ANYWAY


def save_password_answer(update: Update, context):
    global name_of_service
    password = update.message.text
    ph.save_pass_to_csv(name_of_service, password, id_user=update.message.from_user.id)
    update.message.reply_text(f'Added password "{password}" with success', reply_markup=basic_markup)
    name_of_service = ''
    return ConversationHandler.END


def save_password_answer2(update: Update, context):
    global name_of_service
    answer = update.message.text
    if answer.lower() == 'yes' or answer == 'YES✅':
        update.message.reply_text('Please insert password:', reply_markup=ReplyKeyboardRemove())
        return SAVING.PASSWORD
    else:
        update.message.reply_text('Got it.', reply_markup=basic_markup)
        return ConversationHandler.END


save_pass_conv = ConversationHandler(
    entry_points=[CommandHandler('save', save_password_question_2)],
    states={
        SAVING.SERVICE: [
            MessageHandler(Filters.text, save_password_question_3)
        ],
        SAVING.PASSWORD: [
            MessageHandler(Filters.text, save_password_answer)
        ],
        SAVING.CREATE_ANYWAY: [
            MessageHandler(Filters.text, save_password_answer2)
        ]
    },
    fallbacks=[CommandHandler('save', save_password_question_2)]
)
