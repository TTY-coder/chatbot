from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext
import configparser
import logging
import redis
import os
import datetime
import os
import random

import certifi
import firebase_admin
from firebase_admin import db

os.environ['SSL_CERT_FILE'] = certifi.where()
cred_obj = firebase_admin.credentials.Certificate('c:/Users/ROG/Desktop/cloud computing/chatbot/7940.json')
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://project-699883704609295917-default-rtdb.firebaseio.com/',
    'storageBucket':'project-699883704609295917.appspot.com'
	})
db_ref = db.reference('/')
print(db_ref)

def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=('5624610325:AAF1Y0xRDCzscp7mHrLuPLQPGHWTbU8muYc'), use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("help", help_command))
    

    updater.start_polling()
    updater.idle()
    os.environ['SSL_CERT_FILE'] = certifi.where()
    cred_obj = firebase_admin.credentials.Certificate('c:/Users/ROG/Desktop/cloud computing/chatbot/7940.json')
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL':'https://project-699883704609295917-default-rtdb.firebaseio.com/',
        'storageBucket':'project-699883704609295917.appspot.com'
        })
    db_ref = db.reference('/')
    print(db_ref)

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' +
        redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('Good day,  ' + msg + '！ ')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')



if __name__ == '__main__':
    main()


