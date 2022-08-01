import telebot
from telebot import types
import io


bot = telebot.TeleBot('5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E') # Создаем "bot" передаём в него токен бота в TG

@bot.message_handler(commands=['start']) # Создаем кнопки
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    feedback = types.KeyboardButton('Оставить отзыв')
    contacts = types.KeyboardButton('Контакты преподов')
    markup.add(feedback, contacts)
    bot.send_message(message.chat.id, 'Вот что я могу сделать:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def input_error(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if (message.text == 'Контакты преподов'): # Выводим информацию о преподах
        path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
        with io.open(path, encoding='utf-8') as file:
            text = file.read()
            bot.send_message(message.chat.id, text, reply_markup=markup)

    elif (message.text == 'Оставить отзыв'):
        bot.send_message(message.chat.id,
                         'Оставьте свой <u>отзыв / пожелания</u> в следующем сообщении, оно будет переслано создателю сего бота.',
                         parse_mode='html',reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def handle_message(message):
            users_feed_back = message.text
            bot.send_message(993945655, users_feed_back, reply_markup=markup)


bot.polling(none_stop=True) # Задаём вечное время работы боту