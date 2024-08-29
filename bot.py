import telebot
from telebot import types
import logging
import webbrowser

TOKEN = '7506077102:AAEmxERM3-mogzrLbXS62ccQt0TCzEp1bkc'
bot = telebot.TeleBot(TOKEN)


logging.basicConfig(level=logging.INFO)


waiting_for_resume = {}

resume_submitters = {}

waiting_for_technical_task={}

technical_task_submitters={}

start_count = {}

technical_task_counter = 0

user_technical_tasks = {}

authorized_users=[1098482972]

last_technical_task_id = {}

last_technical_task_message_id = {} 

editing_technical_task = {}

for_confirmation = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):

    user_id = message.chat.id
    
    if user_id in start_count:
        start_count[user_id] += 1
    
    else:
        start_count[user_id] = 1
    
    if "sendactions" in message.text:
        send_actions_menu1(message.chat.id)
        
    elif message.chat.id in authorized_users:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('ССылка на тг канал', url=f"https://t.me/free_chanel90")
        markup.add(bt1)
        markup.add(types.InlineKeyboardButton('Добавить ТЗ', callback_data='customer'))
        bot.reply_to(message, 'Выберите предпочитаемое действие:', reply_markup=markup)
        
    elif start_count[user_id] < 3 and user_id not in authorized_users:
        bot.send_message(user_id, 'Недоступная функция')
        
    elif start_count[user_id] >= 3 and user_id not in authorized_users:
        bot.send_message(user_id, 'Пошел нахуй отсюда, черт')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'В команде /info, отображается информауия по работе с ботом \nКоманда /start выводит кнопки для начала действия бота \nКоманда /id выводит id аользователя \nКоманда /legend выводит аккаунт создателя бота')


@bot.message_handler(commands=['id'])
def send_id(message):
    bot.send_message(message.chat.id, F'Ваш ID {message.from_user.id}')


@bot.message_handler(commands=['legend'])
def send_legend(message):
    bot.send_message(message.chat.id, 'Ходит легенда о бодром боровике, сделавшем этого бота \n@biznesmanil - его имя')


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, 'Информация по работе с ботом')
    
    
@bot.message_handler(func=lambda message: message.chat.id in waiting_for_resume and waiting_for_resume[message.chat.id])
def handle_resume(message):
    submitter_id = message.from_user.id

    developer_chat_id = 1098482972  # ID разработчика

    task_number = user_technical_tasks.get(message.chat.id)

    resume_submitters[message.chat.id] = submitter_id

    markup = types.InlineKeyboardMarkup()
    bt9 = types.InlineKeyboardButton('Approve', callback_data=f'approve_{message.chat.id}')
    bt10 = types.InlineKeyboardButton('Reject', callback_data=f'reject_{message.chat.id}')
    markup.add(bt9, bt10)

    try:
        
        if message.content_type == 'text':
            bot.send_message(developer_chat_id, f"Резюме от пользователя (@{message.from_user.username}) на техническое задание №{task_number}:\n{message.text}", reply_markup=markup)
    
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке резюме: {str(e)}")
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке резюме: {str(e)}")
    
    del waiting_for_resume[message.chat.id]
    bot.send_message(message.chat.id, "Ваше резюме было успешно отправлено разработчику! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")


@bot.message_handler(func=lambda message: message.chat.id in waiting_for_technical_task and waiting_for_technical_task[message.chat.id])
def handle_technical_task(message):
    global technical_task_counter

    technical_task_counter += 1

    submitter1_id = message.from_user.id

    chanel_chat_id = -1002212279206  # ID тгк

    technical_task_submitters[message.chat.id] = submitter1_id
    user_technical_tasks[submitter1_id] = technical_task_counter
    last_technical_task_id[message.chat.id] = technical_task_counter
    markup = types.InlineKeyboardMarkup()
    bt20 = types.InlineKeyboardButton('Approve', url=f"https://t.me/NIKITAIvachenko_bot?start=sendactions")
    bt21 = types.InlineKeyboardButton('Reject', callback_data=f'reject1_{submitter1_id}')
    markup.add(bt20, bt21)

    try:
        msg = bot.send_message(chanel_chat_id, f"Техническое задание №{technical_task_counter}:\n{message.text}", reply_markup=markup)
        last_technical_task_message_id[message.chat.id] = msg.message_id

    except Exception as e:
        logging.error(f"Произошла ошибка при отправке ТЗ: {str(e)}")
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке ТЗ: {str(e)}")

    del waiting_for_technical_task[message.chat.id]
    bot.send_message(message.chat.id, f"Ваше техническое задание было успешно отправлено в тгк под номером {technical_task_counter}! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")


