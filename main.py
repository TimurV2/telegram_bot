import telebot
from telebot import types
import io


# TODO: - add config to gide token and other info
bot = telebot.TeleBot('5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E')  # Создаем "bot" передаём в него токен бота в TG


# TODO: - change buttons & start command
@bot.message_handler(commands=['start'])  # Создаем кнопки
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contacts = types.KeyboardButton('Дать контакты преподов')
    markup.add(contacts)
    bot.send_message(message.chat.id, 'Вот что я могу сделать:', reply_markup=markup)


@bot.message_handler(commands=['feedback'])
def feedback(message):
    sent = bot.send_message(message.chat.id,
                            'Оставьте свой <u>отзыв / пожелания</u> в следующем сообщении, '
                            'оно будет переслано создателю сего бота.',
                            parse_mode='html')
    bot.register_next_step_handler(sent, frw_msg)
def frw_msg(message):
    if (message.chat.id != 993945655) and (message.text[0] != '/'):
        bot.forward_message(993945655, message.chat.id, message.message_id)


@bot.message_handler(commands=['contacts'])
def text_parser(message):
    path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
    with io.open(path, encoding='utf-8') as file:
        text = file.read()
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Лог команд:\n'
                                      '/contacts - для получения списка контактов преподов\n'
                                      '/feedback - для отправки отзыва / предложений / сообщения\n'
                                      '/start - /// пока в доработке ///\n'
                                      '/links - полезные ссылки\n'
                                      '')


from link_push import find_url
@bot.message_handler(commands=['linkpush'])
def link_push(message):
    sent = bot.send_message(message.chat.id, 'В <u>одном сообщении</u> введите ссылку и затем её описание', parse_mode='html')
    bot.register_next_step_handler(sent, find_url)


bot.polling(none_stop=True)  # Задаём вечное время работы боту
