import telebot
from telebot import types


TOKEN = '7506077102:AAEOyherkIla8l4W9F_SUE0OhpccwpaaoJ4'
bot = telebot.TeleBot(TOKEN)


waiting_for_resume = {}
resume_submitters = {}
waiting_for_technical_task={}
technical_task_submitters={}
authorized_users=[1098482972]


@bot.message.handler(commands=['start'])
def start_cfg(message):
    if "sendactions" in message.text:
        send_actions_menu1(message.chat.id)
    elif message.chat.id in authorized_users:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('Разработчикам', callback_data='developer')
        markup.add(bt1)
        markup.add(types.InlineKeyboardButton('Заказчикам', callback_data='customer'))
        bot.reply_to(message, 'Выберите предпочитаемое действие:', reply_markup=markup)
        


bot.infinity_polling()