@bot.message_handler(func=lambda message: message.chat.id in editing_technical_task and editing_technical_task[message.chat.id])
def edit_technical_task(message):
    chat_id = message.chat.id

    task_number = user_technical_tasks.get(message.chat.id)

    if chat_id in last_technical_task_message_id:
        message_id = last_technical_task_message_id[chat_id]
        chanel_chat_id = -1002212279206  # ID  тгк

        try:
            bot.edit_message_text(f"Техническое задание №{task_number}:\n{message.text}", chat_id=chanel_chat_id, message_id=message_id)
            bot.send_message(chat_id, "Техническое задание успешно обновлено.")
            del editing_technical_task[chat_id]  

        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка при обновлении сообщения: {str(e)}")

    else:
        bot.send_message(chat_id, "Не найдено техническое задание для редактирования.")
        del editing_technical_task[chat_id]


@bot.message_handler(content_types=['photo'])
def send_photo_0(message):
    
    photo_id = None

    if (message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id]) and message.chat.id not in authorized_users:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return
    

    elif (message.chat.id not in waiting_for_technical_task or not waiting_for_technical_task[message.chat.id]) and message.chat.id in authorized_users:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки технического задания. Пожалуйста, используйте команду /start и выберите соответствующее действие")
        return

    elif message.chat.id not in authorized_users:
        try:
            photo_id = message.photo[-1].file_id
            developer_chat_id = 1098482972  # ID  разработчика
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            bot.send_photo(developer_chat_id, photo_id, caption=f"Резюме (фото) на техническое задание №{task_number} от пользователя (@{message.from_user.username})")
            bot.send_message(message.chat.id, "Ваше фото было успешно отправлено разработчику.")
        
        except Exception as e:
            if photo_id is None:
                bot.send_message(message.chat.id, "Не удалось получить идентификатор фото.")
            
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {str(e)}")

    elif message.chat.id in authorized_users:
        try:
            photo_id = message.photo[-1].file_id
            developer_chat_id = -1002212279206  # ID  тгк
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            bot.send_photo(developer_chat_id, photo_id, caption=f"Техническое задание (фото) №{task_number}")
            bot.send_message(message.chat.id, "Ваше фото было успешно отправлено в тгк.")
        
        except Exception as e:
            if photo_id is None:
                bot.send_message(message.chat.id, "Не удалось получить идентификатор фото.")
        
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {str(e)}")


@bot.message_handler(content_types=['document'])
def send_document_0(message):
    
    if message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id] and message.chat.id not in authorized_users:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return

    elif message.chat.id not in waiting_for_technical_task or not waiting_for_technical_task[message.chat.id] and message.chat.id in authorized_users:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме ожидания отправки технического задания. Пожалуйста, используйте команду /start и выберите соответствующее действие")
        return
    
    developer_chat_id = 1098482972  # ID разработчика
    task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")

    bot.send_document(developer_chat_id, message.document.file_id, caption=f"Резюме (документ) на техническое задание №{task_number} от пользователя (@{message.from_user.username})")
    
    bot.send_message(message.chat.id, "Ваш документ был успешно отправлен разработчику.")


