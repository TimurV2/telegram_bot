from links_funcs import write_link
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import io
from telebot import types

TELEGRAM_TOKEN = '5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E'

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler
def text_message_handler(message):
    match message.text:
        case "Ссылки":
            links_msg = write_link()
            bot.send_message(message.chat.id, links_msg)
        case "Контакты":
            path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
            with io.open(path, encoding='utf-8') as file:
                text = file.read()
                bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Ссылки", "Контакты"]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Wait...', reply_markup=keyboard)


bot.polling(none_stop=True)
