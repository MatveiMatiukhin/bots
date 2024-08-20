import telebot
from telebot import types
import logging
import webbrowser


TOKEN = '7506077102:AAEOyherkIla8l4W9F_SUE0OhpccwpaaoJ4'
bot = telebot.TeleBot(TOKEN)


logging.basicConfig(level=logging.INFO)


waiting_for_resume = {}
resume_submitters = {}
waiting_for_technical_task={}
technical_task_submitters={}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Проверка параметров, переданных в URL
    if "sendactions" in message.text:
        send_actions_menu1(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('Разработчикам', callback_data='developer')
        markup.add(bt1)
        markup.add(types.InlineKeyboardButton('Заказчикам', callback_data='customer'))
        bot.reply_to(message, 'Выберите предпочитаемое действие:', reply_markup=markup)
    
    
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'В команде /info, отображается информауия по работе с ботом \nКоманда /start выводит кнопки для начала действия бота \nКоманда /id выводит id аользователя \nКоманда /legend выводит аккаунт создателя бота')


@bot.message_handler(commands=['id'])
def send_id(message):
    bot.send_message(message.chat.id, F'Ваш ID {message.from_user.id}')
    print(message.chat.id)
    bot.send_message(message.chat.id, message.chat.id)
    
 

@bot.message_handler(commands=['legend'])
def send_legend(message):
    bot.send_message(message.chat.id, 'Ходит легенда о воине сделавшем этого бота \n@biznesmanil - его имя')


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, 'Информация по работе с ботом')
    
    
@bot.message_handler(func=lambda message: message.chat.id in waiting_for_resume and waiting_for_resume[message.chat.id])
def handle_resume(message):
    submitter_id = message.from_user.id
    developer_chat_id = 1098482972 # ID разработчика (здесь укажите ваш ID)
    resume_submitters[message.chat.id] = submitter_id

    markup = types.InlineKeyboardMarkup()
    bt9 = types.InlineKeyboardButton('Approve', callback_data=f'approve_{message.chat.id}')
    bt10 = types.InlineKeyboardButton('Reject', callback_data=f'reject_{message.chat.id}')
    markup.add(bt9, bt10)

    try:
        if message.content_type == 'text':
            bot.send_message(developer_chat_id, f"Резюме от пользователя (@{message.from_user.username}):\n{message.text}", reply_markup=markup)
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке резюме: {str(e)}")
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке резюме: {str(e)}")

    del waiting_for_resume[message.chat.id]
    bot.send_message(message.chat.id, "Ваше резюме было успешно отправлено разработчику! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")


@bot.message_handler(func=lambda message: message.chat.id in waiting_for_technical_task and waiting_for_technical_task[message.chat.id])
def handle_technical_task(message):
    submitter_id = message.from_user.id
    chanel_chat_id = -1002212279206 # ID тгк (здесь укажите ваш ID)
    technical_task_submitters[message.chat.id] = submitter_id

    markup = types.InlineKeyboardMarkup()
    bt20 = types.InlineKeyboardButton('Approve1', callback_data=f'approve1_{message.chat.id}')
    bt21 = types.InlineKeyboardButton('Reject', callback_data=f'reject1_{message.chat.id}')
    markup.add(bt20, bt21)

    try:
        if message.content_type == 'text':
            bot.send_message(chanel_chat_id, f"Техническое задание от пользователя (@{message.from_user.username}):\n{message.text}", reply_markup=markup)
    except Exception as e: 
        logging.error(f"Произошла ошибка при отправке резюме: {str(e)}")
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке резюме: {str(e)}")

    del waiting_for_technical_task[message.chat.id]
    bot.send_message(message.chat.id, "Ваше техническое задание было успешно отправлено в тгк! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")
    

@bot.message_handler(content_types=['photo'])
def send_photo_0(message):
    if message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id]:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return

    photo_id = None
    try:
        photo_id = message.photo[-1].file_id
        developer_chat_id =  1098482972 # ID разработчика (здесь укажите ваш ID)
        
        bot.send_photo(developer_chat_id, photo_id, caption=f"Незаконченное резюме от пользователя (@{message.from_user.username})(фото)")
        bot.send_message(message.chat.id, "Ваше фото было успешно отправлено разработчику.")
    except Exception as e:
        # Обработка ошибки
        if photo_id is None:
            bot.send_message(message.chat.id, "Не удалось получить идентификатор фото.")
        else:
            bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {str(e)}")
            
            
