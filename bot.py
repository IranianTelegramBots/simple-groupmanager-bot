# -*- coding: utf-8 -*-
import simplejson as json 
import requests
import re
import telebot 
from telebot import types
import redis

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def GetChat(chat):
    url = 'https://api.telegram.org/bot' + str(API_TOKEN) + '/getChat?chat_id=' + str(chat)
    print url
    jstr = requests.get(url)
    jdat = json.loads(jstr.text)
    
    txt = '*GroupId:* ' + str(jdat['result']['id']) + '\n*GroupName:* ' + jdat['result']['title'] + '\n*GroupType:* _' + jdat['result']['type'] + '_' 
    return txt
       

@bot.callback_query_handler(func=lambda call: call.data == 'unban')
def uban(call):    
    t = r.get('user').replace("'","").replace("u","").replace("[","").replace("]","")
    bot.unban_chat_member(call.message.chat.id, t)
    markup = types.InlineKeyboardMarkup()
    item_text = types.InlineKeyboardButton('Ban user', callback_data="ban")
    markup.row(item_text)
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'ban')
def ban(call):    
    t = r.get('user').replace("'","").replace("u","").replace("[","").replace("]","")
    bot.kick_chat_member(call.message.chat.id, t)
    markup = types.InlineKeyboardMarkup()
    item_text = types.InlineKeyboardButton('Unban user', callback_data="unban")
    markup.row(item_text)
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,reply_markup=markup)

@bot.message_handler(commands=['ban'])
def ban(message):
  
     if not message.reply_to_message:
        text = message.text.split(' ')[1:]
        bot.kick_chat_member(message.chat.id,text)
        r.set('user', text)
        markup = types.InlineKeyboardMarkup()
        item_text = types.InlineKeyboardButton('Unban user', callback_data="unban")
        markup.row(item_text)
        bot.send_message(message.chat.id,'User was kicked',reply_markup=markup)
     
     if message.reply_to_message:
        text = message.reply_to_message.from_user.id
        r.set('user', text)
        markup = types.InlineKeyboardMarkup()
        item_text = types.InlineKeyboardButton('Unban user', callback_data="unban")
        markup.row(item_text)
        bot.kick_chat_member(message.chat.id,text)
        bot.send_message(message.chat.id,'User was kicked',reply_markup=markup)

@bot.message_handler(commands=['info'])
def send_info(message):

     
     if message.reply_to_message:
        t = str(message.reply_to_message.from_user.id) + '\n' + message.reply_to_message.from_user.first_name
        if message.reply_to_message.from_user.username:
           username = '@' + message.reply_to_message.from_user.username
        else:
           username = ''
        t += '\n' + username 
        bot.send_message(message.chat.id,t)   
      
     if not message.reply_to_message: 
        t = GetChat(message.chat.id)
        bot.send_message(message.chat.id,t,parse_mode="Markdown") 
         
             
bot.polling(none_stop=True, interval=0)



