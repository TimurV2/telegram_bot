import csv
import telebot
from telebot import types
from helpful_funcs import gen_markup
import os

TELEGRAM_TOKEN = str(os.environ['bot_token'])
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def add_user(user_id, first_name, last_name, user_name):
    attend = False
    user_info = [user_id, first_name, last_name, user_name]
    with open('users_hub.csv', 'a', newline='', encoding='utf-8') as writable_file:
        with open('users_hub.csv', 'r') as readable_file:
            reader = csv.DictReader(readable_file)
            for row in reader:
                if str(user_id) in row['ID']:
                    attend = True
                    readable_file.close()
                    break
        if not attend:
            writer = csv.writer(writable_file)
            writer.writerow(user_info)
            writable_file.close()


def sent_notify(message):
    msg = message.text
    avoid_id = message.chat.id
    with open('users_hub.csv', 'r') as readable_file:
        reader = csv.DictReader(readable_file)
        for row in reader:
            if (str(avoid_id) not in row['ID']) and (message.text not in ["Ссылки", "Контакты", "Инициализация", "Оставить отзыв", "Помощь", "Уведомить всех", "Гороскоп"]):
                curr_id = int(row['ID'])
                bot.send_message(curr_id, f'<u>Общее уведомление от пользователя - '
                                          f'@{message.from_user.username}\n</u>' + msg, parse_mode='html')
    bot.send_message(message.chat.id, 'Ваше уведомление было отправлено остальным пользователям!', reply_markup=gen_markup())


def frw_msg(message):
    if (message.chat.id != 993945655) and (message.text not in ["Ссылки", "Контакты", "Инициализация", "Оставить отзыв", "Помощь", "Уведомить всех", "Гороскоп"]):
        bot.forward_message(993945655, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено. Спасибо за обратную связь!', reply_markup=gen_markup())


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