@bot.message_handler(content_types=['document'])
def send_document_0(message):
    if message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id]:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return
    developer_chat_id =  1098482972 # ID разработчика (здесь укажите ваш ID)
    bot.send_document(developer_chat_id, message.document.file_id, caption=f"Незаконченное резюме от пользователя (@{message.from_user.username})(документ)")
    bot.send_message(message.chat.id, "Ваш документ был успешно отправлен разработчику.")
    
    
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    
    chat_id = callback.message.chat.id

    if callback.data == 'developer':
        send_actions_menu1(chat_id)
    elif callback.data == 'customer':
        send_actions_menu2(chat_id)
    elif callback.data == 'add_resume':
        waiting_for_resume[chat_id] = True
        bot.send_message(chat_id, 'Пожалуйста, отправьте ваше резюме. Если есть какие-либо файлы, отправьте их вместе с текстом отдельным сообщением.')
    elif callback.data.startswith('approve_'):
        resume_chat_id = callback.data.split('_')[1]
        submitter_id = resume_submitters.get(int(resume_chat_id))
        if submitter_id:
            resume_approved(submitter_id)
            bot.send_message(chat_id, 'Резюме одобрено и отправлено пользователю.')
        else:
            bot.send_message(chat_id, 'Не удалось найти ID отправителя резюме.')
    elif callback.data.startswith('reject_'):
        resume_chat_id = callback.data.split('_')[1]
        submitter_id = resume_submitters.get(int(resume_chat_id))
        if submitter_id:
            bot.send_message(submitter_id, 'К сожалению, ваше резюме нам не подошло.')
            bot.send_message(chat_id, 'Резюме отклонено.')
        else:
            bot.send_message(chat_id, 'Не удалось найти ID отправителя резюме.')
    elif callback.data == 'add_technical_task':
        waiting_for_technical_task[chat_id] = True
        bot.send_message(chat_id, 'Пожалуйста, отправьте ваше техническое задание. Если есть какие-либо файлы, отправьте их вместе с текстом отдельным сообщением.')
    elif callback.data.startswith('approve1_'):
        technical_task_id = callback.data.split('_')[1]
        submitter1_id = technical_task_submitters.get(int(technical_task_id))
        if submitter1_id:
        
            markup = types.InlineKeyboardMarkup()
            bot_link_button = types.InlineKeyboardButton('Перейти к боту', url=f"https://t.me/NIKITAIvachenko_bot?start=sendactions")
            markup.add(bot_link_button)
            bot.send_message(chat_id, "Нажмите на кнопку ниже, чтобы начать работу:", reply_markup=markup)


def send_actions_menu1(chat_id):
    markup = types.InlineKeyboardMarkup()
    bt3 = types.InlineKeyboardButton('Добавить резюме', callback_data='add_resume')
    bt4 = types.InlineKeyboardButton('Изменить резюме', callback_data='edit_resume')
    bt5 = types.InlineKeyboardButton('Удалить резюме', callback_data='delete_resume')
    markup.add(bt3, bt4)
    markup.add(bt5)
    bot.send_message(chat_id, 'Выберите предпочитаемое действие:', reply_markup=markup)


def send_actions_menu2(chat_id):
    markup = types.InlineKeyboardMarkup()
    bt6 = types.InlineKeyboardButton('Добавить техническое задание', callback_data='add_technical_task')
    bt7 = types.InlineKeyboardButton('Изменить техническое задание', callback_data='edit_technical_task')
    bt8 = types.InlineKeyboardButton('Удалить техническое задание', callback_data='delete_technical_task')
    markup.add(bt6, bt7)
    markup.add(bt8)
    bot.send_message(chat_id, 'Выберите предпочитаемое действие:', reply_markup=markup)


def resume_approved(submitter_id):
    markup = types.InlineKeyboardMarkup()
    bt11 = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
    bt12 = types.InlineKeyboardButton('Отклонить', callback_data='non_confirm')
    markup.add(bt11, bt12)
    bot.send_message(submitter_id, 'Ваше резюме было принято, можете приступать к выполнению заказа.', reply_markup=markup)


bot.infinity_polling()


'''5202136450'''
'''1098482972'''
'''-1002212279206'''