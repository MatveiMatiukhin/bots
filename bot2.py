from aiogram import Bot, Dispatcher, types
from aiogram.utils import Command
import logging

TOKEN = '7506077102:AAEOyherkIla8l4W9F_SUE0OhpccwpaaoJ4'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

waiting_for_resume = {}
resume_submitters = {}
waiting_for_technical_task = {}
technical_task_submitters = {}
start_count = {}
technical_task_counter = 0
user_technical_tasks = {}
authorized_users = [1098482972]
last_technical_task_id = {}
last_technical_task_message_id = {}
editing_technical_task = {}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.chat.id
    
    if user_id in start_count:
        start_count[user_id] += 1
    else:
        start_count[user_id] = 1

    if "sendactions" in message.text:
        await send_actions_menu1(message.chat.id)
    elif message.chat.id in authorized_users:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('ССылка на тг канал', url="https://t.me/free_chanel90")
        markup.add(bt1)
        markup.add(types.InlineKeyboardButton('Добавить ТЗ', callback_data='customer'))
        await message.reply('Выберите предпочитаемое действие:', reply_markup=markup)
    elif start_count[user_id] < 3 and user_id not in authorized_users:
        await message.answer('Недоступная функция')
    elif start_count[user_id] >= 3 and user_id not in authorized_users:
        await message.answer('Пошел нахуй отсюда, черт')

@dp.message(Command['help'])
async def send_help(message: types.Message):
    await message.answer('В команде /info, отображается информация по работе с ботом \nКоманда /start выводит кнопки для начала действия бота \nКоманда /id выводит id пользователя \nКоманда /legend выводит аккаунт создателя бота')

@dp.message(Command['id'])
async def send_id(message: types.Message):
    await message.answer(f'Ваш ID {message.from_user.id}')

@dp.message(Command['legend'])
async def send_legend(message: types.Message):
    await message.answer('Ходит легенда о бодром боровике, сделавшем этого бота \n@biznesmanil - его имя')

@dp.message(Command['info'])
async def send_info(message: types.Message):
    await message.answer('Информация по работе с ботом')

@dp.message_handler(lambda message: message.chat.id in waiting_for_resume and waiting_for_resume[message.chat.id])
async def handle_resume(message: types.Message):
    submitter_id = message.from_user.id
    developer_chat_id = 1098482972
    task_number = user_technical_tasks.get(message.chat.id)
    resume_submitters[message.chat.id] = submitter_id
    markup = types.InlineKeyboardMarkup()
    bt9 = types.InlineKeyboardButton('Approve', callback_data=f'approve_{message.chat.id}')
    bt10 = types.InlineKeyboardButton('Reject', callback_data=f'reject_{message.chat.id}')
    markup.add(bt9, bt10)

    try:
        if message.content_type == 'text':
            await bot.send_message(developer_chat_id, f"Резюме от пользователя (@{message.from_user.username}) на техническое задание №{task_number}:\n{message.text}", reply_markup=markup)
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке резюме: {str(e)}")
        await message.answer(f"Произошла ошибка при отправке резюме: {str(e)}")
    
    del waiting_for_resume[message.chat.id]
    await message.answer("Ваше резюме было успешно отправлено разработчику! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")

@dp.message_handler(lambda message: message.chat.id in waiting_for_technical_task and waiting_for_technical_task[message.chat.id])
async def handle_technical_task(message: types.Message):
    global technical_task_counter
    technical_task_counter += 1
    submitter1_id = message.from_user.id
    chanel_chat_id = -1002212279206
    technical_task_submitters[message.chat.id] = submitter1_id
    user_technical_tasks[submitter1_id] = technical_task_counter
    last_technical_task_id[message.chat.id] = technical_task_counter
    markup = types.InlineKeyboardMarkup()
    bt20 = types.InlineKeyboardButton('Approve', url="https://t.me/NIKITAIvachenko_bot?start=sendactions")
    bt21 = types.InlineKeyboardButton('Reject', callback_data=f'reject1_{submitter1_id}')
    markup.add(bt20, bt21)

    try:
        msg = await bot.send_message(chanel_chat_id, f"Техническое задание №{technical_task_counter}:\n{message.text}", reply_markup=markup)
        last_technical_task_message_id[message.chat.id] = msg.message_id
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке ТЗ: {str(e)}")
        await message.answer(f"Произошла ошибка при отправке ТЗ: {str(e)}")

    del waiting_for_technical_task[message.chat.id]
    await message.answer(f"Ваше техническое задание было успешно отправлено в тгк под номером {technical_task_counter}! \nЖдите ответа от администратора \nОтвет прийдет в этот чат")

