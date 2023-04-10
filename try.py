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
LIKE = 1
REVIEW = 2
CONFIRM = 4
CANCEL = 5
def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=('5624610325:AAF1Y0xRDCzscp7mHrLuPLQPGHWTbU8muYc'), use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


    handler = ConversationHandler(
      entry_points=[CommandHandler("show", show),CallbackQueryHandler(keyboard_callback)],
      states={
			
            ADD: [CallbackQueryHandler(add)],
            LIKE:[CallbackQueryHandler(like)],
            CANCEL:[CallbackQueryHandler(cancel)],
            REVIEW:[CallbackQueryHandler(review)],
            CONFIRM:[MessageHandler(Filters.text & (~Filters.command), get_message),CallbackQueryHandler(confirm)],
      },
      fallbacks=[CommandHandler('cancel', cancel)],
      )
    dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()

def show(update: Update, context: CallbackContext) -> None:
    movieset
    keyboard = []
    for i in movieset:
        keyboard.append([InlineKeyboardButton(str(i), callback_data=str(i))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'What movie would you like to view?',reply_markup = reply_markup)

def keyboard_callback(update: Update, context: CallbackContext):
    query = update.callback_query 
    query.answer() 
    context.user_data['movie'] = query.data
    query.edit_message_text(text=f"Selected option: {context.user_data['movie']}")
    keyboard = [[InlineKeyboardButton('View reviews', callback_data='review')],[InlineKeyboardButton('like',callback_data='like')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,text = 'What would you like to do',reply_markup = reply_markup)
    return ADD

def add(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    if query.data == 'like':
        return LIKE
    elif query.data == 'review':
        return REVIEW
    else:
    	return ConversationHandler.END

def like (update: Update, context: CallbackContext):
    likes = db_ref.child('movie/'+ context.user_data['movie']+'/likes' ).get()
    db_ref.child('movie/'+ context.user_data['movie']+'/likes' ).set(int(likes)+1)
    keyboard = [[InlineKeyboardButton('Back to movie list', callback_data='movie')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,text=f"There are now {likes} likes",reply_markup = reply_markup)
    return CANCEL

def review (update: Update, context: CallbackContext):
    mname = context.user_data['movie']
    
    review = db_ref.child('movie/'+mname+'/review' ).get()
    for i in review.items():
        context.bot.send_message(chat_id=update.effective_chat.id,text = i[0]+':'+i[1])    		
    keyboard = [[InlineKeyboardButton('confirm', callback_data='confirm')],[InlineKeyboardButton('cancel', callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)   
    context.bot.send_message(chat_id=update.effective_chat.id,text="Type out your review and click confirm",reply_markup = reply_markup)
    return CONFIRM

def get_message(update: Update, context: CallbackContext):
    content =  update.message.text
    context.user_data['review'] = content
    

def confirm (update: Update, context: CallbackContext):  
    try:
        query = update.callback_query
        query.answer()
        if query.data == 'confirm':
            first_name = update.effective_chat.first_name
            last_name = update.effective_chat.last_name
            full_name = first_name+' '+last_name
            mname = context.user_data['movie']
            content = context.user_data['review']
            logging.info("Update: " + str(update))
            logging.info("context: " + str(context))
            db_ref.child('movie/'+mname+'/review/'+full_name ).set(content)
            return CANCEL
        if query.data == 'cancel':
            return CANCEL
    except (IndexError, ValueError):
        update.message.reply_text('please enter something')
        
    




def cancel(update: Update, context: CallbackContext):
    # get the user's first name
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    context.bot.send_message(chat_id=update.effective_chat.id,text = f"Okay, no question for you then, take care, {first_name}{last_name}!")
    return ConversationHandler.END

   

if __name__ == '__main__':
    main()

