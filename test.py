import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import os


TELEGRAM_TOKEN = str(os.environ['bot_token'])
bot = telebot.TeleBot(TELEGRAM_TOKEN)
urls = ['https://horo.mail.ru/prediction/aries/today/',
        'https://horo.mail.ru/prediction/taurus/today/',
        'https://horo.mail.ru/prediction/gemini/today/',
        'https://horo.mail.ru/prediction/cancer/today/',
        'https://horo.mail.ru/prediction/leo/today/',
        'https://horo.mail.ru/prediction/virgo/today/',
        'https://horo.mail.ru/prediction/libra/today/',
        'https://horo.mail.ru/prediction/scorpio/today/',
        'https://horo.mail.ru/prediction/sagittarius/today/',
        'https://horo.mail.ru/prediction/capricorn/today/',
        'https://horo.mail.ru/prediction/aquarius/today/',
        'https://horo.mail.ru/prediction/pisces/today/']

# url = 'https://horo.mail.ru/prediction/aries/today/'
# responce = requests.get(url)
# soup = BeautifulSoup(responce.text, 'html.parser')
# prediction = soup.find_all('p')
# prediction[0] = str(prediction[0]).replace('<p>', '').replace('</p>', '')
# prediction[1] = str(prediction[1]).replace('<p>', '').replace('</p>', '')


@bot.message_handler()
def ask_horo(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    b1 = types.InlineKeyboardButton('Овен♈️', callback_data='Овен')
    b2 = types.InlineKeyboardButton('Телец♉️', callback_data='Телец')
    b3 = types.InlineKeyboardButton('Близнецы♊️', callback_data='Близнецы')
    b4 = types.InlineKeyboardButton('Рак♋️', callback_data='Рак')
    b5 = types.InlineKeyboardButton('Лев♌️', callback_data='Лев')
    b6 = types.InlineKeyboardButton('Дева♍️', callback_data='Дева')
    b7 = types.InlineKeyboardButton('Весы♎️', callback_data='Весы')
    b8 = types.InlineKeyboardButton('Скорпион♏️', callback_data='Скорпион')
    b9 = types.InlineKeyboardButton('Стрелец♐️', callback_data='Стрелец')
    b10 = types.InlineKeyboardButton('Козерог♑️', callback_data='Козерог')
    b11 = types.InlineKeyboardButton('Водолей♒️', callback_data='Водолей')
    b12 = types.InlineKeyboardButton('Рыбы♓️', callback_data='Рыбы')
    markup.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
    bot.send_message(message.chat.id, 'Выберите ваш знак зодиака:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        match call.data:
            case "Овен":
                url = urls[0]
            case "Телец":
                url = urls[1]
            case "Близнецы":
                url = urls[2]
            case "Рак":
                url = urls[3]
            case "Лев":
                url = urls[4]
            case "Дева":
                url = urls[5]
            case "Весы":
                url = urls[6]
            case "Скорпион":
                url = urls[7]
            case "Стрелец":
                url = urls[8]
            case "Козерог":
                url = urls[9]
            case "Водолей":
                url = urls[10]
            case "Рыбы":
                url = urls[11]

        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        prediction = soup.find_all('p')
        prediction[0] = str(prediction[0]).replace('<p>', '').replace('</p>', '')
        prediction[1] = str(prediction[1]).replace('<p>', '').replace('</p>', '')
        bot.send_message(call.message.chat.id, f'{prediction[0]}\n\n' + f'{prediction[1]}')


# bot.polling(none_stop=True)