from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext,CallbackQueryHandler,ConversationHandler
import re
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
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup

os.environ['SSL_CERT_FILE'] = certifi.where()
cred_obj = firebase_admin.credentials.Certificate('c:/Users/ROG/Desktop/cloud computing/chatbot/7940.json')
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://project-699883704609295917-default-rtdb.firebaseio.com/',
    'storageBucket':'project-699883704609295917.appspot.com'
	})
db_ref = db.reference('/')
movie = db_ref.child('movie/').get()
movieset = []
for i in movie:
    movieset.append(i)
ADD = 0 
def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=('5624610325:AAF1Y0xRDCzscp7mHrLuPLQPGHWTbU8muYc'), use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    
    dispatcher.add_handler(CommandHandler("show", show))
    
    handler = ConversationHandler(
      entry_points=[CommandHandler("show", show),CallbackQueryHandler(keyboard_callback)],
      states={
            ADD: [MessageHandler(Filters.text,add)],
            
      },
      fallbacks=[CommandHandler('cancel', cancel)],
      )
    dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()

def add(update: Update, context: CallbackContext):
    print('yes')
    return ConversationHandler.END


def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!"
    )
    return ConversationHandler.END

def show(update: Update, context: CallbackContext) -> None:
    movieset
    keyboard = []
    for i in movieset:
        keyboard.append([InlineKeyboardButton(str(i), callback_data=str(i))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'What movie would you like to view?',reply_markup = reply_markup)
    return ADD
    

def keyboard_callback(update: Update, context: CallbackContext):
    query = update.callback_query 
    query.answer() 
    query.edit_message_text(text=f"Selected option: {query.data}")
    
    if query.data == 'movie':
        show(update,context)
    if query.data == 'add':
        query.edit_message_text(text="Enter your comment")
        return ADD
    elif re.match(r'[\w+\s+]+/review',query.data)!= None:
        review = db_ref.child('movie/'+ query.data ).get()
        for i in review.items():
            context.bot.send_message(chat_id=update.effective_chat.id,text = i[0]+':'+i[1])    
        keyboard = [[InlineKeyboardButton('Adding review', callback_data='add')],[InlineKeyboardButton('Back to movie list', callback_data='movie')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="Would you like to review?",reply_markup = reply_markup)

    elif re.match(r'[\w+\s+]+/likes',query.data)!= None:
        likes = db_ref.child('movie/'+ query.data ).get()
        db_ref.child('movie/'+ query.data ).set(int(likes)+1)
        keyboard = [[InlineKeyboardButton('Back to movie list', callback_data='movie')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text=f"There are now {likes} likes",reply_markup = reply_markup)
        
    else :
        keyboard = [[InlineKeyboardButton('View reviews', callback_data=query.data+'/review')],[InlineKeyboardButton('like', callback_data=query.data+'/likes')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text = 'What would you like to do',reply_markup = reply_markup)
    
    




if __name__ == '__main__':
    main()

