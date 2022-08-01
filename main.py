import telebot
from telebot import types
import io


bot = telebot.TeleBot('5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E') # Создаем "bot" передаём в него токен бота в TG

@bot.message_handler()
def input_error(message):
    if message.text == 'Контакты преподов':
        path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
        with io.open(path, encoding='utf-8') as file:
            text = file.read()
            bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start']) # Создаем кнопки
def Help_Buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    feedback = types.KeyboardButton('Оставить отзыв')
    contacts = types.KeyboardButton('Контакты преподов')
    markup.add(feedback, contacts)
    bot.send_message(message.chat.id, 'Вот что я могу сделать:', reply_markup=markup)


bot.polling(none_stop = True) # Задаём вечное время работы боту