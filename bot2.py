import telebot
from telebot import types


TOKEN = '7506077102:AAEOyherkIla8l4W9F_SUE0OhpccwpaaoJ4'
bot = telebot.TeleBot(TOKEN)

@bot.message.handler(commands=['start'])
def start_cfg(message):
    

bot.infinity_polling()