@dp.message_handler(lambda message: message.chat.id in editing_technical_task and editing_technical_task[message.chat.id])
async def edit_technical_task(message: types.Message):
    chat_id = message.chat.id
    task_number = user_technical_tasks.get(message.chat.id)

    if chat_id in last_technical_task_message_id:
        message_id = last_technical_task_message_id[chat_id]
        chanel_chat_id = -1002212279206

        try:
            await bot.edit_message_text(f"Техническое задание №{task_number}:\n{message.text}", chat_id=chanel_chat_id, message_id=message_id)
            await message.answer("Техническое задание успешно обновлено.")
            del editing_technical_task[chat_id]  
        except Exception as e:
            await message.answer(f"Произошла ошибка при обновлении сообщения: {str(e)}")
    else:
        await message.answer("Не найдено техническое задание для редактирования.")
        del editing_technical_task[chat_id]

@dp.message_handler(content_types=['photo'])
async def send_photo_0(message: types.Message):
    photo_id = None
    if (message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id]) and message.chat.id not in authorized_users:
        await message.answer("Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return
    elif (message.chat.id not in waiting_for_technical_task or not waiting_for_technical_task[message.chat.id]) and message.chat.id in authorized_users:
        await message.answer("Вы не находитесь в режиме ожидания отправки технического задания. Пожалуйста, используйте команду /start и выберите соответствующее действие")
        return
    elif message.chat.id not in authorized_users:
        try:
            photo_id = message.photo[-1].file_id
            developer_chat_id = 1098482972
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            await bot.send_photo(developer_chat_id, photo_id, caption=f"Резюме (фото) на техническое задание №{task_number} от пользователя (@{message.from_user.username})")
            await message.answer("Ваше фото было успешно отправлено разработчику.")
        except Exception as e:
            if photo_id is None:
                await message.answer("Не удалось получить идентификатор фото.")
            else:
                await message.answer(f"Произошла ошибка при отправке фото: {str(e)}")
    elif message.chat.id in authorized_users:
        try:
            photo_id = message.photo[-1].file_id
            developer_chat_id = -1002212279206
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            await bot.send_photo(developer_chat_id, photo_id, caption=f"Техническое задание (фото) №{task_number}")
            await message.answer("Ваше фото было успешно отправлено в тгк.")
        except Exception as e:
            if photo_id is None:
                await message.answer("Не удалось получить идентификатор фото.")
            else:
                await message.answer(f"Произошла ошибка при отправке фото: {str(e)}")

@dp.message_handler(content_types=['document'])
async def send_document_0(message: types.Message):
    if message.chat.id not in waiting_for_resume or not waiting_for_resume[message.chat.id] and message.chat.id not in authorized_users:
        await message.answer("Вы не находитесь в режиме ожидания отправки резюме. Пожалуйста, используйте команду /start и выберите действие.")
        return
    elif message.chat.id not in waiting_for_technical_task or not waiting_for_technical_task[message.chat.id] and message.chat.id in authorized_users:
        await message.answer("Вы не находитесь в режиме ожидания отправки технического задания. Пожалуйста, используйте команду /start и выберите соответствующее действие")
        return
    elif message.chat.id not in authorized_users:
        try:
            document = message.document
            file_id = document.file_id
            developer_chat_id = 1098482972
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            await bot.send_document(developer_chat_id, file_id, caption=f"Резюме (документ) на техническое задание №{task_number} от пользователя (@{message.from_user.username})")
            await message.answer("Ваш документ был успешно отправлен разработчику.")
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке документа: {str(e)}")
    elif message.chat.id in authorized_users:
        try:
            document = message.document
            file_id = document.file_id
            developer_chat_id = -1002212279206
            task_number = user_technical_tasks.get(message.chat.id, "Неизвестно")
            await bot.send_document(developer_chat_id, file_id, caption=f"Техническое задание (документ) №{task_number}")
            await message.answer("Ваш документ был успешно отправлен в тгк.")
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке документа: {str(e)}")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('approve'))
async def process_approve(callback_query: types.CallbackQuery):
    chat_id = int(callback_query.data.split('_')[1])
    submitter_id = resume_submitters.get(chat_id)
    if submitter_id:
        await bot.send_message(submitter_id, "Ваше резюме было одобрено!")
    await callback_query.answer("Резюме одобрено.")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('reject'))
async def process_reject(callback_query: types.CallbackQuery):
    chat_id = int(callback_query.data.split('_')[1])
    submitter_id = resume_submitters.get(chat_id)
    if submitter_id:
        await bot.send_message(submitter_id, "Ваше резюме было отклонено!")
    await callback_query.answer("Резюме отклонено.")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('reject1'))
async def process_reject1(callback_query: types.CallbackQuery):
    submitter_id = int(callback_query.data.split('_')[1])
    if submitter_id:
        await bot.send_message(submitter_id, "Ваше техническое задание было отклонено!")
    await callback_query.answer("Техническое задание отклонено.")

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'customer')
async def handle_customer(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите действие:")
    # You can add additional inline keyboard options or actions here

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
