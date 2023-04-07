from aiogram import Bot, Dispatcher, executor, types
import openai
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, italic
from aiogram.utils import executor
from io import BytesIO
from aiogram.dispatcher import FSMContext
from pytube import YouTube
import os
from PIL import ImageGrab
import os
import pyautogui
import aiogram.utils.markdown as md
import webbrowser
from aiogram.types import ParseMode
from datetime import datetime
from googletrans import Translator
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from aiogram.types import  InlineKeyboardButton
from aiogram import executor


openai.api_key = "API GPT "
openai.Model.list()


API_TOKEN = 'API BOT'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['message'])
async def send_message_on_screen(message: types.Message):
    text = message.text.split(' ', maxsplit=1)[1]
    pyautogui.alert(text)
    await message.reply(f'Message "{text}" has been displayed on the screen')

# обработка команды help
@dp.message_handler(commands=['help_MyPCMaksim'])
async def help_command(message: types.Message):
    await message.reply("Я могу выполнить следующие команды:\n"
                       "/open_site\n"
                        "/start_Видео Редактор\n"
                        "/start_гугл\n"
                        "/презагрузка\n"
                        "/start_вскод\n"
                        "/sleep \n"
                        "/mouse_click\n"
                        "/Скриншот\n"
                        "/Выключить\n")




# список сайтов
sites = ['https://www.youtube.com/', 'https://chat.openai.com/chat', 'https://classroom.google.com/']

# обработчик команды /open_site
@dp.message_handler(commands=['open_site'])
async def open_site(message: types.Message):
    # проверяем, есть ли аргумент с индексом сайта
    if len(message.text.split()) == 2:
        try:
            index = int(message.text.split()[1]) # получаем индекс сайта из аргумента
            if index >= 0 and index < len(sites): # проверяем, что индекс в допустимом диапазоне
                webbrowser.open_new_tab(sites[index]) # открываем сайт в новой вкладке браузера
                await message.reply(f"Сайт {sites[index]} открыт")
            else:
                await message.reply("Неверный индекс сайта")
        except ValueError:
            await message.reply("Индекс сайта должен быть числом")
    else:
        await message.reply("Укажите индекс сайта")


@dp.message_handler(commands=['start_Видео Редактор'])
async def start_program(message: types.Message):
    os.startfile("D:\Movavi Video Editor Plus\VideoEditorPlus.exe")
    await message.reply("Программа запущена!")

@dp.message_handler(commands=['start_гугл'])
async def start_program(message: types.Message):
    os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
    await message.reply("Программа запущена!")

@dp.message_handler(commands=['презагрузка'])
async def reboot_computer(message: types.Message):
    os.system("shutdown /r /t 1")
    await message.reply("Компьютер перезагружается...")

@dp.message_handler(commands=['start_вскод'])
async def start_program(message: types.Message):
    os.startfile("D:\Microsoft VS Code\Code.exe")
    await message.reply("Программа запущена!")
 
# обработчик команды "sleep"
@dp.message_handler(commands=['sleep'])
async def sleep_command(message: types.Message):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0") # переводим компьютер в спящий режим

# Обработчик команды /mouse_click
@dp.message_handler(commands=['mouse_click'])
async def click_mouse(message: types.Message):
    # Клик мыши
    pyautogui.click()
    await message.reply("Клик мыши выполнен")

# создаем список администраторов, которые будут получать уведомления о сообщениях от пользователей
admin_usernames = ['@officialdarkhack']
# добавляем обработчик команды /support
@dp.message_handler(commands=['support'])
async def support_command(message: types.Message):
    # формируем текст сообщения с инструкциями по использованию чата поддержки
    text = 'Для обращения в службу поддержки используйте чат: @officialdarkhack'

    # отправляем сообщение пользователю
    await message.answer(text)

# добавляем обработчик сообщений для чата поддержки
@dp.message_handler(chat_type=types.ChatType.GROUP, content_types=types.ContentTypes.ANY)
async def support_chat_message(message: types.Message):
    if message.from_user.username:
        # формируем текст сообщения
        text = f'Сообщение от @{message.from_user.username}:\n\n{message.text}'
    else:
        # если у пользователя нет имени пользователя, используем его имя
        text = f'Сообщение от {message.from_user.full_name}:\n\n{message.text}'
    # отправляем сообщение администраторам
    for admin_username in admin_usernames:
        await bot.send_message(admin_username, text)

## Обработчик команды /Скриншот и кнопки "Скриншот экрана"
@dp.message_handler(commands=['Скриншот'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'Скриншот')
async def screenshot(message: types.Message):
    # Получаем скриншот экрана
    screenshot = ImageGrab.grab()

    # Сохраняем скриншот в файл
    screenshot.save("screenshot.png")

    # Отправляем скриншот пользователю
    with open("screenshot.png", "rb") as file:
        await bot.send_photo(chat_id=message.chat.id, photo=file)

# Обработчик команды /shutdown и кнопки "Выключить компьютер"
@dp.message_handler(commands=['Выключить'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'Выключить')
async def shutdown(message: types.Message):
    # Выполняем команду выключения компьютера
    os.system("shutdown /s /t 1")
    await message.answer("Компьютер будет выключен в течение 1 секунд.")

# обработчик команды /download
@dp.message_handler(commands=['download'])
async def download_video(message: types.Message):
    # получаем ссылку на видео из текста сообщения
    video_url = message.text.replace('/download ', '')

    # скачиваем видео с помощью pytube
    yt = YouTube(video_url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    buffer = BytesIO()
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    # отправляем видео пользователю
    await bot.send_video(message.chat.id, buffer)

# Обработчик команды /help
@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    help_text = "Список доступных команд:\n"
    help_text += "/help - Get help on commands\n"
    help_text += "/ChatGpt - start using ChatGpt absolutely free\n"
    help_text += "/download  - start using Download Video YouTube free когда вы пишите /download не забудьте добавить сылку на видео \n"
    help_text += "/support - Данная Команда позваляет вам иметь прямую связь с Владельцом Данного Канала Любый вопрсы пишыте мне в личку (: ) \n"
    # Отправляем сообщение пользователю
    await message.reply(help_text, parse_mode=ParseMode.HTML)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("our telegram group")
    button2 = types.KeyboardButton("Author Support")
    keyboard.add(button1, button2,)
    await message.answer("Welcome!если нужно больше команд пропишы команду /help там есть все комади :", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.message_handler(lambda message: message.text == "our telegram group")
async def process_button1(message: types.Message):
    await message.answer("subscription https://t.me/darklaboratoryX ")

@dp.message_handler(lambda message: message.text == "Author Support")
async def process_button2(message: types.Message):
    await message.answer("Author Support https://new.donatepay.ru/@957785 write to learn all the commands help")



@dp.message_handler(commands=['ChatGpt'])
async def start_command(message: types.Message):
    await message.answer(f'💡 Добро пожаловать, {message.from_user.first_name}!')

@dp.message_handler()
async def answer(message: types.Message):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.9,
        max_tokens=3246,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    await message.reply(response['choices'][0]['text'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