@bot.callback_query_handler(func = lambda call: True)
def callback_message(call):
    
    chat_id = call.message.chat.id
    
    if call.data == 'customer':
        send_actions_menu2(chat_id)
        
    elif call.data == 'add_resume':
        waiting_for_resume[chat_id] = True
        bot.send_message(chat_id, 'Пожалуйста, отправьте ваше резюме. Если есть какие-либо файлы, отправьте их вместе с текстом отдельным сообщением.')
    
    elif call.data.startswith('approve_'):
        developer_id = 1098482972
        resume_chat_id = call.data.split('_')[1]
        submitter_id = resume_submitters.get(int(resume_chat_id))
        
        if submitter_id:
            confirmation(developer_id)
            for_confirmation[call.message.chat.id] = submitter_id
            
        else:
            bot.send_message(chat_id, 'Не удалось найти ID отправителя резюме.')
    
    elif call.data == 'confirm52':
        submitter_id = for_confirmation.get(call.message.chat.id)
        resume_approved(submitter_id)
        bot.send_message(chat_id, 'Резюме одобрено и отправлено пользователю.')

    elif call.data.startswith('reject_'):
        resume_chat_id = call.data.split('_')[1]
        submitter_id = resume_submitters.get(int(resume_chat_id))
        
        if submitter_id:
            bot.send_message(submitter_id, 'К сожалению, ваше резюме нам не подошло.')
            bot.send_message(chat_id, 'Резюме отклонено.')
        
        else:
            bot.send_message(chat_id, 'Не удалось найти ID отправителя резюме.')
    
    elif call.data == 'add_technical_task':
        waiting_for_technical_task[chat_id] = True
        bot.send_message(chat_id, 'Пожалуйста, отправьте ваше техническое задание. Если есть какие-либо файлы, отправьте их вместе с текстом отдельным сообщением.')
    
    elif call.data.startswith('approve1_'):
        technical_task_id = call.data.split('_')[1]
        submitter1_id = technical_task_submitters.get(int(technical_task_id))
        
        if submitter1_id:
            markup = types.InlineKeyboardMarkup()
            bot_link_button = types.InlineKeyboardButton('Перейти к боту', url=f"https://t.me/NIKITAIvachenko_bot?start=sendactions")
            markup.add(bot_link_button)
            bot.send_message(chat_id, "Нажмите на кнопку ниже, чтобы начать работу:", reply_markup=markup)

    elif call.data == 'delete_technical_task':

        if chat_id in last_technical_task_message_id:
            message_id = last_technical_task_message_id[chat_id]
            chanel_chat_id = -1002212279206  # ID  тгк

            try:
                bot.delete_message(chanel_chat_id, message_id)
                bot.send_message(chat_id, "Последнее техническое задание было успешно удалено.")
                del last_technical_task_message_id[chat_id] 

            except Exception as e:
                bot.send_message(chat_id, f"Произошла ошибка при удалении сообщения: {str(e)}")

        else:
            bot.send_message(chat_id, "Не найдено техническое задание для удаления.")

    elif call.data == 'confirm':

        chanel_chat_id = -1002212279206  # ID  тгк
        developer_id = 1098482972 # ID  разработчика
        username = call.from_user.username

        try:
            bot.send_message(developer_id, f"@{username} приступил к выполнению заказа")
            bot.send_message(call.message.chat.id, f"Приступайте к выполнению")

        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка при удалении сообщения: {str(e)}")

    elif call.data == 'non_confirm':
        bot.send_message(chat_id, "Спасибо за потраченное время")
        bot.send_message(1098482972, "В последний момент, уебок отказался")

    elif call.data == 'edit_technical_task':
        editing_technical_task[chat_id] = True
        bot.send_message(chat_id, 'Введите новый текст для последнего технического задания:')


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


def confirmation(developer_id):
    markup = types.InlineKeyboardMarkup()
    bt52 = types.InlineKeyboardButton('Подтвердить(да, он достоин)', callback_data = 'confirm52')
    markup.add(bt52)
    bot.send_message(developer_id, 'Вы уверены, что он достоин?', reply_markup=markup)


bot.infinity_polling()


'''5202136450'''
'''1098482972'''
'''-1002212279206'''
'''authorized_users=[7374493167, 1048033836]'''